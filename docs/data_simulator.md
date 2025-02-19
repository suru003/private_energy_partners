# Energy Data Simulator

## Overview
This Python script simulates a continuous data generation pipeline for renewable energy monitoring, creating realistic energy consumption and generation datasets with occasional anomalies.

## Features
- Generates synthetic energy data for multiple sites
- Introduces random anomalies (negative energy values)
- Uploads data to AWS S3 bucket
- Supports multiple energy sites
- Includes additional contextual data like temperature and weather conditions

## Data Schema
```json
{
  "site_id": "site_1|site_2|site_3",
  "timestamp": "ISO 8601 Timestamp",
  "energy_generated_kwh": "Decimal",
  "energy_consumed_kwh": "Decimal", 
  "temperature_c": "Integer",
  "humidity_percent": "Integer",
  "weather_condition": "sunny|cloudy|rainy|stormy"
}
```

## Anomaly Requirements Simulation
- 5% chance of negative energy generation
- 5% chance of negative energy consumption

## Prerequisites
- Python 3.8+
- `boto3` library
- Configured AWS credentials

## Configuration
- Modify `SITES` to add/remove energy sites
- Adjust generation ranges in `generate_data()`
- Configure S3 bucket name

## Deployment
```bash
python data_simulator.py
```

## Note
Designed for data engineering assessment simulating real-world energy monitoring scenarios.