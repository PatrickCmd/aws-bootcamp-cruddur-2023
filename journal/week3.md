# Week 3 — Decentralized Authentication

## Setting up AWS Cognito and AWS User Pool via Web Console

![AWS Cognito](assets/week-3/aws_cognito_1.png)

![AWS Cognito](assets/week-3/aws_cognito_2.png)

![AWS Cognito](assets/week-3/aws_cognito_3.png)

![AWS Cognito](assets/week-3/aws_cognito_4.png)

![AWS Cognito](assets/week-3/aws_cognito_5.png)

![AWS Cognito](assets/week-3/aws_cognito_6.png)

![AWS Cognito](assets/week-3/aws_cognito_7.png)

![AWS Cognito](assets/week-3/aws_cognito_8.png)

![AWS Cognito](assets/week-3/aws_cognito_9.png)

![AWS Cognito](assets/week-3/aws_cognito_10.png)

![AWS Cognito](assets/week-3/aws_cognito_11.png)

![AWS Cognito](assets/week-3/aws_cognito_12.png)

![AWS Cognito](assets/week-3/aws_cognito_13.png)

![AWS Cognito](assets/week-3/aws_cognito_14.png)

![AWS Cognito](assets/week-3/aws_cognito_15.png)

![AWS Cognito](assets/week-3/aws_cognito_16.png)

![AWS Cognito](assets/week-3/aws_cognito_17.png)


Export these environment variables and also export them to the gitpod environment.

```sh
export AWS_USER_POOL_ID="us-east-1_ZpwVxxxx"
export AWS_APP_CLIENT_ID="40th30ihk7eoo34augvxxxxxxx"
gp env AWS_USER_POOL_ID=${AWS_USER_POOL_ID}
gp env AWS_APP_CLIENT_ID=${AWS_APP_CLIENT_ID}
```

Add the environment variables to the `frontend-react-js` service in the `docker-compose` file.

```sh
REACT_APP_AWS_PROJECT_REGION: ${AWS_DEFAULT_REGION}
REACT_APP_AWS_COGNITO_REGION: ${AWS_DEFAULT_REGION}
REACT_APP_AWS_USER_POOLS_ID: ${AWS_USER_POOL_ID}
REACT_APP_CLIENT_ID: ${AWS_APP_CLIENT_ID}
REACT_APP_AWS_USER_POOLS_WEB_CLIENT_ID: ${AWS_APP_CLIENT_ID}
```

Force password change AWS Cognito via aws cli

```sh
aws cognito-idp admin-set-user-password \
  --user-pool-id ${AWS_USER_POOL_ID} \
  --username patrickcmd \
  --password <password> \
  --permanent
```