# Week 10 — CloudFormation Part 1

## What is AWS CloudFormation?


AWS CloudFormation is a service provided by Amazon Web Services (AWS) that allows you to model and provision AWS resources and infrastructure in an automated and scalable manner. 

Using CloudFormation, you can define and manage infrastructure as code, which allows you to declare your desired configuration in a template, and CloudFormation takes care of provisioning and configuring the necessary resources in your AWS account. 

This helps simplify the process of creating and managing infrastructure and reduces the potential for human error. CloudFormation templates can be written in `YAML` or `JSON` and can be stored in version control for easy management and collaboration. 

With CloudFormation, you can create and manage a variety of AWS resources including EC2 instances, RDS databases, S3 buckets, IAM roles, and more. You can also use CloudFormation to create, update, and delete entire stacks of resources as a single unit. 

Overall, CloudFormation helps make the process of creating and managing infrastructure more efficient and less error-prone, while also enabling greater automation and scalability in your AWS environment.

### AWS CloudFormation Templates
- [AWS CloudFormation Templates](https://aws.amazon.com/cloudformation/resources/templates/)
- [Amazon Elastic Container Service template snippets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ecs.html#quickref-ecs-example-1.yaml)

### Deploy CloudFormation template
See instructions in the [README.md](../aws/cfn/Readme.md) first.

#### Sample ECS CFN template
```yml
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster: #LogicalName
    Type: 'AWS::ECS::Cluster'
```

This CloudFormation template is written in `YAML` and is used to create an AWS ECS cluster. Here is a breakdown of the different elements in the template:

- `AWSTemplateFormatVersion: 2010-09-09`: This specifies the format version of the CloudFormation template, which is required at the top of every CloudFormation template.

- `Description: |`: This is a description of the CloudFormation stack. The pipe symbol indicates that the description spans multiple lines.

- `Setup ECS Cluster`: This is the text of the description. It indicates that the CloudFormation stack is being used to set up an ECS cluster.

- `Resources:`: This is the start of the CloudFormation resources section, which lists the AWS resources that will be created when the stack is created.

- `ECSCluster:`: This is a logical name for the ECS cluster resource. Logical names are used within the CloudFormation template to refer to specific resources.

- `Type: 'AWS::ECS::Cluster'`: This specifies the type of resource that will be created, in this case, an AWS ECS cluster. The `AWS::ECS::Cluster` type is used to create a logical grouping of container instances that can be used to run tasks and services.

In summary, this CloudFormation template defines an AWS ECS cluster resource with the logical name `ECSCluster`. When the CloudFormation stack is created, this resource will be provisioned in the AWS account.

#### Cluster deploy

```sh
./bin/cfn/cluster-deploy
```

![CloudFormation](assets/week-10/cloudformation-1.png)

![CloudFormation](assets/week-10/cloudformation-2-review.png)

![CloudFormation](assets/week-10/cloudformation-3-change-sets.png)

![CloudFormation](assets/week-10/cloudformation-3-change-sets-details.png)

![CloudFormation](assets/week-10/cloudformation-3-execute-change-sets.png)

![CloudFormation](assets/week-10/cloudformation-4-events.png)

![CloudFormation](assets/week-10/cloudformation-5-resources.png)

![CloudFormation](assets/week-10/cloudformation-6-created-ecs-cluster.png)

#### Test Modifying cluster name and deploy

```yml
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster: #LogicalName
    Type: 'AWS::ECS::Cluster'
    Properties:
      ClusterName: CruddurCluster
```

![CloudFormation](assets/week-10/cloudformation-7-modify-change-set.png)

![CloudFormation](assets/week-10/cloudformation-8-modification-change-events.png)

![CloudFormation](assets/week-10/cloudformation-9-modification-resource-name-change.png)

![CloudFormation](assets/week-10/cloudformation-10-new-ecs-cluster-created.png)

#### Checking deployment errors
IF errors do occur or a deployment fails when change set is executed, do check out `cloudtrail Event History` to track down the error.

#### CloudFormation Linting - Validate CFN template for errors
We can validate a cloudformation template for errors.

```sh
aws cloudformation validate-template --template-body file:///workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml
```

**Sample output  with no errors**
```json
{
    "Parameters": [],
    "Description": "Setup ECS Cluster\n"
}
```

OR: We can also use cfn-lint. See how to setup `cfn-lint` [here - cfn-lint](https://github.com/aws-cloudformation/cfn-lint)

#### Install
#### Pip
```sh
pip install cfn-lint. 
```

If pip is not available, run python setup.py clean --all then python setup.py install.

#### Homebrew (macOS)
```sh
brew install cfn-lint
```

#### Basic Usage
- `cfn-lint template.yaml`
- `cfn-lint -t template.yaml`

Test linting with our cfn template

```sh
cfn-lint /workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml
```

No output if there is no error

### AWS CloudFormation Integration & Automation
A deep dive into testing with TaskCat
- [TaskCat Github](https://github.com/aws-ia/taskcat)
- [TaskCat Documentation](https://aws-ia.github.io/taskcat/)

### AWS CloudFormation Guard - Policy-as-code
- [AWS CloudFormation Guard Docs](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html)
- [AWS CloudFormation Guard - Github](https://github.com/aws-cloudformation/cloudformation-guard)

**Validate Cloud Environments with Policy-as-Code**

AWS CloudFormation Guard is an open-source general-purpose policy-as-code evaluation tool. It provides developers with a simple-to-use, yet powerful and expressive domain-specific language (DSL) to define policies and enables developers to validate JSON- or YAML- formatted structured data with those policies.

#### Setting up AWS CloudFormation Guard
See resources here
- [AWS](https://docs.aws.amazon.com/cfn-guard/latest/ug/setting-up.html)
- [AWS CloudFormation Guard - Github](https://github.com/aws-cloudformation/cloudformation-guard#guard-cli)

```sh
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/aws-cloudformation/cloudformation-guard/main/install-guard.sh | sh
export PATH=~/.guard/bin:$PATH
cfn-guard --version
gem install cfn-toml
```

#### [How does Guard CLI work?](https://github.com/aws-cloudformation/cloudformation-guard#how-does-guard-cli-work)
The two common Guard CLI commands are `validate` and `test`.

**Generate rule**
- Autogenerate rules from an existing JSON- or YAML- formatted data. (Currently works with only CloudFormation templates)

```sh
cfn-guard rulegen --template /workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml > /workspace/aws-bootcamp-cruddur-2023/aws/cfn/ecs-cluster.guard
```

**Validate**
- Validate command is used when you need to assess the compliance or security posture as defined by a set of policy files against incoming JSON/YAML data. Common data payloads used are CloudFormation Templates, CloudFormation ChangeSets, Kubernetes Pod policies, Terraform Plan/Configuration in JSON format, and more. 

```sh
cfn-guard validate -r /workspace/aws-bootcamp-cruddur-2023/aws/cfn/ecs-cluster.guard
```

**Test**
- Test command is used during the development of guard policy rules files. Test provides a simple integrated unit-test frameworks that allows authors to individually test each policy file for different types of inputs. Unit testing helps authors gain confidence that the rule does indeed conform to expectations. It can also be used as regression tests for rules.

```sh
cfn-guard test -r /workspace/aws-bootcamp-cruddur-2023/aws/cfn/ecs-cluster.guard -t /workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml
```
