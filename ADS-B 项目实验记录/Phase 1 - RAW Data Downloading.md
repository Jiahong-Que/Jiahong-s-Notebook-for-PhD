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


![XCR_record_count](https://github.com/user-attachments/assets/dfc29580-6cf7-46f5-b45b-3e5ff7be6b5a)
![WAW_record_count](https://github.com/user-attachments/assets/1d0d6b9b-65bb-4e92-a520-1a2d9a2932b9)
![LUX_record_count](https://github.com/user-attachments/assets/58247620-0a66-4484-9d2e-c92a82736027)
![LHR_record_count](https://github.com/user-attachments/assets/8ccd7f07-3654-421a-bf76-5170b68d9718)
![LEJ_record_count](https://github.com/user-attachments/assets/f54b60f8-9b5e-4e2b-bffc-8d4fdc790c80)
![IST_record_count](https://github.com/user-attachments/assets/1f25b1ac-4de1-44d7-879e-86d8a065b9a3)
![FRA_record_count](https://github.com/user-attachments/assets/ffb313e0-e89c-4ec5-ab0f-d5a9278ac265)
![CGN_record_count](https://github.com/user-attachments/assets/1de6c9a1-3b23-4572-a6fa-b7a226741185)
![BUD_record_count](https://github.com/user-attachments/assets/7baee4ad-1f30-41a8-af46-a5037679685f)
![BRU_record_count](https://github.com/user-attachments/assets/7da0bb40-ba1d-4288-8e04-ba154c8bbc15)
![AMS_record_count](https://github.com/user-attachments/assets/890dfc86-86c2-4102-ad65-fb7e3371280c)
![all_airports_record_count_comparison](https://github.com/user-attachments/assets/30e6ce22-3cf4-4a6e-9996-d0de64656a91)


