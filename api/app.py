from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import boto3
from datetime import datetime

app = FastAPI()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EnergyMetrics')

class Record(BaseModel):
    site_id: str
    timestamp: str
    energy_generated_kwh: float
    energy_consumed_kwh: float
    temperature_c: float
    humidity_percent: float
    weather_condition: str
    anomaly: bool

@app.get("/")
def read_root():
    return {"message": "Welcome to the Energy Metrics API"}

# http://127.0.0.1:8000/records/?site_id=site_2&&start_time=2025-02-17&&end_time=2025-02-18
@app.get("/records/", response_model=List[Record])
def get_records(site_id: str, start_time: str, end_time: str):
    # Fetch records for a specific site and time range
    response = table.scan()
    data = response['Items']

    # Filter records based on site_id and time range
    filtered_data = [
        record for record in data
        if record['site_id'] == site_id and start_time <= record['timestamp'] <= end_time
    ]

    return filtered_data

# http://127.0.0.1:8000/anomalies/?site_id=site_2
@app.get("/anomalies/", response_model=List[Record])
def get_anomalies(site_id: str):
    # Retrieve all anomalies for a given site
    response = table.scan()
    data = response['Items']

    anomalies = [
        record for record in data
        if record['site_id'] == site_id and record.get('anomaly', False)
    ]

    return anomalies