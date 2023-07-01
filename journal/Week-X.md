# Snyc tool for static website hosting

**Resource video**: [Wee X Sync tool for static website hosting](https://www.youtube.com/watch?v=0nDBqZGu4rI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=115)

Follow the instructions [here](https://github.com/teacherseat/aws-s3-website-sync) on how to install the **AWS S3 Website Sync** tool and use it to sync the directory for static webhosting with **AWS S3**

## Create Gemfile and install
Create a `Gemfile` that installs the gem:

```rb
source 'https://rubygems.org'

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end

gem 'rake'
gem 'aws_s3_website_sync', tag: '1.0.1'
gem 'dotenv', groups: [:development, :test]
```

The proceed to install the required gems:

```sh
bundle install
```


Remember to have the following environment variables set

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
SYNC_S3_BUCKET
SYNC_CLOUDFRONT_DISTRUBTION_ID
SYNC_BUILD_DIR
SYNC_OUTPUT_CHANGESET_PATH
SYNC_AUTO_APPROVE
```

For this project, we can generate the `SYNC` environment variables with the command

```sh
ruby "$THEIA_WORKSPACE_ROOT/bin/frontend/generate-env"
```

Now run static build and sync to AWS S3 and follow the prompts to complete the sync.

```sh
./bin/frontend/static-build
```

```sh
./bin/frontend/sync
```

## Create GithubOidc Identity Provider and Cruddur Sync Role

See cloudformation template [here](../aws/cfn/sync/template.yaml)

To create provider and role, run the deploy script as below

```sh
./bin/cfn/sync-deploy
```
