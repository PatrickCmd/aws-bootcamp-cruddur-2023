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

## Create CloudWatch Log Group
```sh
aws logs create-log-group --log-group-name cruddur
aws logs put-retention-policy --log-group-name cruddur --retention-in-days 1
```

## Create ECS Cluster

```sh
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

**Output**

```
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6) $ aws ecs create-cluster --cluster-name cruddur --service-connect-defaults namespace=cruddur
{
    "cluster": {
        "clusterArn": "arn:aws:ecs:us-east-1:476313879638:cluster/cruddur",
        "clusterName": "cruddur",
        "status": "PROVISIONING",
        "registeredContainerInstancesCount": 0,
        "runningTasksCount": 0,
        "pendingTasksCount": 0,
        "activeServicesCount": 0,
        "statistics": [],
        "tags": [],
        "settings": [
            {
                "name": "containerInsights",
                "value": "disabled"
            }
        ],
        "capacityProviders": [],
        "defaultCapacityProviderStrategy": [],
        "attachments": [
            {
                "id": "d23cd9fb-ea6b-46e8-bb7d-25b3dfcf909d",
                "type": "sc",
                "status": "ATTACHING",
                "details": []
            }
        ],
        "attachmentsStatus": "UPDATE_IN_PROGRESS",
        "serviceConnectDefaults": {
            "namespace": "arn:aws:servicediscovery:us-east-1:476313879638:namespace/ns-v2krcvqtelpmtvtb"
        }
    }
}
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6) $ 
```

![ECS Cluster](assets/week-6/ecs-cluster.png)

## For ECS EC2 launch type we need to perform the next two steps below.

- **But since we are using `fargate` these next two steps can be skipped**

### Create ECS Cluster Security Group (Need for EC2 launch type)

```sh
export CRUDDUR_ECS_CLUSTER_SG=$(aws ec2 create-security-group \
  --group-name cruddur-ecs-cluster-sg \
  --description "Security group for Cruddur ECS ECS cluster" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
echo $CRUDDUR_ECS_CLUSTER_SG
```

### Get the Security Group ID (after its created) (Need for EC2 launch type)

```sh
export CRUDDUR_ECS_CLUSTER_SG=$(aws ec2 describe-security-groups \
--group-names cruddur-ecs-cluster-sg \
--query 'SecurityGroups[0].GroupId' \
--output text)
```

```sh
gp env CRUDDUR_ECS_CLUSTER_SG=$CRUDDUR_ECS_CLUSTER_SG
```

## Gaining Access to ECS Fargate Container
## Create ECR repo and push image

### For Base-image python

Create ECR repository for python

```sh
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
```

**Output**
```
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6) $ aws ecr create-repository \
>   --repository-name cruddur-python \
>   --image-tag-mutability MUTABLE
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:476313879638:repository/cruddur-python",
        "registryId": "476313879638",
        "repositoryName": "cruddur-python",
        "repositoryUri": "476313879638.dkr.ecr.us-east-1.amazonaws.com/cruddur-python",
        "createdAt": "2023-03-31T19:01:47+00:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

### Login to ECR (To be able to push docker containers to ECR)

```sh
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

Also created bash script for `ECR` login. Reference at [ecr/login](../backend-flask/bin/ecr/login)

### Set URL
```sh
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
gp env ECR_PYTHON_URL=$ECR_PYTHON_URL
```

### Pull Image from Docker Hub
```sh
docker pull python:3.10-slim-buster
```

### Tag Image
```sh
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```

```sh
docker images
```

**Output**
```
476313879638.dkr.ecr.us-east-1.amazonaws.com/cruddur-python   3.10-slim-buster   a8bd408e774a   8 days ago          118MB
python                                                        3.10-slim-buster   a8bd408e774a   8 days ago          118MB
```

### Push Image to ECR
```sh
docker push $ECR_PYTHON_URL:3.10-slim-buster
```

### For Backend Flask
In the backend flask dockerfile update the from to instead of using DockerHub's python image I use my own eg.

> remember to put the :latest tag on the end

### Create Repo
```sh
aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
```

### Set URL
```sh
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL
gp env ECR_BACKEND_FLASK_URL=$ECR_BACKEND_FLASK_URL
```

### Build Image
```sh
docker build -f ./backend-flask/Dockerfile.prod -t backend-flask-prod ./backend-flask/
```

### Tag Image
```sh
docker tag backend-flask-prod:latest $ECR_BACKEND_FLASK_URL:latest
```

### Push Image
```sh
docker push $ECR_BACKEND_FLASK_URL:latest
```

## Register Task Defintions
### Passing Senstive Data to Task Defintion
- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html 
- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html

```sh
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_ACCESS_KEY_ID" --value $AWS_ACCESS_KEY_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/DATABASE_URL" --value $PROD_CONNECTION_URL
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" --value $ROLLBAR_ACCESS_TOKEN
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" --value "x-honeycomb-team=$HONEYCOMB_API_KEY"
```
**Sample Output**
```
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6) $ aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
{
    "Version": 1,
    "Tier": "Standard"
}
gitpod /workspace/aws-bootcamp-cruddur-2023 (week-6) $ aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/DATABASE_URL" --value $PROD_CONNECTION_URL
{
    "Version": 1,
    "Tier": "Standard"
}
```

![aws parameter store](assets/week-6/aws_parameter_store.png)

### Create Task and Exection Roles for Task Defintion
#### Create ExecutionRole

```sh
aws iam create-role \
    --role-name CruddurServiceExecutionRole \
    --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[\"sts:AssumeRole\"],
    \"Effect\":\"Allow\",
    \"Principal\":{
      \"Service\":[\"ecs-tasks.amazonaws.com\"]
    }
  }]
}"
```

```sh
aws iam create-role --role-name CruddurServiceExecutionPolicy --assume-role-policy-document "file://aws/policies/service-assume-role-execution-policy.json"
```

```sh
aws iam put-role-policy \
  --policy-name CruddurServiceExecutionPolicy \
  --role-name CruddurServiceExecutionRole \
  --policy-document "file://aws/policies/service-execution-policy.json"
```

```sh
aws iam attach-role-policy --policy-arn POLICY_ARN --role-name CruddurServiceExecutionRole
```
