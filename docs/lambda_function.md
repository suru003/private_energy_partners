# Energy Data Processing Lambda Function

## Overview
AWS Lambda function for processing renewable energy data files, performing validation, anomaly detection, and storage in DynamoDB with SNS notifications.

## Key Features
- Data validation
- Anomaly detection
- DynamoDB storage
- SNS notifications
- Error handling and logging

## Anomaly Detection Criteria
- Negative energy generation/consumption
- Unusual energy patterns
- Extreme weather conditions

## Configured AWS Services 
- Lambda
- S3
- DynamoDB
- SNS

## Configuration
- `TABLE_NAME`: DynamoDB table
- `SNS_TOPIC_ARN`: Notification topic
- `ANOMALY_THRESHOLD`: Validation ranges

## Anomaly Thresholds
- Energy Generation: `>= 0 kWh`
- Energy Consumption: `>= 0 kWh`
- Temperature: -20°C to 50°C
- Humidity: 0% to 100%

## Error Handling
- Custom exceptions
- Detailed logging
- SNS error notifications

## Deployment
1. Create Lambda function
2. Set IAM roles
3. Configure S3 trigger
4. Set environment variables

## Monitoring
- CloudWatch logs
- SNS alerts for anomalies and errors

## Prerequisites
#### Most of deployment is done by CloudFormation. (ref to cloudformation.md)
- AWS Account
- Configured Lambda function
- S3 bucket with data files
- DynamoDB table
- SNS topic

## Security
- Follow the principle of least privilege for IAM roles `(currently set to full admin but will be restricted to necessary permissions)`
- Encrypt sensitive data