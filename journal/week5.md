# Week 5 — DynamoDB and Serverless Caching

## The Boundaries of DynamoDB
I read through the instructor's journal [here](https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-5/journal/week5.md#the-boundaries-of-dynamodb) to be able to complete this week.

## DynamoDB Bash Scripts
Implemented a couple of scripts for loading schema, dropping tables and seed data into dynamodb locally. For a complete reference see the dynamodb scripts to test locally [here](../backend-flask/bin/ddb/)

To test out the scripts and access patterns locally, I ran the scritps with the commands below.

```sh
cd ${THEIA_WORKSPACE_ROOT}/backend-flask
```

To create a sample table `cruddur-messages`, I load the schema using the script below

```sh
./bin/ddb/schema-load
```

After loading the schema, I can confirm if the table has been created.

```sh
./bin/ddb/list-tables
```

**Output**
```
gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (week-5) $ ./bin/ddb/list-tables 
----------------------
|     ListTables     |
+--------------------+
|  Music             |
|  cruddur-messages  |
+--------------------+
gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (week-5) $ 
```

### Seed data into dynamodb table
To be able to seed some data, I need to make sure I have some users loaded/seeded in my local postgresql database.
I first perform a database setup. Set some local environment variables.

```sh
echo $LOCAL_CONNECTION_URL
```

**Output**
```
postgresql://postgres:password@localhost:5432/cruddur
```

Set `DATABASE_URL` which is referenced in the [**db**](../backend-flask/utils/db.py) script
```sh
export DATABASE_URL=$LOCAL_CONNECTION_URL
```

Connect, load schema and seed data into postgresql database
```sh
./bin/db/setup
```

```
gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (week-5) $ ./bin/db/connect 
psql (13.10 (Ubuntu 13.10-1.pgdg20.04+1))
Type "help" for help.

cruddur=# \d
           List of relations
 Schema |    Name    | Type  |  Owner   
--------+------------+-------+----------
 public | activities | table | postgres
 public | users      | table | postgres
(2 rows)

cruddur=# \x on
Expanded display is on.
cruddur=# SELECT * FROM users;

gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (week-5) $ ./bin/db/connect 
psql (13.10 (Ubuntu 13.10-1.pgdg20.04+1))
Type "help" for help.

cruddur=# \d
           List of relations
 Schema |    Name    | Type  |  Owner   
--------+------------+-------+----------
 public | activities | table | postgres
 public | users      | table | postgres
(2 rows)

cruddur=# \x on
Expanded display is on.
cruddur=# SELECT * FROM users;

-[ RECORD 1 ]---+-------------------------------------
uuid            | ea76091e-1a0d-4b57-a57a-5c9c0965c061
display_name    | Andrew Brown
handle          | andrewbrown
email           | andrewbrown@cloudprojectbootcamp.com
cognito_user_id | MOCK
created_at      | 2023-03-23 22:20:57.088515
-[ RECORD 2 ]---+-------------------------------------
uuid            | 6fddb47e-6739-46b0-ac13-e7f3e78aa2e0
display_name    | Andrew Bayko
handle          | bayko
email           | bayko@cloudprojectbootcamp.com
cognito_user_id | MOCK
created_at      | 2023-03-23 22:20:57.088515
-[ RECORD 3 ]---+-------------------------------------
uuid            | 618e67a7-336f-4578-97b8-4740f7c93aa3
display_name    | Patrick Walukagga
handle          | patrickcmd
email           | pwalukagga@gmail.com
cognito_user_id | MOCK
created_at      | 2023-03-23 22:20:57.088515
-[ RECORD 4 ]---+-------------------------------------
uuid            | 1b2a36b5-3b56-4c15-91c7-65df403c62e4
display_name    | Telnet Cmd
handle          | telnetcmd
email           | patrickcmdtelnet@gmail.com
cognito_user_id | MOCK
created_at      | 2023-03-23 22:20:57.088515
```

Now that some mock users have been added to our database, we can use them to seed conversation messages into the `cruddur-messages` table in dynamoDB.

```sh
./bin/ddb/seed
```

