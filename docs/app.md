# Energy Metrics FastAPI Backend

## Overview
A FastAPI-based API for querying energy metrics data stored in DynamoDB, providing endpoints for retrieving records and anomalies.

## Hardcoded Values
### 1. DynamoDB Table
```python
table = dynamodb.Table('EnergyMetrics')
```
- **Hardcoded Table Name**: `EnergyMetrics`
- **Recommendation**: Use environment variables
  ```python
  import os
  table_name = os.environ.get('DYNAMODB_TABLE', 'EnergyMetrics')
  table = dynamodb.Table(table_name)
  ```

## Recommended Improvements

### 1. Query Optimization
```python
@app.get("/records/", response_model=List[Record])
def get_records(site_id: str, start_time: str, end_time: str):
    response = table.query(
        KeyConditionExpression=Key('site_id').eq(site_id) & 
                                Key('timestamp').between(start_time, end_time)
    )
    return response['Items']
```

### 2. Pagination Support
```python
@app.get("/records/")
def get_records(
    site_id: str, 
    start_time: str, 
    end_time: str,
    limit: int = Query(default=100, le=1000)
):
    # Implement pagination logic
    pass
```

## API Endpoints
1. `/`: Root endpoint
2. `/records/`: Fetch records by site and time range
3. `/anomalies/`: Retrieve site-specific anomalies

## Security Considerations
- Add authentication
- Implement rate limiting

## Performance Optimization
- Use DynamoDB `Query` instead of `Scan`
- Implement caching
- Add pagination
- Use indexing

## Deployment Considerations
- Use AWS Lambda with API Gateway
- Configure CORS
- Set up proper IAM roles

## Example Request
```bash
# Fetch records
GET /records/?site_id=site_2&start_time=2025-02-17&end_time=2025-02-18

# Fetch anomalies
GET /anomalies/?site_id=site_2
```

## Monitoring
- Add logging
- Integrate with CloudWatch
- Track API performance metrics

## Recommended Tools
- `python-dotenv` for environment management
- `mangum` for AWS Lambda integration
- `aws-xray-sdk` for tracing

## Deployment
```bash
# Local development
uvicorn main:app --reload

# Production (AWS Lambda)
chalice deploy
```
