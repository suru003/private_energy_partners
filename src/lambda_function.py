import json
import boto3
import logging
from urllib.parse import unquote_plus
from decimal import Decimal
from datetime import datetime
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Constants
TABLE_NAME = 'EnergyMetrics'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:600627349906:Anomaly-Detection-Topic'
ANOMALY_THRESHOLD = {
    'energy_generated_min': 0,
    'energy_consumed_min': 0,
    'temperature_min': -20,
    'temperature_max': 50,
    'humidity_min': 0,
    'humidity_max': 100
}


class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass


def validate_entry(entry):
    """
    Validate the data entry
    Returns tuple (is_valid, error_message)
    """
    required_fields = ['site_id', 'timestamp', 'energy_generated_kwh',
                       'energy_consumed_kwh', 'temperature_c',
                       'humidity_percent', 'weather_condition']

    # Check for required fields
    for field in required_fields:
        if field not in entry:
            raise DataValidationError(f"Missing required field: {field}")

    # Validate numeric values
    try:
        energy_generated = float(entry['energy_generated_kwh'])
        energy_consumed = float(entry['energy_consumed_kwh'])
        temperature = float(entry['temperature_c'])
        humidity = float(entry['humidity_percent'])
    except (ValueError, TypeError) as e:
        raise DataValidationError(f"Invalid numeric value: {str(e)}")

    # Validate ranges
    if temperature < ANOMALY_THRESHOLD['temperature_min'] or temperature > ANOMALY_THRESHOLD['temperature_max']:
        raise DataValidationError(f"Temperature {temperature}°C is outside valid range")

    if humidity < ANOMALY_THRESHOLD['humidity_min'] or humidity > ANOMALY_THRESHOLD['humidity_max']:
        raise DataValidationError(f"Humidity {humidity}% is outside valid range")


def detect_anomalies(entry):
    """
    Detect anomalies in the data entry
    Returns tuple (is_anomaly, anomaly_details)
    """
    anomalies = []

    # Convert values to float for comparison
    energy_generated = float(entry['energy_generated_kwh'])
    energy_consumed = float(entry['energy_consumed_kwh'])
    temperature = float(entry['temperature_c'])
    humidity = float(entry['humidity_percent'])

    # Check for negative energy values
    if energy_generated < ANOMALY_THRESHOLD['energy_generated_min']:
        anomalies.append(f"Negative energy generation: {energy_generated} kWh")
    if energy_consumed < ANOMALY_THRESHOLD['energy_consumed_min']:
        anomalies.append(f"Negative energy consumption: {energy_consumed} kWh")

    # Check for unusual energy patterns
    if energy_generated > 0 and energy_consumed == 0:
        anomalies.append("Energy generation without consumption")
    if energy_generated / energy_consumed > 10 if energy_consumed > 0 else 0:
        anomalies.append("Unusually high generation to consumption ratio")

    # Check for extreme weather conditions
    if temperature > 40 or temperature < -10:
        anomalies.append(f"Extreme temperature: {temperature}°C")
    if humidity > 95 or humidity < 5:
        anomalies.append(f"Extreme humidity: {humidity}%")

    return bool(anomalies), anomalies


def publish_sns_message(message, subject):
    """Publish message to SNS topic"""
    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps(message, indent=2),
            Subject=subject
        )
        logger.info(f"Published message to SNS: {response['MessageId']}")
    except ClientError as e:
        logger.error(f"Failed to publish to SNS: {str(e)}")
        raise


def process_entry(entry, site_metrics):
    """Process a single data entry"""
    # Validate data
    validate_entry(entry)

    # Convert numeric values to Decimal
    energy_generated_kwh = Decimal(str(entry['energy_generated_kwh']))
    energy_consumed_kwh = Decimal(str(entry['energy_consumed_kwh']))
    net_energy = energy_generated_kwh - energy_consumed_kwh

    # Detect anomalies
    is_anomaly, anomaly_details = detect_anomalies(entry)

    # Update site metrics
    site_id = entry['site_id']
    if site_id not in site_metrics:
        site_metrics[site_id] = {
            'total_generated': 0,
            'total_consumed': 0,
            'anomaly_count': 0
        }

    site_metrics[site_id]['total_generated'] += float(energy_generated_kwh)
    site_metrics[site_id]['total_consumed'] += float(energy_consumed_kwh)
    if is_anomaly:
        site_metrics[site_id]['anomaly_count'] += 1

    # Prepare item for DynamoDB
    item = {
        'site_id': entry['site_id'],
        'timestamp': entry['timestamp'],
        'energy_generated_kwh': energy_generated_kwh,
        'energy_consumed_kwh': energy_consumed_kwh,
        'net_energy_kwh': net_energy,
        'temperature_c': Decimal(str(entry['temperature_c'])),
        'humidity_percent': Decimal(str(entry['humidity_percent'])),
        'weather_condition': entry['weather_condition'],
        'anomaly': is_anomaly,
        'anomaly_details': anomaly_details if is_anomaly else []
    }

    # Store in DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=item)

    # Publish anomaly notification if needed
    if is_anomaly:
        publish_sns_message(
            {
                'site_id': entry['site_id'],
                'timestamp': entry['timestamp'],
                'anomalies': anomaly_details,
                'data': entry
            },
            f"Energy Data Anomaly Detected - Site {entry['site_id']}"
        )


def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        site_metrics = {}
        processing_errors = []

        for record in event['Records']:
            try:
                # Get S3 object details
                bucket = record['s3']['bucket']['name']
                key = unquote_plus(record['s3']['object']['key'])
                logger.info(f'Processing file: s3://{bucket}/{key}')

                # Read and parse data
                response = s3.get_object(Bucket=bucket, Key=key)
                data = json.loads(response['Body'].read().decode('utf-8'))

                # Process each entry
                for entry in data:
                    try:
                        process_entry(entry, site_metrics)
                    except (DataValidationError, ClientError) as e:
                        error_msg = f"Error processing entry: {str(e)}"
                        processing_errors.append(error_msg)
                        logger.error(error_msg)

            except Exception as e:
                error_msg = f"Error processing file {key}: {str(e)}"
                processing_errors.append(error_msg)
                logger.error(error_msg)

        # Publish processing summary
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'site_metrics': site_metrics,
            'processing_errors': processing_errors,
            'total_errors': len(processing_errors)
        }

        publish_sns_message(
            summary,
            f"Energy Data Processing Summary - {len(processing_errors)} errors"
        )

        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }

    except Exception as e:
        error_msg = f"Fatal error in lambda_handler: {str(e)}"
        logger.error(error_msg)
        publish_sns_message(
            {'error': error_msg},
            "Energy Data Processing - Fatal Error"
        )
        raise