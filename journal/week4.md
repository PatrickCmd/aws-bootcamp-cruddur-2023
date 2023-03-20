# Week 4 — Postgres and RDS

## Reference

I used the [instructors journal](https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-4/journal/week4.md) as a reference.

## Note:
The lat final implementations for this week were done with both gitpod and codespaces. Run low on gitpod credits, so most of the environment variables are pointing to `CODESPACES` environment.

### Setting up codespaces environment
```sh
export CODESPACES_IP=$(curl ifconfig.me)
cd backend-flask
./bin/rds-update-sg-rule CODDESPACES
```

### Test for database connection
```sh
./bin/db-connect prod
cd ../
```

## Provision RDS Instance via AWS CONSOLE

I started by experimenting how to provision an AWS RDS instance from the `AWS web console (GUI)` and also update the vpc security group of the instance to allow connections to the database instance from anywhere.

![AWS RDS](assets/week-4/aws_rds_1.png)

![AWS RDS](assets/week-4/aws_rds_2.png)


![AWS RDS](assets/week-4/aws_rds_3.png)


![AWS RDS](assets/week-4/aws_rds_4.png)


![AWS RDS](assets/week-4/aws_rds_5.png)


![AWS RDS](assets/week-4/aws_rds_6.png)


![AWS RDS](assets/week-4/aws_rds_7.png)

![AWS RDS](assets/week-4/aws_rds_8.png)

![AWS RDS](assets/week-4/aws_rds_9.png)

After the experiment I deleted the RDS instance.

## Provision RDS Instance via AWS CLI

For the most part of the this section I work via console, provision the `AWS RDS instance` via cli.

```sh
export AWS_RDS_POSTGRES_PASSWORD="cmdhuEE33z2Qvlxxxxxxxxx"
gp env AWS_RDS_POSTGRES_PASSWORD=${AWS_RDS_POSTGRES_PASSWORD}
```

