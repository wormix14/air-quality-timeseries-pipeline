import os
from azure.identity import AzureCliCredential
from deltalake import DeltaTable
import pandas as pd
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def run_pipeline():
    os.makedirs("data", exist_ok=True)
    path = os.getenv("FABRIC_DELTA_TABLE_PATH")

    client = influxdb_client.InfluxDBClient(
    url=os.getenv("INFLUXDB_URL"),
    token=os.getenv("INFLUXDB_TOKEN"),
    org=os.getenv("INFLUXDB_ORG")
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    try:
        if not path:
            raise ValueError("FABRIC_DELTA_TABLE_PATH is not set")
        
        token = (
            AzureCliCredential().get_token("https://storage.azure.com/.default").token
        )

        df = DeltaTable(
            path, storage_options={"bearer_token": token, "use_fabric_endpoint": "true"}
        ).to_pandas()

        df.to_parquet("data/fact_air_quality_daily.parquet", index=False)
        
    except Exception as e:
        print(f"Fabric unavailable ({e}), using local parquet.", flush=True)
        df = pd.read_parquet("data/fact_air_quality_daily.parquet")


    points =  []
    for row in df.itertuples(index=False):
        if pd.notna(row.borough) and pd.notna(row.date):
            point = (influxdb_client.Point(
                "air-quality")
                .tag("borough", str(row.borough))
                .time(pd.to_datetime(row.date, utc=True))
                )
            if pd.notna(row.pm25):
                point.field("pm25", float(row.pm25))
            if pd.notna(row.o3):
                point.field("o3", float(row.o3))
            if pd.notna(row.temperature):
                point.field("temperature", float(row.temperature))

            if point._fields:
                points.append(point)
    try:
        if points:
            write_api.write(bucket=os.getenv("INFLUXDB_BUCKET"), org=os.getenv("INFLUXDB_ORG"), record=points)
    finally:
        client.close()
