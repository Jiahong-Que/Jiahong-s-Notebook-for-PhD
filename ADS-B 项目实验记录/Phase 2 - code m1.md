

## ✅ 1. 每日结果对应 `.meta.json` 文件

在每个 `.parquet` 文件处理完后，自动保存对应的元信息，包括：

* `airport`
* `date`
* `taxi_in_count`
* `avg_taxi_in_duration_min`
* `total_duration_min`
* `source_file`

👉 保存在：

```
./results_hub/meta/{airport}/{month}/xxx_meta.json
```

---

## ✅ 2. 日志系统 Logging（替代 print）

输出处理过程到：

```
./results_hub/processing.log
```

---

## ✅ 🚀 **最终代码（增强版）**

```python
import pandas as pd
import os
import json
import logging
from datetime import datetime

# ---------- 参数配置 ----------
base_folder = '../01_raw_data/HUB_data_2024'
output_folder = './results_hub'
max_gap_seconds = 600

# ---------- 日志设置 ----------
os.makedirs(output_folder, exist_ok=True)
log_file = os.path.join(output_folder, 'processing.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

results = []
all_taxi_in_events = []

# ---------- Taxi-in 分析函数 ----------
def analyze_taxi_in_groundspeed(df, airport, date_str, max_gap_seconds=600):
    df = df.dropna(subset=['icao24', 'timestamp', 'onground', 'groundspeed', 'latitude', 'longitude'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    taxi_in_records = []

    for icao, group in df.groupby('icao24'):
        group = group.sort_values('timestamp').reset_index(drop=True)

        in_taxi_in = False
        start_time = None
        trajectory = []
        last_ts = None

        if group.iloc[0]['onground'] and group.iloc[0]['groundspeed'] > 5:
            in_taxi_in = True
            start_time = group.iloc[0]['timestamp']
            trajectory = [group.iloc[0].to_dict()]
            last_ts = group.iloc[0]['timestamp']

        for i in range(1, len(group)):
            row = group.iloc[i]
            prev_row = group.iloc[i - 1]

            ts = row['timestamp']
            og_now = row['onground']
            og_prev = prev_row['onground']
            gs = row['groundspeed']

            if not in_taxi_in and not og_prev and og_now and gs > 5:
                in_taxi_in = True
                start_time = ts
                trajectory = [row.to_dict()]
                last_ts = ts
                continue

            if in_taxi_in:
                time_gap = (ts - last_ts).total_seconds() if last_ts else 0
                if time_gap > max_gap_seconds:
                    end_time = last_ts
                    taxi_in_records.append({
                        'airport': airport,
                        'icao24': icao,
                        'callsign': trajectory[0].get('callsign', ''),
                        'start': start_time,
                        'end': end_time,
                        'duration_min': round((end_time - start_time).total_seconds() / 60, 2),
                        'trajectory': trajectory,
                        'date': date_str
                    })
                    in_taxi_in = False
                    trajectory = []
                    continue

                if gs > 5:
                    trajectory.append(row.to_dict())
                    last_ts = ts

                if not og_now:
                    end_time = ts
                    taxi_in_records.append({
                        'airport': airport,
                        'icao24': icao,
                        'callsign': trajectory[0].get('callsign', ''),
                        'start': start_time,
                        'end': end_time,
                        'duration_min': round((end_time - start_time).total_seconds() / 60, 2),
                        'trajectory': trajectory,
                        'date': date_str
                    })
                    in_taxi_in = False
                    trajectory = []

        if in_taxi_in and trajectory:
            end_time = group.iloc[-1]['timestamp']
            taxi_in_records.append({
                'airport': airport,
                'icao24': icao,
                'callsign': trajectory[0].get('callsign', ''),
                'start': start_time,
                'end': end_time,
                'duration_min': round((end_time - start_time).total_seconds() / 60, 2),
                'trajectory': trajectory,
                'date': date_str
            })

    result_df = pd.DataFrame(taxi_in_records)
    summary = {
        'airport': airport,
        'date': date_str,
        'taxi_in_count': result_df.shape[0],
        'avg_taxi_in_duration_min': round(result_df['duration_min'].mean(), 2) if not result_df.empty else 0,
        'total_duration_min': round(result_df['duration_min'].sum(), 2)
    }

    return summary, result_df


# ---------- 批量处理 ----------
for airport in sorted(os.listdir(base_folder)):
    airport_path = os.path.join(base_folder, airport)
    if not os.path.isdir(airport_path):
        continue

    for month_folder in sorted(os.listdir(airport_path)):
        month_path = os.path.join(airport_path, month_folder)
        if not os.path.isdir(month_path):
            continue

        for file in sorted(os.listdir(month_path)):
            if file.endswith('.parquet'):
                file_path = os.path.join(month_path, file)
                date_str = file.replace('.parquet', '').split('_')[-1]
                month_str = month_folder  # e.g., 2024-03

                try:
                    logging.info(f"Processing {airport}/{month_str}/{file}")
                    df = pd.read_parquet(file_path)

                    summary, taxiin_df = analyze_taxi_in_groundspeed(df, airport, date_str, max_gap_seconds)

                    results.append(summary)
                    all_taxi_in_events.append(taxiin_df)

                    # 保存 meta 信息
                    meta_folder = os.path.join(output_folder, 'meta', airport, month_str)
                    os.makedirs(meta_folder, exist_ok=True)

                    meta_path = os.path.join(meta_folder, f"{file.replace('.parquet', '')}_meta.json")
                    summary['source_file'] = file
                    with open(meta_path, 'w') as f:
                        json.dump(summary, f, indent=2, default=str)

                except Exception as e:
                    logging.error(f"❌ Failed to process {file_path}: {e}")

# ---------- 最终保存 ----------
summary_df = pd.DataFrame(results)
events_df = pd.concat(all_taxi_in_events, ignore_index=True)

summary_df.to_csv(os.path.join(output_folder, 'summary.csv'), index=False)
events_df.to_json(os.path.join(output_folder, 'all_events.jsonl'), orient='records', lines=True)

logging.info("✅ All processing completed.")
print("🚀 所有机场处理完成，日志与 meta 信息已生成！")
```

---

## 🧾 输出结构示意

```
results_hub/
├── summary.csv
├── all_events.jsonl
├── processing.log
└── meta/
    └── BRU/
        └── 2024-03/
            ├── BRU_2024-03-01_meta.json
            ├── BRU_2024-03-02_meta.json
            └── ...
```

---

如需将这些 meta 信息进一步与每日事件数据一一对应输出成 `.parquet` 或 `.json` 文件，也可以继续扩展。如果你需要，我可以再帮你加上。
