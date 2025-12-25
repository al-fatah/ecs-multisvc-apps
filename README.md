# ECS Multi-Service Deployment (Apps)

Two containerized Flask microservices:
- `flask-s3-service`: will upload files to S3 (Phase 3)
- `flask-sqs-service`: will send messages to SQS (Phase 3)

## Local quick test
- S3 service: `docker build -t s3 ./flask-s3-service && docker run -p 8080:8080 s3`
- SQS service: `docker build -t sqs ./flask-sqs-service && docker run -p 8081:8081 sqs`

## Phase 1 – Application Build ✅

Both services are containerized Flask apps designed to run locally and on ECS.

### Environment variables
- AWS_REGION
- BUCKET_NAME (flask-s3-service)
- QUEUE_URL (flask-sqs-service)

If variables are not set, the services run in local-safe mode without AWS calls.