```sh
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cmdcruddurroot \
  --master-user-password ${AWS_RDS_POSTGRES_PASSWORD} \
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp3 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

```
{
    "DBInstance": {
        "DBInstanceIdentifier": "cruddur-db-instance",
        "DBInstanceClass": "db.t3.micro",
        "Engine": "postgres",
        "DBInstanceStatus": "creating",
        "MasterUsername": "cmdcruddurroot",
        "DBName": "cruddur",
        "AllocatedStorage": 20,
        "PreferredBackupWindow": "03:53-04:23",
        "BackupRetentionPeriod": 0,
        "DBSecurityGroups": [],
        "VpcSecurityGroups": [
            {
                "VpcSecurityGroupId": "sg-04edcc89a5ba6f26b",
                "Status": "active"
            }
        ],
        "DBParameterGroups": [
            {
                "DBParameterGroupName": "default.postgres14",
                "ParameterApplyStatus": "in-sync"
            }
        ],
        
    ...
    }
}
```



### Connect to postgres via psql client

To connect to psql via the psql client cli tool remember to use the host flag to specific localhost.

```sh
psql -U postgres --host localhost
```

**Common PSQL commands:**

```sql
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```

## Create (and dropping) our database

We can use the createdb command to create our database:

https://www.postgresql.org/docs/current/app-createdb.html

```sh
createdb cruddur -h localhost -U postgres
psql -U postgres -h localhost
\l
DROP database cruddur;
```

We can create the database within the PSQL client

```sql
CREATE database cruddur;
```

## Importing Scripts

### Import DB Schema

```sh
psql cruddur < db/schema.sql -h localhost -U postgres
```

### Set postgresql local connection URL

```sh
export LOCAL_CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
gp env LOCAL_CONNECTION_URL=${LOCAL_CONNECTION_URL}
```

Now we can connect to the local postgresql instance via psql client with the command below

```sh
psql ${LOCAL_CONNECTION_URL}
```

### Set postgresql AWS Connection URL

```sh
export AWS_RDS_POSTGRES_ENPOINT="cruddur-db-instance.cqs4fi8faxh3.us-east-1.rds.amazonaws.com"
gp env AWS_RDS_POSTGRES_ENPOINT=${AWS_RDS_POSTGRES_ENPOINT}
export PROD_CONNECTION_URL="postgresql://cmdcruddurroot:${AWS_RDS_POSTGRES_PASSWORD}@${AWS_RDS_POSTGRES_ENPOINT}:5432/cruddur"
gp env PROD_CONNECTION_URL=${PROD_CONNECTION_URL}
```

### Add binary files for creating, droping and loading database schema

Reference the `bin` folder to see the full files [here](../backend-flask/bin/)

### Change permissions for the binary files to be executable for the user

```sh
cd backend-flask
chmod u+x bin/*
cd ../
```

### Perform string replacement with the `sed` command before running the binary files.

Resources to learn more about `sed` command
1. [sed cheatsheat quickref](https://quickref.me/sed)
2. [Digital Ocean](https://www.digitalocean.com/community/tutorials/the-basics-of-using-the-sed-stream-editor-to-manipulate-text-in-linux)
3. [Tutorialspoint](https://www.tutorialspoint.com/sed/index.htm)
4. [Sed - An Introduction and Tutorial by Bruce Barnett](https://www.grymoire.com/Unix/Sed.html)
5. [Geeksforgeeks](https://www.geeksforgeeks.org/sed-command-in-linux-unix-with-examples/)
6. [ssstonebraker/sed cheatsheet](https://gist.github.com/ssstonebraker/6140154)

For example replace the `/cruddur` word with empty space using `sed` with command below:

```sh
sed 's/\/cruddur//g' <<<"$LOCAL_CONNECTION_URL"
```

Output
```
postgresql://postgres:password@localhost:5432
```

### Install `psycopg` the python postgresql driver.
Follow the link [here](https://www.psycopg.org/)


### Set postgresql local connection URL for backend service in [docker-compose.yml](../docker-compose.yml) file

```sh
export CONTAINER_DATABASE_URL="postgresql://postgres:password@db:5432/cruddur"
gp env CONTAINER_DATABASE_URL=${CONTAINER_DATABASE_URL}
```


### Connect to RDS via Gitpod
In order to connect to the RDS instance we need to provide our Gitpod IP and whitelist for inbound traffic on port 5432.

```sh
GITPOD_IP=$(curl ifconfig.me)
gp env GITPOD_IP=${GITPOD_IP}
```

We'll create an inbound rule for Postgres (5432) and provide the GITPOD ID.

We'll get the security group rule id so we can easily modify it in the future from the terminal here in Gitpod.

```sh
export DB_SG_ID="sg-04edcc89a5ba6f26b"
gp env DB_SG_ID="${DB_SG_ID}"

export DB_SG_RULE_ID="sgr-0b718303ba558d171"
gp env DB_SG_RULE_ID="${DB_SG_RULE_ID}"
```

Whenever we need to update our security groups we can do this for access.

```sh
cd ${THEIA_WORKSPACE_ROOT}/backend-flask
source bin/rds-update-sg-rule 
cd $THEIA_WORKSPACE_ROOT
```

![AWS RDS SG](assets/week-4/aws_rds_update_sg.png)

![AWS RDS SG](assets/week-4/aws_rds_update_sg_2.png)

### Test remote access
We'll create a connection url:

```sh
echo $PROD_CONNECTION_URL
```

We'll test that it works in Gitpod:

```sh
psql $PROD_CONNECTION_URL
```

#### Output
```
psql (13.10 (Ubuntu 13.10-1.pgdg20.04+1), server 14.6)
WARNING: psql major version 13, server major version 14.
         Some psql features might not work.
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

cruddur=> \l
                                           List of databases
   Name    |     Owner      | Encoding |   Collate   |    Ctype    |         Access privileges         
-----------+----------------+----------+-------------+-------------+-----------------------------------
 cruddur   | cmdcruddurroot | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 postgres  | cmdcruddurroot | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 rdsadmin  | rdsadmin       | UTF8     | en_US.UTF-8 | en_US.UTF-8 | rdsadmin=CTc/rdsadmin            +
           |                |          |             |             | rdstopmgr=Tc/rdsadmin
 template0 | rdsadmin       | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/rdsadmin                      +
           |                |          |             |             | rdsadmin=CTc/rdsadmin
 template1 | cmdcruddurroot | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/cmdcruddurroot                +
           |                |          |             |             | cmdcruddurroot=CTc/cmdcruddurroot
(5 rows)

cruddur=> \d
```

Updated [.gitpod.yml](../.gitpod.yml) file to set `GITPOD IPAddress` and update `AWS RDS SG` whenever gitpod is lauching



### Load Schema and connect to production database

```sh
cd ${THEIA_WORKSPACE_ROOT}/backend-flask
./bin/db-schema-load prod
```

**Output**
```
== db-schema-load
/workspaces/aws-bootcamp-cruddur-2023/backend-flask/db/schema.sql
Running in production mode
CREATE EXTENSION
NOTICE:  table "users" does not exist, skipping
DROP TABLE
NOTICE:  table "activities" does not exist, skipping
DROP TABLE
CREATE TABLE
CREATE TABLE
```

```sh
./bin/db-connect prod
```

**Output**

```
Running in production mode
psql (13.10 (Ubuntu 13.10-1.pgdg20.04+1), server 14.6)
WARNING: psql major version 13, server major version 14.
         Some psql features might not work.
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

cruddur=> \d
              List of relations
 Schema |    Name    | Type  |     Owner      
--------+------------+-------+----------------
 public | activities | table | cmdcruddurroot
 public | users      | table | cmdcruddurroot
(2 rows)

cruddur=> \dt users
            List of relations
 Schema | Name  | Type  |     Owner      
--------+-------+-------+----------------
 public | users | table | cmdcruddurroot
(1 row)

cruddur=> \d users
                                   Table "public.users"
     Column      |            Type             | Collation | Nullable |      Default       
-----------------+-----------------------------+-----------+----------+--------------------
 uuid            | uuid                        |           | not null | uuid_generate_v4()
 display_name    | text                        |           | not null | 
 handle          | text                        |           | not null | 
 email           | text                        |           | not null | 
 cognito_user_id | text                        |           | not null | 
 created_at      | timestamp without time zone |           | not null | CURRENT_TIMESTAMP
Indexes:
    "users_pkey" PRIMARY KEY, btree (uuid)

cruddur=> \d activities
                                    Table "public.activities"
         Column         |            Type             | Collation | Nullable |      Default       
------------------------+-----------------------------+-----------+----------+--------------------
 uuid                   | uuid                        |           | not null | uuid_generate_v4()
 user_uuid              | uuid                        |           | not null | 
 message                | text                        |           | not null | 
 replies_count          | integer                     |           |          | 0
 reposts_count          | integer                     |           |          | 0
 likes_count            | integer                     |           |          | 0
 reply_to_activity_uuid | integer                     |           |          | 
 expires_at             | timestamp without time zone |           |          | 
 created_at             | timestamp without time zone |           | not null | CURRENT_TIMESTAMP
Indexes:
    "activities_pkey" PRIMARY KEY, btree (uuid)

cruddur=> 
```

```sh
cd $THEIA_WORKSPACE_ROOT
```


## Setup Cognito post confirmation lambda

- Create the handler function
- Create lambda in same vpc as rds instance Python 3.8

For the `lambda function` see full example [here](../aws/lambdas/cruddur_post_confirmation.py)

Add a layer for `psycopg2` with one of the below methods for development or production

### Development
https://github.com/AbhimanyuHK/aws-psycopg2

> This is a custom compiled psycopg2 C library for Python. Due to AWS Lambda missing the required PostgreSQL libraries in the AMI image, we needed to compile psycopg2 with the PostgreSQL libpq.so library statically linked libpq library instead of the default dynamic link.

### EASIEST METHOD

Some precompiled versions of this layer are available publicly on AWS freely to add to your function by ARN reference.

https://github.com/jetbridge/psycopg2-lambda-layer

Just go to Layers + in the function console and add a reference for your region
`arn:aws:lambda:ca-central-1:898466741470:layer:psycopg2-py38:1`

Alternatively you can create your own development layer by downloading the psycopg2-binary source files from https://pypi.org/project/psycopg2-binary/#files

- Download the package for the lambda runtime environment: psycopg2_binary-2.9.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

- Extract to a folder, then zip up that folder and upload as a new lambda layer to your AWS account

### Production
Follow the instructions on https://github.com/AbhimanyuHK/aws-psycopg2 to compile your own layer from postgres source libraries for the desired version.

### Add the function to Cognito
Under the user pool properties add the function as a Post Confirmation lambda trigger.


![AWS Cognito Lambda](assets/week-4/aws_lambda_1.png)

![AWS Cognito Lambda](assets/week-4/aws_lambda_2.png)

![AWS Cognito Lambda](assets/week-4/aws_lambda_3.png)

![AWS Cognito Lambda](assets/week-4/aws_lambda_4.png)

![AWS Cognito Lambda](assets/week-4/aws_lambda_5.png)

![AWS Cognito Lambda](assets/week-4/aws_lambda_6.png)

![AWS Cognito Lambda](assets/week-4/aws_lambda_7.png)

### Add permission to lambda to be able to attach VPC

To create a permission, we need to attach a custom policy. See [stackoverflow resource here](https://stackoverflow.com/questions/41177965/aws-lambdathe-provided-execution-role-does-not-have-permissions-to-call-describ)

For example, this is a policy that allows to deploy a Lambda into a VPC:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeNetworkInterfaces",
        "ec2:CreateNetworkInterface",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeInstances",
        "ec2:AttachNetworkInterface"
      ],
      "Resource": "*"
    }
  ]
}
```

![AWS Lambda VPC policy EC2](assets/week-4/aws_lambda_access_vpc_policy.png)

![AWS Lambda VPC policy EC2](assets/week-4/aws_lambda_assign_vpc_policy_3.png)

![AWS Lambda VPC policy EC2](assets/week-4/aws_lambda_assign_vpc_policy_4.png)

![AWS Lambda edit VPC](assets/week-4/aws_lambda_edit_vpc.png)

## Test out AWS Cognito Lambda signing up and confirmation

![AWS cognito signup](assets/week-4/congnito_signup.png)

![AWS cognito signup](assets/week-4/aws_congito_1.png)

After signing up we receive a confirmation code for ccompleting up the confirmarion process.

![AWS cognito confirm](assets/week-4/cognito_confirm.png)

But we that our post confirmation process terminates with an error.

![AWS cognito confirm](assets/week-4/cognito_confirm_fail.png)

But also checking on our cognito user in the `user pool` we that he was successfully confirmed. So now we know that our problem is with the `post confirmation lambda function`.

![AWS cognito confirm](assets/week-4/aws_cognito_2.png)

Digging further into the problem, I see that in the logs we go a timed out error on trying to post to the database, and also our `lambda function` code had some bugs that I have to fix.

![AWS Lambda logs errors](assets/week-4/aws_lambda_logs_1.png)

After updating my lambda function code and deploying it. I see that the confirmation passes successfuly and the user is created in the database after the post confirmation process.

![AWS cognito confirm pass](assets/week-4/aws_cognito_confirm_passed.png)

![AWS Lambda logs pass](assets/week-4/aws_lambda_logs_2.png)


### Check production `AWS RDS` database for user inserted after post confirmation on signup.

```
@PatrickCmd ➜ /workspaces/aws-bootcamp-cruddur-2023/backend-flask (week-4) $ ./bin/db-connect prod
Running in production mode
psql (13.10 (Ubuntu 13.10-1.pgdg20.04+1), server 14.6)
WARNING: psql major version 13, server major version 14.
         Some psql features might not work.
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

cruddur=> \d
              List of relations
 Schema |    Name    | Type  |     Owner      
--------+------------+-------+----------------
 public | activities | table | cmdcruddurroot
 public | users      | table | cmdcruddurroot
(2 rows)

cruddur=> \x on
Expanded display is on.
cruddur=> SELECT * FROM users;
-[ RECORD 1 ]---+-------------------------------------
uuid            | 0b24a278-b60e-4d43-98ab-d10316c8469c
display_name    | Patrick Walukagga
handle          | patrickcmd
email           | pwalukagga@gmail.com
cognito_user_id | 696acd13-a66f-4c77-a16e-d3f980c07fda
created_at      | 2023-03-18 15:11:03.157329

cruddur=> 
````


## Creaing activities

Implemented creating activities endpoint and wiring it with the frontend. See full implementation here [create_activity.py](../backend-flask/services/create_activity.py)

![create activities](assets/week-4/crud_1.png)

![create activities](assets/week-4/frontend_list_activities.png)

### Checking for created activities in production database (AWS RDS Instance)

```sh
cd backend-flask
./bin/db-connect prod
```


```
@PatrickCmd ➜ /workspaces/aws-bootcamp-cruddur-2023/backend-flask (week-4) $ ./bin/db-connect prod
Running in production mode
psql (13.10 (Ubuntu 13.10-1.pgdg20.04+1), server 14.6)
WARNING: psql major version 13, server major version 14.
         Some psql features might not work.
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

cruddur=> SELECT * FROM activities;
cruddur=> \x on
Expanded display is on.
cruddur=> SELECT * FROM activities;
-[ RECORD 1 ]----------+----------------------------------------------------------------------------------------------------------------------------------------
uuid                   | 9dc949ea-179f-4c93-a05e-67188e64b06c
user_uuid              | 0b24a278-b60e-4d43-98ab-d10316c8469c
message                | Learning AWS cloud with Andrew Brown. Completing week 4.
replies_count          | 0
reposts_count          | 0
likes_count            | 0
reply_to_activity_uuid | 
expires_at             | 2023-03-27 09:18:27.676211
created_at             | 2023-03-20 09:18:27.716455
-[ RECORD 2 ]----------+----------------------------------------------------------------------------------------------------------------------------------------
uuid                   | 7057f717-7c0c-4040-abb1-a4c441004a7d
user_uuid              | 0b24a278-b60e-4d43-98ab-d10316c8469c
message                | First to mind when asked what 'the cloud' is, a majority respond it’s either an actual cloud, the sky, or something related to weather.
replies_count          | 0
reposts_count          | 0
likes_count            | 0
reply_to_activity_uuid | 
expires_at             | 2023-03-27 09:26:18.707299
created_at             | 2023-03-20 09:26:18.748366
-[ RECORD 3 ]----------+----------------------------------------------------------------------------------------------------------------------------------------
uuid                   | a02aa21a-3617-495d-a0dd-ee53b3e8d92c
user_uuid              | 0b24a278-b60e-4d43-98ab-d10316c8469c
message                | Week 4 has been tough though. A lot of moving parts.
replies_count          | 0
reposts_count          | 0
likes_count            | 0
reply_to_activity_uuid | 
expires_at             | 2023-03-27 09:27:21.969397
created_at             | 2023-03-20 09:27:22.010373

cruddur=> 
```

![create activities](assets/week-4/database_activities.png)
