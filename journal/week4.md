# Week 4 — Postgres and RDS

## Provision RDS Instance via AWS CLI

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

```sh
psql -U postgres --host localhost
```

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