To confirm, I perform a table scan on `cruddur-messages`

```sh
./bin/ddb/scan
```

**Sample Output**
```
{'user_uuid': '1b2a36b5-3b56-4c15-91c7-65df403c62e4', 'message_group_uuid': '5ae290ed-55d1-47a0-bc6d-fe2bc2700399', 'user_handle': 'telnetcmd', 'sk': '2023-03-23T22:39:12.160498+00:00', 'pk': 'GRP#618e67a7-336f-4578-97b8-4740f7c93aa3', 'message': 'this is a filler message', 'user_display_name': 'Telnet Cmd'}
{'user_uuid': '618e67a7-336f-4578-97b8-4740f7c93aa3', 'message_group_uuid': '5ae290ed-55d1-47a0-bc6d-fe2bc2700399', 'user_handle': 'patrickcmd', 'sk': '2023-03-23T22:39:12.160498+00:00', 'pk': 'GRP#1b2a36b5-3b56-4c15-91c7-65df403c62e4', 'message': 'this is a filler message', 'user_display_name': 'Patrick Walukagga'}
{'user_uuid': '618e67a7-336f-4578-97b8-4740f7c93aa3', 'user_handle': 'patrickcmd', 'sk': '2023-03-23T22:39:12.160498+00:00', 'pk': 'MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399', 'message_uuid': 'a0c23064-216e-4f47-bf56-a33c586caa56', 'message': "Have you ever watched Babylon 5? It's one of my favorite TV shows!", 'user_display_name': 'Patrick Walukagga'}
{'user_uuid': '1b2a36b5-3b56-4c15-91c7-65df403c62e4', 'user_handle': 'telnetcmd', 'sk': '2023-03-23T22:40:12.160498+00:00', 'pk': 'MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399', 'message_uuid': 'bb2765be-0ecf-4878-a83b-1b217a0bd9db', 'message': "Yes, I have! I love it too. What's your favorite season?", 'user_display_name': 'Telnet Cmd'}
{'user_uuid': '618e67a7-336f-4578-97b8-4740f7c93aa3', 'user_handle': 'patrickcmd', 'sk': '2023-03-23T22:41:12.160498+00:00', 'pk': 'MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399', 'message_uuid': 'f75c2756-4ec7-4657-9e50-7e680cbe8df6', 'message': 'I think my favorite season has to be season 3. So many great episodes, like "Severed Dreams" and "War Without End."', 'user_display_name': 'Patrick Walukagga'}
{'user_uuid': '1b2a36b5-3b56-4c15-91c7-65df403c62e4', 'user_handle': 'telnetcmd', 'sk': '2023-03-23T22:42:12.160498+00:00', 'pk': 'MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399', 'message_uuid': 'cb4a828d-4093-464e-af82-6eb198a2e8f1', 'message': 'Yeah, season 3 was amazing! I also loved season 4, especially with the Shadow War heating up and the introduction of the White Star.', 'user_display_name': 'Telnet Cmd'}
...
```

### Sample Access Patterns
A sample of the access patterns can be referenced [here](../backend-flask/bin/ddb/patterns/)

**Showing a single conversion**
```sh
./bin/ddb/get-conversation
```

