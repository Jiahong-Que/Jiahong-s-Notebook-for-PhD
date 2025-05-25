# Phase 1 - RAW Data Downloading

## ✈️ ADS-B Project – Part 1: Raw Data Download

This module handles the automated download of historical ADS-B data for the year 2024 from the OpenSky Network, focusing on selected European airports. The script includes mechanisms for logging, data storage, and automatic retry for failed downloads.

---

### 🔧 Logging System Initialization

To monitor and track the download process, a logging system is initialized. All messages are recorded in the `adsb_download.log` file, documenting the status of each download task — including success, failure, and cases with no data found.

---

### ✈️ Airport Information

The script includes information for **11 major European airports**, such as Frankfurt, Amsterdam, and Heathrow. Each airport is defined with:

* ICAO code
* Name
* Latitude and longitude

These coordinates are used to define the geographic boundaries for downloading data.

---

### 📅 Time Range

* **Period:** January 1, 2024 to December 31, 2024
* The script processes **one day at a time**, covering all 366 days (leap year included)

---

### 🌐 Spatial Query Radius

* **Radius:** 6 km
* This defines a rectangular bounding box (west, east, south, north) around each airport based on the center coordinates, used to fetch only the local data.

---

### 📦 Data Download Process

#### 1. Iterate Over Dates

For each airport, the script loops through every day in the target year.

#### 2. Download Data

It uses the `opensky.history()` function from the `traffic` Python package to retrieve trajectory data within the specified time and spatial bounds.

#### 3. Local Storage

* Data is saved as `.parquet` files for efficient storage and processing.
* Metadata is stored in `.json` files, containing:

  * Airport details
  * Time range and bounding box
  * Download status (success/empty/error)
  * Number of records

#### 4. Skip Existing Files

If the `.parquet` file for a date already exists, the script skips the download to prevent redundancy.

#### 5. Failure Handling

Failed downloads are logged and the failed dates are stored in a `failed_days.csv` file for future retry.

---

### 🔁 Automatic Retry

After the initial download pass, the script checks for failed dates. It retries these dates automatically and saves the results in a separate `retry_failed_days.csv` file.

---

### 📊 Summary Output

At the end of the process:

* A summary table is generated, listing each airport’s:

  * Total number of days processed
  * Number of failed days
  * Total number of rows (records) downloaded
* This summary is saved to a file named `airport_download_summary.csv`

---

### 📁 Directory Structure Example

```
data_2024/
  └── FRA/
        ├── 2024-01/
        │     ├── FRA_2024-01-01.parquet
        │     └── FRA_2024-01-01_meta.json
        └── failed_days.csv
airport_download_summary.csv
adsb_download.log
```

---

### ✅ Key Outcomes

* Supports full-year ADS-B data download for multiple airports
* Automatically manages directory creation, data saving, and metadata logging
* Includes robust retry and logging mechanisms to ensure completeness and traceability
* Provides clean, organized input for downstream data processing and modeling

