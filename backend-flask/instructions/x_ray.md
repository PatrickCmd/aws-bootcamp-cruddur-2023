```sh
export AWS_REGION="us-east-1"
gp env AWS_REGION="us-east-1"
```

Create X-ray Group

```sh
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"backend-flask\")"
```

Output
```json
{
    "Group": {
        "GroupName": "Cruddur",
        "GroupARN": "arn:aws:xray:us-east-1:476313879638:group/Cruddur/ZRANGNXCHRAFR6JHO5AEECAJLXXLCFWTDZVPJ7D2JQTIHPDL6V6Q",
        "FilterExpression": "service(\"backend-flask\")",
        "InsightsConfiguration": {
            "InsightsEnabled": false,
            "NotificationsEnabled": false
        }
    }
}
```

Create X-ray Sampling rule

```sh
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```

Output
```json
{
    "SamplingRuleRecord": {
        "SamplingRule": {
            "RuleName": "Cruddur",
            "RuleARN": "arn:aws:xray:us-east-1:476313879638:sampling-rule/Cruddur",
            "ResourceARN": "*",
            "Priority": 9000,
            "FixedRate": 0.1,
            "ReservoirSize": 5,
            "ServiceName": "backend-flask",
            "ServiceType": "*",
            "Host": "*",
            "HTTPMethod": "*",
            "URLPath": "*",
            "Version": 1,
            "Attributes": {}
        },
    }
}
```