import pandas as pd
import os
from datetime import datetime

# 参数设置
data_folder = '../data/adsb_data_fra_2024_678'  # 存放每天csv数据的文件夹
max_gap_seconds = 600  # 两条记录间最大允许间隔（秒）

# 保存分析结果
results = []
all_taxi_in_events = []

# 创建结果文件夹
os.makedirs('./results', exist_ok=True)

# 核心分析函数（改进后的版本）
def analyze_taxi_in_groundspeed(df, date_str, max_gap_seconds=600):
    # 数据预处理
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

        # 初始判断：是否一开始就在 taxi-in 中
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

            # 检测 onground 从 False 变 True 且速度合理 => taxi-in 开始
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
                        'icao24': icao,
                        'callsign': trajectory[0].get('callsign', ''),
                        'start': start_time,
                        'end': end_time,
                        'duration_min': round((end_time - start_time).total_seconds() / 60, 2),
                        'trajectory': trajectory
                    })
                    in_taxi_in = False
                    trajectory = []
                    continue

                if gs > 5:
                    trajectory.append(row.to_dict())
                    last_ts = ts

                # onground 变为 False（可能是误报起飞），提前终止
                if not og_now:
                    end_time = ts
                    taxi_in_records.append({
                        'icao24': icao,
                        'callsign': trajectory[0].get('callsign', ''),
                        'start': start_time,
                        'end': end_time,
                        'duration_min': round((end_time - start_time).total_seconds() / 60, 2),
                        'trajectory': trajectory
                    })
                    in_taxi_in = False
                    trajectory = []

        # 收尾处理
        if in_taxi_in and trajectory:
            end_time = group.iloc[-1]['timestamp']
            taxi_in_records.append({
                'icao24': icao,
                'callsign': trajectory[0].get('callsign', ''),
                'start': start_time,
                'end': end_time,
                'duration_min': round((end_time - start_time).total_seconds() / 60, 2),
                'trajectory': trajectory
            })

    result_df = pd.DataFrame(taxi_in_records)
    result_df['date'] = date_str
    result_df['count'] = 1

    summary = {
        'date': date_str,
        'taxi_in_count': result_df.shape[0],
        'avg_taxi_in_duration_min': round(result_df['duration_min'].mean(), 2) if not result_df.empty else 0,
        'total_duration_min': round(result_df['duration_min'].sum(), 2)
    }

    return summary, result_df

# 主程序：批量处理所有文件
file_list = sorted([f for f in os.listdir(data_folder) if f.endswith('.csv')])

for file in file_list:
    print(f"📦 正在处理文件: {file}")
    date_str = file.replace('.csv', '')
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)

    summary, taxiin_df = analyze_taxi_in_groundspeed(df, date_str, max_gap_seconds=max_gap_seconds)
    results.append(summary)
    all_taxi_in_events.append(taxiin_df)

# 保存结果
summary_df = pd.DataFrame(results)
events_df = pd.concat(all_taxi_in_events, ignore_index=True)

summary_df.to_csv('./results/daily_taxi_in_summary_from_onground_change_callsign_v_678.csv', index=False)
events_df.to_json('./results/all_taxi_in_events_with_trajectory_callsign_v_678.json', orient='records', lines=True)
events_df.drop(columns=['trajectory'], inplace=True)
events_df.to_csv('./results/all_taxi_in_events_no_trajectory_callsign_v_678.csv', index=False)



print("✅ 基于 onground 转变识别 taxi-in，滑行轨迹数据提取完毕，已包含 callsign！")
