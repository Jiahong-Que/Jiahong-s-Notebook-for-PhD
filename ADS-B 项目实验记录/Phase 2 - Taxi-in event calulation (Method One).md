
## 🧪 Experiment Purpose

This script is designed to **identify and extract taxi-in events** from ADS-B data of aircraft at Frankfurt Airport (FRA). A taxi-in event refers to the ground movement of an aircraft from the runway to the gate after landing. The analysis is based on the change in the `onground` status and a reasonable `groundspeed` threshold (> 5 knots). The result includes detailed taxi-in trajectories, start and end timestamps, durations, and summary statistics for each day.

---

## 🧱 Code Structure and Workflow

### 1. 📂 Initial Setup

```python
data_folder = '../data/adsb_data_fra_2024_678'
max_gap_seconds = 600
```

* **Data folder** contains one CSV file per day with raw ADS-B messages.
* **`max_gap_seconds`** is a threshold for determining if a gap between two ground movement data points is too long (10 minutes). If exceeded, the taxi-in event is considered ended.

---

### 2. 📦 Core Function: `analyze_taxi_in_groundspeed(df, date_str, max_gap_seconds=600)`

This function performs the analysis for a single day.

#### 🔍 Step 1: Data Preprocessing

```python
df = df.dropna(...)
df['timestamp'] = pd.to_datetime(...)
```

* Drops rows with missing values in critical fields.
* Converts the `timestamp` to datetime format.

#### 🔄 Step 2: Group by Aircraft (`icao24`)

```python
for icao, group in df.groupby('icao24'):
```

* Iterates through each unique aircraft ID.
* Sorts each group by timestamp.

#### ✈️ Step 3: Taxi-in Detection Logic

The key logic detects the start and end of a taxi-in event:

```python
if not in_taxi_in and not og_prev and og_now and gs > 5:
    # Start of taxi-in
elif in_taxi_in:
    if time_gap > max_gap_seconds:
        # End due to time gap
    elif gs > 5:
        # Continue taxiing
    elif not og_now:
        # Early termination
```

* A taxi-in event **starts** when the `onground` flag switches from `False` to `True` and the groundspeed is above 5 knots.
* The event **ends** if:

  * There is a gap > 600 seconds between data points,
  * The groundspeed drops or the `onground` becomes `False` again (e.g., due to takeoff misdetection).

#### 📝 Step 4: Save Detected Taxi-in Segments

Each segment is stored as:

```json
{
  "icao24": "...",
  "callsign": "...",
  "start": "...",
  "end": "...",
  "duration_min": ...,
  "trajectory": [point1, point2, ...]
}
```

* Includes full trajectory, start and end time, duration in minutes, and the aircraft's callsign.

#### 📊 Step 5: Daily Summary

At the end of each day’s analysis, a summary dictionary is generated:

```python
summary = {
    'date': date_str,
    'taxi_in_count': ...,
    'avg_taxi_in_duration_min': ...,
    'total_duration_min': ...
}
```

---

### 3. 🔁 Batch Processing of Daily Files

```python
for file in file_list:
    ...
    df = pd.read_csv(file_path)
    summary, taxiin_df = analyze_taxi_in_groundspeed(...)
```

* Loops through all CSV files in the folder.
* Calls the analysis function for each file (representing a day).
* Aggregates both the per-day summary and detailed taxi-in events.

---

### 4. 💾 Save Results

```python
summary_df.to_csv(...)   # Daily statistics
events_df.to_json(...)   # All taxi-in events with trajectories
events_df.to_csv(...)    # All taxi-in events without trajectories
```

* **`daily_taxi_in_summary_...csv`**: Contains a summary for each day.
* **`all_taxi_in_events_with_trajectory_...json`**: Detailed taxi-in segments including the full trajectory (useful for visualization).
* **`all_taxi_in_events_no_trajectory_...csv`**: Simplified event list without full trajectories.

---

## ✅ Experiment Output

* Successfully extracted **taxi-in segments** for each aircraft.
* Saved:

  * Taxi-in **events with trajectories**,
  * **Summaries** of taxi-in counts and durations.
* These can be used for further studies on ground operations, delays, and airport efficiency.

---

## 💡 Remarks (Optional for your report)

* The threshold for `groundspeed > 5` can be fine-tuned based on actual taxi speed distributions.
* This logic can be extended to include:

  * Runway detection (using latitude/longitude),
  * Gate assignment or terminal-level analysis.
* The trajectory data can be visualized using `folium` or `matplotlib` for geographical plots.