**Sample Output**
```
{
  "ConsumedCapacity": {
    "CapacityUnits": 1.5,
    "TableName": "cruddur-messages"
  },
  "Count": 20,
  "Items": [
    {
      "message": {
        "S": "Definitely. I think his character is a great example of the show's ability to balance humor and heart, and to create memorable and beloved characters that fans will cherish for years to come."
      },
      "message_uuid": {
        "S": "69d85141-24cf-4dfe-9980-827c193be12f"
      },
      "pk": {
        "S": "MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399"
      },
      "sk": {
        "S": "2023-03-24T00:22:12.160498+00:00"
      },
      "user_display_name": {
        "S": "Telnet Cmd"
      },
      "user_handle": {
        "S": "telnetcmd"
      },
      "user_uuid": {
        "S": "1b2a36b5-3b56-4c15-91c7-65df403c62e4"
      }
    },
    {
      "message": {
        "S": "And Zathras was just one example of that. He was a small but important part of the show's legacy, and he's still remembered fondly by fans today."
      },
      "message_uuid": {
        "S": "99c64a27-566a-47f3-8e26-6c11c291232a"
      },
      "pk": {
        "S": "MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399"
      },
      "sk": {
        "S": "2023-03-24T00:21:12.160498+00:00"
      },
      "user_display_name": {
        "S": "Patrick Walukagga"
      },
      "user_handle": {
        "S": "patrickcmd"
      },
      "user_uuid": {
        "S": "618e67a7-336f-4578-97b8-4740f7c93aa3"
      }
    },
...
    "ScannedCount": 20
}
{
  "CapacityUnits": 1.5,
  "TableName": "cruddur-messages"
}
patrickcmd  2023-03-24 12:03 AM   One thing that really stands out about B...
telnetcmd   2023-03-24 12:04 AM   I thought the special effects in Babylon...
patrickcmd  2023-03-24 12:05 AM   Yes, I was really blown away by the leve...
telnetcmd   2023-03-24 12:06 AM   And I also appreciated the way the show ...
patrickcmd  2023-03-24 12:07 AM   Absolutely. The show had a great balance...
telnetcmd   2023-03-24 12:08 AM   And it's also worth noting the way the s...
patrickcmd  2023-03-24 12:09 AM   Yes, I agree. And it's impressive how th...
telnetcmd   2023-03-24 12:10 AM   Definitely. And it's one of the reasons ...
patrickcmd  2023-03-24 12:11 AM   Agreed. And it's also worth noting the w...
telnetcmd   2023-03-24 12:12 AM   Yes, it definitely had a big impact on t...
patrickcmd  2023-03-24 12:13 AM   Another character I wanted to discuss is...
telnetcmd   2023-03-24 12:14 AM   Zathras was a really unique and memorabl...
patrickcmd  2023-03-24 12:15 AM   Yes, I thought he was a great addition t...
```

**List of conversations**
```sh
./bin/ddb/patterns/list-conversations
```

**Sample Output**
```
connection_url: postgresql://postgres:password@localhost:5432/cruddur
 SQL STATEMENT-[value]------

    SELECT 
      users.uuid
    FROM users
    WHERE
      users.handle =%(handle)s
   {'handle': 'patrickcmd'}
my-uuid: 618e67a7-336f-4578-97b8-4740f7c93aa3
{
  "ConsumedCapacity": {
    "CapacityUnits": 0.5,
    "TableName": "cruddur-messages"
  },
  "Count": 1,
  "Items": [
    {
      "message": {
        "S": "this is a filler message"
      },
      "message_group_uuid": {
        "S": "5ae290ed-55d1-47a0-bc6d-fe2bc2700399"
      },
      "pk": {
        "S": "GRP#618e67a7-336f-4578-97b8-4740f7c93aa3"
      },
      "sk": {
        "S": "2023-03-23T22:39:12.160498+00:00"
      },
      "user_display_name": {
        "S": "Telnet Cmd"
      },
      "user_handle": {
        "S": "telnetcmd"
      },
      "user_uuid": {
        "S": "1b2a36b5-3b56-4c15-91c7-65df403c62e4"
      }
    }
  ],
  "ResponseMetadata": {
    "HTTPHeaders": {
      "content-length": "449",
      "content-type": "application/x-amz-json-1.0",
      "date": "Fri, 24 Mar 2023 00:26:53 GMT",
      "server": "Jetty(9.4.48.v20220622)",
      "x-amz-crc32": "287447233",
      "x-amzn-requestid": "c954f085-92fc-4070-99cc-2be3a6aa0c17"
    },
    "HTTPStatusCode": 200,
    "RequestId": "c954f085-92fc-4070-99cc-2be3a6aa0c17",
    "RetryAttempts": 0
  },
  "ScannedCount": 1
}
```

## Implement Conversations with DynamoDB into the application

![home page](assets/week-5/home.png)

![signin](assets/week-5/signin.png)

![home after signin](assets/week-5/home_after_signin.png)

