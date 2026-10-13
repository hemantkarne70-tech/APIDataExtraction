# 🚀 APIDataExtraction

**A Python-based API Data Extraction, ETL, and Database Ingestion Framework**

APIDataExtraction is a Python-based data ingestion project designed to fetch data from API endpoints, process and clean the extracted records, and ingest the data into a Neo4j database. It also supports Excel-based ingestion, making it possible to process previously downloaded datasets without calling the API again.

The project supports routine data ingestion, calendar event date management, local Excel data storage, logging, and recovery of missing historical records for specific dates or date ranges.

---

## ✨ Key Features

- 🌐 **API Data Extraction** — Fetch data from configured API endpoints.
- 🔄 **ETL Pipeline** — Extract, clean, transform, and prepare records for ingestion.
- 🗄️ **Neo4j Integration** — Ingest processed records into a Neo4j database.
- 📊 **Excel Support** — Process Excel files as an alternative to fetching data directly from an API.
- 📅 **Calendar Event Management** — Insert calendar event date entries into Neo4j during ingestion.
- 🎯 **Date-Specific Processing** — Support calendar event entries for specific dates.
- 🕰️ **Historical Data Recovery** — Fetch and ingest missing records for particular dates or date ranges.
- 📝 **Logging** — Maintain execution logs to help monitor ingestion runs and troubleshoot failures.
- ⚙️ **Centralized Configuration** — Manage database settings, API configuration, and file paths in a dedicated configuration module.

---

## 🏗️ Project Structure

```text
APIDataExtraction/
│
├── Config.py
├── Logger.py
├── CalendarEvent.py
├── CalendarEvent_SpecificDate.py
├── getapidata.py
├── fetchold_apidata.py
├── README.md
└── .gitignore
```

---

## 📂 File Descriptions

| File | Description |
|---|---|
| `Config.py` | Centralized configuration for database credentials, API settings, and directory paths. |
| `Logger.py` | Provides logging functionality for recording execution details, errors, and ingestion activities. |
| `CalendarEvent.py` | Handles the insertion of calendar event date entries into Neo4j as part of the ingestion process. |
| `CalendarEvent_SpecificDate.py` | Handles calendar event date entry processing for a specified date. |
| `getapidata.py` | Main ingestion script responsible for API fetching, data cleaning, date processing, ETL, database ingestion, and local Excel storage. Also supports ingestion from existing Excel files. |
| `fetchold_apidata.py` | Supports historical or backfill ingestion for missing records associated with a specific date or date range. Uses the same general ingestion workflow as the main script. |

---

## 🔄 Data Ingestion Workflow

The project follows an ETL-oriented workflow to process API or Excel data.

```text
        API Endpoint / Excel Files
                   |
                   v
          Data Extraction
                   |
                   v
          Data Cleaning
                   |
                   v
       Date Processing & Splitting
                   |
                   v
           Data Transformation
                   |
                   v
           Processed Records
              /         \
             v           v
     Neo4j Database   Local Excel Files
             |
             v
      Ingestion Logging
```

*Note: The diagram represents the overall workflow. Exact processing order and output behavior depend on the implementation of the individual scripts.*

---

## ⚙️ Configuration

The `Config.py` module centralizes the settings required by the ingestion scripts.

Typical configuration categories include:

- Database connection settings
- API base URLs and endpoint configuration
- API authentication settings, where applicable
- Input and output directory paths
- Excel file locations
- Logging configuration, if configured in the project

---

## 🛠️ Installation and Setup

### Prerequisites

Before running the project, ensure that the following are available:

- Python 3
- Git
- Neo4j database access
- Valid API endpoint and required authentication, if applicable
- Required Python packages
- Access to the configured input and output directories

### 1. Clone the repository

```bash
git clone https://github.com/hemantkarne70-tech/APIDataExtraction.git
cd APIDataExtraction
```

### 2. Create a virtual environment

**Windows — Git Bash or PowerShell**

```bash
python -m venv .venv
```

Activate the environment in Git Bash:

```bash
source .venv/Scripts/activate
```

Or activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / Ubuntu**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the Python packages required by the project.

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

If one is not available, create it based on the imports and dependency versions used by the project.

### 4. Configure the application

Review `Config.py` and configure the required database connection, API endpoint, and input/output paths. Ensure that sensitive credentials are provided securely.

### 5. Execute the appropriate script

Use the main ingestion script for routine data processing, or the historical ingestion script when backfilling missing records.

The exact arguments and execution options depend on how the scripts are implemented.

---

## 📅 Available Ingestion Modes

### 1. Routine Data Ingestion

**Script:** `getapidata.py`

Use this script for the regular ingestion workflow. It supports:

- Fetching data from a configured API endpoint.
- Cleaning and transforming the extracted records.
- Processing and splitting date information as required.
- Ingesting processed records into Neo4j.
- Saving data locally in Excel format.
- Processing existing Excel data when API fetching is not required.

### 2. Calendar Event Date Ingestion

**Script:** `CalendarEvent.py`

Used to insert calendar event date entries into Neo4j during the ingestion process.

### 3. Specific-Date Calendar Event Processing

**Script:** `CalendarEvent_SpecificDate.py`

Used when calendar event entries need to be processed for a particular date.

### 4. Historical Data Backfill

**Script:** `fetchold_apidata.py`

Used to retrieve and ingest missing historical records for a specific date or date range.

This supports recovery and backfilling without changing the purpose of the routine ingestion script.

---

## 📊 Data Storage

The project uses two primary data destinations:

| Destination | Purpose |
|---|---|
| Neo4j | Stores ingested records for database access and downstream processing. |
| Local Excel files | Maintains local copies of extracted or processed data for reuse and offline ingestion. |

The availability and exact behavior of these destinations depend on the selected ingestion mode and the implementation of the scripts.

---

## 📝 Logging and Troubleshooting

The `Logger.py` module provides logging support for the ingestion process.

Logs can help with:

- Tracking script execution.
- Identifying data extraction or transformation errors.
- Investigating database ingestion failures.
- Reviewing the execution of historical data backfills.
- Diagnosing issues during data processing.

Review the configured log output when troubleshooting failed runs. Avoid writing passwords, API tokens, or other sensitive information into logs.

---

## 👨‍💻 Author

**Hemant Karne**

Software Engineer | Python | Data Engineering | API Integration | Neo4j | Elasticsearch

GitHub: [@hemantkarne70-tech](https://github.com/hemantkarne70-tech)

---

## 📄 License

A license has not yet been specified. Add a suitable license file if you intend to distribute or reuse this project under explicit licensing terms.

---

*APIDataExtraction — Extract, transform, ingest, and manage data through a reusable Python-based workflow.*
