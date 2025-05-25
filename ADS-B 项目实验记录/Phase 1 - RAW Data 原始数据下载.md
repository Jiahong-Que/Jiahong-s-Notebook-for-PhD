# Phase 1 - RAW Data 原始数据下载

以下是 ADS-B 项目中 **第一部分：原始数据下载** 的文字描述整理，适用于技术文档、报告或博客说明：

---

## ✈️ ADS-B 项目第一部分：原始数据下载

本部分负责从 OpenSky Network 自动化下载 2024 年全年指定机场范围内的 ADS-B 原始历史数据，并进行本地保存与失败重试机制处理。

### 🔧 日志系统初始化

为了记录整个数据下载流程中的运行状态，设置了日志记录模块 `logging`，日志文件保存为 `adsb_download.log`，用于记录每个机场每天数据下载的结果，包括成功、失败或数据为空的情况。

---

### ✈️ 支持的机场信息

定义了 11 个欧洲主要机场（如 Frankfurt, Amsterdam, Heathrow 等）的三字码、名称和地理坐标（纬度、经度），用于设定抓取的空间边界。

---

### 📅 数据时间范围

* 下载时间段为：**2024年1月1日 至 2024年12月31日**
* 采用逐天下载的方式，遍历全年 366 天数据（含闰年）

---

### 🌐 空间抓取范围

* 抓取半径设定为：**6 公里**
* 根据机场中心坐标，换算成纬度与经度方向的矩形边界（西、东、南、北）

---

### 📦 下载流程说明

#### 1. 遍历日期

对每个机场，逐日下载对应边界内的数据。

#### 2. 数据下载

调用 `traffic.data.opensky.history()` 获取指定时间和空间范围内的历史轨迹数据。

#### 3. 本地保存

* 保存数据为 `.parquet` 文件，结构清晰、压缩率高
* 同步生成 `.json` 格式的元数据文件，记录：

  * 机场信息
  * 抓取时间与边界
  * 数据量统计
  * 下载状态（成功/失败/无数据）

#### 4. 跳过重复

若对应日期的文件已存在，则自动跳过，避免重复抓取。

#### 5. 下载失败处理

* 对失败日期记录日志并保存至 `failed_days.csv`
* 所有下载完成后，对失败日期进行 **自动重试**

---

### 🔁 自动重试机制

程序会检查是否存在 `failed_days.csv` 文件，对于之前下载失败的日期，重新调用下载函数并保存结果为 `retry_failed_days.csv`。

---

### 📊 汇总与输出

* 所有机场的下载汇总统计（总天数、失败天数、数据行数）将输出为 `airport_download_summary.csv` 文件
* 提供总览每个机场下载状态的概况

---

### 📁 文件结构示意

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

### ✅ 成果总结

* 支持对多个机场的全年度 ADS-B 数据抓取
* 自动构建目录、保存数据和元信息
* 支持失败重试与日志记录，保证数据完整性和可追溯性
* 可作为后续数据清洗与建模的原始输入

![XCR_record_count](https://github.com/user-attachments/assets/5f001575-4190-4833-81aa-074804005522)
![WAW_record_count](https://github.com/user-attachments/assets/76ff842b-9699-4c3f-bca9-c920ce7d2959)
![LUX_record_count](https://github.com/user-attachments/assets/c191d6e6-0ef3-4d9c-840e-1936151d170a)
![LHR_record_count](https://github.com/user-attachments/assets/ada3e7ef-6cd0-471c-b598-69ba64fd99b8)
![LEJ_record_count](https://github.com/user-attachments/assets/94f91fa6-2e14-4e18-b7f7-cc3c32ce21e5)
![IST_record_count](https://github.com/user-attachments/assets/f44a4759-f1af-4485-aaad-8185b00c3c9d)
![FRA_record_count](https://github.com/user-attachments/assets/55c6a781-885c-4285-beb0-e13a5661afd0)
![CGN_record_count](https://github.com/user-attachments/assets/dfef5bfa-b630-4376-bd62-08a28b1783d3)
![BUD_record_count](https://github.com/user-attachments/assets/c879c4ce-285a-4a0a-88db-3086b3fc3830)
![BRU_record_count](https://github.com/user-attachments/assets/89a58f2c-b39c-4647-b637-9a7ad0ff00cd)
![AMS_record_count](https://github.com/user-attachments/assets/27a0316a-8aa9-46f8-8f76-25d3c8c251cd)
![all_airports_record_count_comparison](https://github.com/user-attachments/assets/a03ac44d-8b93-4ec3-9a6a-260f7242eeea)

