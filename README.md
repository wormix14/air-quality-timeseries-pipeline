# Fabric to InfluxDB Air Quality Pipeline

Automated ETL pipeline that extracts air quality metrics (`pm25`, `o3`, `temperature` by `borough`) from a Microsoft Fabric OneLake Delta table and loads time-series points into InfluxDB on a 10-minute schedule.

## Tech Stack
- **Storage:** Microsoft Fabric OneLake (`deltalake`, `azure-identity`), Parquet (`pandas`, `pyarrow`)
- **Time-Series Database:** InfluxDB (`influxdb-client`)
- `APScheduler` library in Python

## Setup & Usage

1. **Create .env:**
   ```bash
   cd air-quality-timeseries-pipeline
   cp .env.example .env
2. **Enter InfluxDB Keys in .env**

   You don't need to enter Fabric path, because you have parquet file locally in **data/** 

4. **Build and start the containers:**
   ```bash
   docker compose up --build -d
   ```
4.**Access services locally**

InfluxDB: http://localhost:8086

Grafana: http://localhost:3000
