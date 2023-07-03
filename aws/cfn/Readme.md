## Architecture Guide

Before you run any templates, be sure to create an S3 bucket to contain
all of our artifacts for CloudFormation.

```
aws s3 mb s3://cfn-artifacts-cmd-1001
export CFN_BUCKET="cfn-artifacts-cmd-1001"
gp env CFN_BUCKET="cfn-artifacts-cmd-1001"

aws s3 mb s3://codepipeline-cruddur-artifacts-cmd-1001
export ArtifactBucketName="codepipeline-cruddur-artifacts-cmd-1001"
gp env ArtifactBucketName="codepipeline-cruddur-artifacts-cmd-1001"

aws s3 mb s3://www.cruddurcorecodecmdsystems.website
export WwwBucketName="www.cruddurcorecodecmdsystems.website"
gp env WwwBucketName="www.cruddurcorecodecmdsystems.website"

aws s3 mb s3://cruddurcorecodecmdsystems.website
export RootBucketName="cruddurcorecodecmdsystems.website"
gp env RootBucketName="cruddurcorecodecmdsystems.website"
```

> remember bucket names are unique to the provide code example you may need to adjust
