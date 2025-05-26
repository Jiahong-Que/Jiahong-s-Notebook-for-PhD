实现一个 **基于 ADS-B 数据分析飞机 taxi-in 滑行阶段（落地后滑行至停机位）** 的完整流程，并提取了详细的滑行事件数据与统计摘要。

以下是对**功能结构和逻辑的详细分析**，可以作为实验记录：

---

## 🧪 实验目的

识别并提取飞机落地后的 **taxi-in 滑行阶段**，通过分析 `onground` 状态从 `False` 到 `True` 的变化，并结合 `groundspeed > 5` 的条件进行判断，记录每一段滑行轨迹的起止时间、持续时长、callsign 等信息，并输出分析汇总结果。

---

## 🧱 实验步骤与代码结构

### 1. 📂 初始设置

```python
data_folder = '../data/adsb_data_fra_2024_678'
max_gap_seconds = 600
```

* 指定数据文件夹：包含每日的 CSV 格式 ADS-B 数据文件（每个文件一整天）。
* 设置最大滑行时间间隔：用于判断滑行中断的时间阈值（10分钟内连续滑行数据才被视作一段）。

---

### 2. 📦 主函数 `analyze_taxi_in_groundspeed(df, date_str, max_gap_seconds=600)`

对某一天的数据（DataFrame）进行如下处理：

#### 🔍 Step 1: 数据预处理

```python
df = df.dropna(...)
df['timestamp'] = pd.to_datetime(...)
```

* 移除缺失的关键字段：如 `icao24`、`timestamp`、`onground`、`groundspeed`。
* 转换 `timestamp` 字段为标准时间格式。

#### 🔄 Step 2: 按照 `icao24` 分组处理每一架飞机

```python
for icao, group in df.groupby('icao24'):
```

* 遍历每一架飞机的记录，按时间排序。

#### ✈️ Step 3: 滑行状态识别逻辑

```python
if not in_taxi_in and not og_prev and og_now and gs > 5:
    # taxi-in 开始
elif in_taxi_in:
    if time_gap > max_gap_seconds:
        # 滑行中断，记录结束
    elif gs > 5:
        # 继续滑行
    elif not og_now:
        # 滑行意外终止（例如短时间起飞判断错误）
```

* 当 `onground` 从 False → True，且速度 > 5，认为是 **taxi-in 开始**。
* 如果两个数据点之间时间差超过设定阈值（10分钟），则判断为 **滑行中断**，记录结束。
* 滑行过程中一旦 `onground` 变为 False，认为是数据误判或起飞，提前终止滑行。

#### 📝 Step 4: 保存滑行事件

每段滑行记录保存为：

```json
{
  "icao24": "...",
  "callsign": "...",
  "start": "...",
  "end": "...",
  "duration_min": ...,
  "trajectory": [dict, dict, ...]
}
```

* 包含起止时间、持续时间（分钟）、callsign、所有点的轨迹数据。

#### 📊 Step 5: 生成统计摘要

```python
summary = {
    'date': date_str,
    'taxi_in_count': ...,
    'avg_taxi_in_duration_min': ...,
    'total_duration_min': ...
}
```

* 提取该日的统计数据：滑行次数、平均滑行时间、总滑行时间。

---

### 3. 🔁 批处理多个日期的数据文件

```python
for file in file_list:
    ...
    df = pd.read_csv(file_path)
    summary, taxiin_df = analyze_taxi_in_groundspeed(...)
```

* 遍历文件夹中所有 `.csv` 文件（按日期命名）。
* 分别调用分析函数处理每一天的数据。
* 累计汇总结果：`summary` 用于统计，`taxiin_df` 存储所有滑行段详细数据。

---

### 4. 💾 保存结果到本地

```python
summary_df.to_csv(...)  # 每日统计汇总
events_df.to_json(...)  # 所有滑行事件，含轨迹
events_df.to_csv(...)   # 所有滑行事件，不含轨迹
```

* 保存三个结果文件：

  1. `daily_taxi_in_summary_...csv`：每一天的滑行统计。
  2. `all_taxi_in_events_with_trajectory_...json`：含完整轨迹的滑行事件（适合分析）。
  3. `all_taxi_in_events_no_trajectory_...csv`：不含轨迹，适合概览统计。

---

## ✅ 实验结果

* 成功提取了 **每架飞机的 taxi-in 滑行段**。
* 提供了 **统计摘要**（滑行段数、平均滑行时间等）。
* 为后续建模、聚类、可视化等分析准备了结构化数据。

---

## 💡 总结建议（可选添加到实验记录中）

* 本算法假设滑行速度应大于 5 knots，这一阈值可进一步根据地面运动分析调整。
* 可扩展支持机场跑道识别、停机位匹配等功能。
* 可将 `trajectory` 中的数据用于绘制滑行路径轨迹图（结合地图可视化）。


