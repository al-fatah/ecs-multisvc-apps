# ECS Multi-Service Applications

This repository contains the **application layer** for a portfolio project deploying **two containerized Flask microservices** on **AWS ECS Fargate**, fronted by an **Application Load Balancer (ALB)**.

The services are deployed using **GitHub Actions CI/CD** with **OIDC-based authentication** (no static AWS credentials).

---

## Services Overview

### 1) Flask S3 Service
- Endpoint base path: `/s3`
- Responsibilities:
  - Health check
  - File upload to Amazon S3
- AWS integrations:
  - Amazon S3
  - CloudWatch Logs

### 2) Flask SQS Service
- Endpoint base path: `/sqs`
- Responsibilities:
  - Health check
  - Send messages to Amazon SQS
- AWS integrations:
  - Amazon SQS
  - CloudWatch Logs

---

## Architecture (Runtime View)

Internet  
→ Application Load Balancer (ALB)  
→ `/s3/*` → ECS Service (Flask S3 App) → S3 Bucket  
→ `/sqs/*` → ECS Service (Flask SQS App) → SQS Queue  

Each service runs as an independent **ECS Fargate service** with its own task definition and IAM permissions.

---

## Repository Structure

```
ecs-multisvc-apps/
├── flask-s3-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── flask-sqs-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── .github/
│   └── workflows/
│       ├── ci-s3.yml
│       ├── ci-sqs.yml
│       ├── deploy-s3.yml
│       └── deploy-sqs.yml
└── README.md
```

---

## Environment Variables

### Flask S3 Service
- `AWS_REGION`
- `BUCKET_NAME`
- `BASE_PATH` (default: `/s3`)

### Flask SQS Service
- `AWS_REGION`
- `QUEUE_URL`
- `BASE_PATH` (default: `/sqs`)

If AWS variables are not set, services run in **local-safe mode** (no AWS calls).

---

## Local Development

### Build images
```bash
docker build -t flask-s3-service ./flask-s3-service
docker build -t flask-sqs-service ./flask-sqs-service
```

### Run locally
```bash
docker run -p 8080:8080 flask-s3-service
docker run -p 8081:8081 flask-sqs-service
```

### Test endpoints
```bash
curl http://localhost:8080/health
curl http://localhost:8081/health
```

---

## CI/CD Workflows

### CI (Pull Requests)
Triggered on pull requests to `main`:
- Docker image build per service directory
- Ensures Dockerfiles remain valid

### CD (Manual Deploy)
Triggered manually via GitHub Actions:
- Builds and pushes Docker images to ECR
- Forces ECS service redeployment
- Uses GitHub OIDC to assume AWS IAM role

No AWS access keys are stored in GitHub.

---

## Deployment Validation

After deployment, verify:

```bash
curl http://<ALB_DNS>/s3/health
curl http://<ALB_DNS>/sqs/health
```

### Upload file to S3
```bash
curl -F "file=@README.md" http://<ALB_DNS>/s3/upload
```

### Send message to SQS
```bash
curl -X POST http://<ALB_DNS>/sqs/send \
  -H "Content-Type: application/json" \
  -d '{"message":"hello from ecs"}'
```

---

## Security Design

- GitHub Actions uses **OIDC** (no static credentials)
- ECS Task Roles use **least privilege**
  - S3 service: `s3:PutObject`
  - SQS service: `sqs:SendMessage`
- Each service has isolated permissions

---

## Why These Design Choices

- **Separate services**: clear boundaries and scaling
- **ALB path routing**: single entry point, multiple apps
- **OIDC CI/CD**: secure, modern deployment pattern
- **Dockerized Flask apps**: portable and reproducible

---

## Status

- Phase 1: Application build (Docker + Flask) ✅
- Phase 3: ECS deployment ✅
- Phase 4: CI/CD with GitHub Actions + OIDC ✅
- Phase 5: Portfolio documentation ✅

---

### One-line summary

Two containerized Flask microservices deployed on ECS Fargate with ALB routing, automated via GitHub Actions using OIDC and least-privilege IAM.
