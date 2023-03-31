# Week 6 — Deploying Containers

## AWS Containers

### Types of Container Services in AWS
1. Virtual Machines: Hosting containers in avirtual server (EC2)
2. Managed services
    - Amazon ECS (Elastic Container Service)
    - Fargate
    _ Amazon EKS (Elastic Kubernetes Service)

## Deploying an Application to a Container using AWS ECS
### Types of Launch types to AWS ECS
- Amazon EC2 architecture
- Amazon ECS architecture
- Fargate (serveless architecture)

### Amazon ECS Security Best Practices - AWS

**Resource**: https://www.youtube.com/watch?v=zz2FQAk1I28&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=58

- Cloud Control Plane Configuration - Access Control, Container Images etc
- Choosing the right Public or Private ECR for images.
- Amazon ECR Scan Images to `Scan on Push` using Basic or Enhanced(Inspector + Snyk)
- Use VPC Endpoints or Security Groups with known sources only
- Amazon Organizations SCP - to manage ECS Task deletion, ECS creation, region lock etc
- AWS CloudTrail is enabled and monitored to trigger alerts on malicious ECS behaviour by an identity in AWS.
- AWS Config Rules (as no GuardDuty (ECS) even in Mar'2023) is enabled in the account and region of ECS

### Amazon ECS Security Best Practices - Application
- Access Control - Roles or IAM Users for ECS Clusters/Services/Tasks
- Most recent version of ECR Agent daemon on EC@
- Container Control Plane Configuration - Root privileges, resource limitations etc
- No secrets/passwords in ECS Task Definitions e.d db password etc - Consider AWS Secret Manager
- Only use Trusted Containers from ECR with no HIGH/CRITICAL Vulnerabilities
- Limit ability to ssh into EC2 container to read only file systems - use APIs or GitOps to pull information for troubleshooting
- Amazon CloudWatch to monitor Malicious ECS Configuration Changes
- Only using Authorized Container Images (hopefully some Image signing in the future e.g sigstore)

## Test RDS Connecetion
Add this `test` script into `db` so we can easily check our connection from our container.

```python
#!/usr/bin/env python3

import psycopg
import os
import sys

connection_url = os.getenv("CONNECTION_URL")

conn = None
try:
  print('attempting connection')
  conn = psycopg.connect(connection_url)
  print("Connection successful!")
except psycopg.Error as e:
  print("Unable to connect to the database:", e)
finally:
  conn.close()
```

Make file executable and test with production RDS instance

```sh
cd ${THEIA_WORKSPACE_ROOT}/backend-flask
chmod u+x bin/db/test
./bin/db/test
cd $THEIA_WORKSPACE_ROOT
```

## Task Flask Script
Add the health-check endpoint for the flask app. See [app.py](../backend-flask/app.py)

```python
@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200
```

Create a new bin script at `backend/bin/flask/health-check` for performing health checks against the backend flask app.

```python
#!/usr/bin/env python3

import urllib.request

response = urllib.request.urlopen('http://localhost:4567/api/health-check')
if response.getcode() == 200:
  print("[OK] Flask server is running")
  exit(0) # success
else:
  print("[BAD] Flask server is not running")
  exit(1) # false
```

Make file executable and test with production RDS instance

```sh
cd ${THEIA_WORKSPACE_ROOT}/backend-flask
chmod u+x bin/flask/health-check
./bin/flask/health-check
cd $THEIA_WORKSPACE_ROOT
```

**Output**
```
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6) $ ./backend-flask/bin/flask/health-check 
[OK] Flask server is running
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6)
```