![crud create activity](assets/week-5/crud_create_acivity.png)

![home after crud create activity](assets/week-5/home_after_crud_create_activity.png)

![display message groups](assets/week-5/display_message_groups.png)

![messages in message groups](assets/week-5/display_messages_of_group.png)

![create message in group](assets/week-5/create_message.png)

![created message in group](assets/week-5/created_message_in_group.png)

![new handle](assets/week-5/message_new_handle.png)

![new handle create message](assets/week-5/new_handle_create_message.png)

![new handle created message](assets/week-5/new_handle_created_message.png)

## DynamoDB Streams and Serverless Caching

### DynamoDB Stream trigger to update message groups
- create a VPC endpoint for dynamoDB service on your VPC
- create a Python lambda function in your vpc
- enable streams on the table with 'new image' attributes included
- add your function as a trigger on the stream
- grant the lambda IAM role permission to read the DynamoDB stream events

`AWSLambdaInvocation-DynamoDB`

- grant the lambda IAM role permission to update table items

#### Create DynamoDB table and load schema in production

See full scripts [here](../backend-flask/bin/ddb/)

```sh
cd ${THEIA_WORKSPACE_ROOT}/backend-flask
./bin/ddb/schema-load prod
```

![dynamodb prod table](assets/week-5/dynamodb_table_prod.png)

#### The function

```python
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
 'dynamodb',
 region_name='us-east-1',
 endpoint_url="http://dynamodb.us-east-1.amazonaws.com"
)

def lambda_handler(event, context):
  pk = event['Records'][0]['dynamodb']['Keys']['pk']['S']
  sk = event['Records'][0]['dynamodb']['Keys']['sk']['S']
  if pk.startswith('MSG#'):
    group_uuid = pk.replace("MSG#","")
    message = event['Records'][0]['dynamodb']['NewImage']['message']['S']
    print("GRUP ===>",group_uuid,message)
    
    table_name = 'cruddur-messages'
    index_name = 'message-group-sk-index'
    table = dynamodb.Table(table_name)
    data = table.query(
      IndexName=index_name,
      KeyConditionExpression=Key('message_group_uuid').eq(group_uuid)
    )
    print("RESP ===>",data['Items'])
    
    # recreate the message group rows with new SK value
    for i in data['Items']:
      delete_item = table.delete_item(Key={'pk': i['pk'], 'sk': i['sk']})
      print("DELETE ===>",delete_item)
      
      response = table.put_item(
        Item={
          'pk': i['pk'],
          'sk': sk,
          'message_group_uuid':i['message_group_uuid'],
          'message':message,
          'user_display_name': i['user_display_name'],
          'user_handle': i['user_handle'],
          'user_uuid': i['user_uuid']
        }
      )
      print("CREATE ===>",response)
```

#### Turn on DynamoDB streams

- Enable streams on the table with 'new image' attributes included

![dynamodb-streams](assets/week-5/turn_dynamodb_streams_on_new_image.png)

![dynamodb-streams](assets/week-5/dynamodb_streams_details.png)

#### VPC endpoint for dynamoDB service on the VPC

![create dynamo vpc endpoint](assets/week-5/create_dynamo_vpc_endpoint1.png)

![create dynamo vpc endpoint](assets/week-5/create_dynamo_vpc_endpoint2.png)

![create dynamo vpc endpoint](assets/week-5/create_dynamo_vpc_endpoint3.png)

![create dynamo vpc endpoint](assets/week-5/create_dynamo_vpc_endpoint4.png)

#### Create a Python lambda function in the vpc

![Create a Python lambda](assets/week-5/create_lambda_function1.png)

![Create a Python lambda](assets/week-5/create_lambda_function2.png)

![Create a Python lambda](assets/week-5/create_lambda_function3.png)

![Create a Python lambda](assets/week-5/create_lambda_function4.png)

![Create a Python lambda](assets/week-5/create_lambda_function5.png)

#### Grant the lambda IAM role permission to read the DynamoDB stream events

- Also remember to attach `AmazonDynamoDBFullAccess` policy in case of any errors.

