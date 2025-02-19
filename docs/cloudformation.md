# CloudFormation Template for Energy Metrics Infrastructure

## Template Overview
Provisions AWS resources for an energy metrics data processing pipeline using serverless architecture.

## Architectural Considerations

### Lambda Function
- **Inline Code Approach**
  - Quick deployment for assessment
  - Recommended for small, single-purpose functions
  - *Note*: For production, I'd use separate code repository or S3-stored code

### Configuration Improvements
- **Environment Variables Recommendation**
  ```python
  # Utilize os.environ for dynamic configuration
  TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'DefaultTableName')
  SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC', 'default-topic-arn')
  ```

### Deployment Considerations
- Single CloudFormation template
- Parameterized bucket name
- Includes IAM roles and permissions
- Automated resource provisioning

## Resource Breakdown
- S3 Bucket for data ingestion
- DynamoDB for data storage
- Lambda for data processing
- IAM Roles and Permissions

## Potential Enhancements
- Separate Lambda code into external file
- Use AWS Systems Manager Parameter Store
- Add error handling and retry mechanisms

## Deployment
```bash
aws cloudformation create-stack \
  --stack-name PipelineName \
  --template-body file://template.yaml \
  --parameters ParameterKey=NotificationBucket,ParameterValue=my-unique-bucket-name
```

```
------------------------------ Notes ------------------------------
``` 
- Designed for assessment purposes
- Demonstrates serverless data processing pattern
- Easily extensible infrastructure