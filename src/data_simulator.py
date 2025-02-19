import boto3
import json
import random
import time
from decimal import Decimal
from datetime import datetime, timedelta

s3 = boto3.client('s3')
BUCKET = 'my-s3-energy-data-bucket'
SITES = ['site_1', 'site_2', 'site_3']
WEATHER_CONDITIONS = ['sunny', 'cloudy', 'rainy', 'stormy']


def generate_data():
    # Simulate realistic energy data with occasional anomalies
    energy_generated = Decimal(random.uniform(0, 100)).quantize(Decimal('0.00'))
    energy_consumed = Decimal(random.uniform(0, 100)).quantize(Decimal('0.00'))

    # Introduce a 5% chance of generating negative values for anomalies
    if random.random() < 0.05:
        energy_generated = Decimal(random.uniform(-10, 0)).quantize(Decimal('0.00'))  # Negative generation
    if random.random() < 0.05:
        energy_consumed = Decimal(random.uniform(-5, 0)).quantize(Decimal('0.00'))  # Negative consumption

    return {
        'site_id': random.choice(SITES),
        'timestamp': (datetime.utcnow() - timedelta(days=random.randint(0, 21))).isoformat(),
        'energy_generated_kwh': str(energy_generated),
        'energy_consumed_kwh': str(energy_consumed),
        'temperature_c': random.randint(10, 35),  # Temperature in Celsius
        'humidity_percent': random.randint(30, 90),  # Humidity in percentage
        'weather_condition': random.choice(WEATHER_CONDITIONS)  # Random weather condition
    }

while True:
    data = [generate_data() for _ in range(100)]  # 100 records per file
    file_name = f"energy_data_{datetime.utcnow().isoformat()}.json"
    s3.put_object(Bucket=BUCKET, Key=file_name, Body=json.dumps(data))
    print(f'New file added: {file_name}...')

    minutes_wait = 1
    for min in range(minutes_wait):
        time.sleep(60)
        print(f'{min + 1}min(s) passed...')