![Attach policy](assets/week-5/create_lambda_attach_policy.png)

![Attach policy](assets/week-5/create_lambda_attach_policy2.png)

![Attach policy](assets/week-5/create_lambda_attach_policy3.png)

- Found that adding `DynamoDB Full Access` policy doesn't resolve the permission errors. So went ahead and created/attached an inline plocy with the permissions below

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:Query"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:476313879638:table/cruddur-messages",
                "arn:aws:dynamodb:us-east-1:476313879638:table/cruddur-messages/index/message-group-sk-index"
            ]
        }
    ]
}
```

![Attach policy](assets/week-5/create_lambda_attach_policy4.png)



#### Add the function as a trigger on the stream

![Add lambda trigger](assets/week-5/create_lambda_turnon_trigger.png)

### Testing out DynamoDB Streams with Lambda

![dynamodb streams](assets/week-5/dynamoDB_streams_testing.png)

![dynamodb streams](assets/week-5/dynamoDB_streams_testing_lambda_logs.png)


## Additional Resources

### AWS DynamoBD
- [Andrew’s OmenKing Repository – Week 5 Notes](https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-5/journal/week5.md)
- [Jason Paul -  Week 5: Unofficial Homework Guide](https://www.linuxtek.ca/2023/03/19/aws-cloud-project-bootcamp-week-5-unofficial-homework-guide/)
- [Alex DeBrie – The DynamoDB Book ](https://www.dynamodbbook.com/#buy)
- [AWS DynamoDB Docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [AWS DynamoDB Guides - Youtube playlist](https://www.youtube.com/playlist?list=PL9nWRykSBSFi5QD8ssI0W5odL9S0309E2)
- [Single-table vs. multi-table design in Amazon DynamoDB](https://aws.amazon.com/blogs/database/single-table-vs-multi-table-design-in-amazon-dynamodb/)
- [DigitalCloud - Amazon DynamoDB](https://digitalcloud.training/amazon-dynamodb/)
- [The Ultimate DynamoDB Cheatsheet](https://www.freecodecamp.org/news/ultimate-dynamodb-2020-cheatsheet/)
- [Commander Docs](https://docs.getcommandeer.com/docs/DynamoDB/viewing-your-dynamodb-er-diagram/#viewing-your-dynamodb-er-diagram)
- [DynamoDB examples using SDK for Python (Boto3)](https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html)
- [Boto3 DynamoDB – Complete Tutorial](https://hands-on.cloud/boto3-dynamodb-tutorial/)
- [W3Schools - AWS Cloud Tutorial](https://www.w3schools.com/aws/aws_cloudessentials_intro.php)
- [Working with Amazon DynamoDB using Python & Boto3](https://www.coursera.org/projects/amazon-dynamodb-using-python-boto3?irclickid=VY9WzQQrDxyNUB30ibTyX2paUkAW1SSAJwPO3Y0&irgwc=1&utm_medium=partners&utm_source=impact&utm_campaign=3552020&utm_content=b2c)
- [ExamPro - AWS Developer Associate 2020 Youtube Playlist](https://www.youtube.com/playlist?list=PLBfufR7vyJJ5WuCNg2em7SgdAfjduqnNq)

### PartiQL
- [PartiQL Tutorial](https://partiql.org/tutorial.html)

### Momento Cache
- [Momento Serverless Cache](https://docs.momentohq.com/)
- [Cheat Sheet for Python with Momento Serverless Cache](https://docs.momentohq.com/develop/guides/cheat-sheets/momento-cache-python-cheat-sheet)
- [beabetterdev](https://beabetterdev.com/)

### AWS Security
- [AWS Security BootCamp 2023 Youtibe Playlist](https://www.youtube.com/playlist?list=PLrU93JvkXVl5TamdCdCwzqFs6vt5vySFi)


### Josh Hargett's Medium Blogs
- [Josh Hargett](https://medium.com/@joshhargett.jh)

I have not been writing blogs, though I have found Josh Hargett's medium blogs as a good motivator to start thinking also putting out my work out their as simple contribution to the tech community.
