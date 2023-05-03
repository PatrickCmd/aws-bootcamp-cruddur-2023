# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## The steps to create an AWS CodePipeline that uses GitHub as the source, AWS CodeBuild in the build stage, and deploys to AWS ECS using AWS management console:

1. Sign in to the AWS Management Console and navigate to the AWS CodePipeline console.

2. Click on the "Create pipeline" button to create a new pipeline.

3. In the "Pipeline settings" page, enter a name for the pipeline and select the "GitHub" option as the source provider.

4. Connect your GitHub account and select the repository and branch you want to use as the source for the pipeline.

5. Click on the "Next" button to configure the build stage.

6. In the "Build provider" section, select "AWS CodeBuild" as the build provider and choose a CodeBuild project you have already created or create a new one.

7. Configure the build settings as necessary, including the build environment, build commands, and environment variables.

8. Click on the "Next" button to configure the deployment stage.

9. In the "Deployment provider" section, select "Amazon ECS" as the deployment provider.

10. Choose the ECS cluster and service you want to deploy to and configure the deployment settings as necessary, including the container name and image.

11. Click on the "Next" button to review and create the pipeline.

12. Review the pipeline settings and click on the "Create pipeline" button to create the pipeline.

Your AWS CodePipeline that uses GitHub as the source, AWS CodeBuild in the build stage, and deploys to AWS ECS is now ready to use. You can start the pipeline manually or configure it to start automatically when changes are made to the source code in the GitHub repository.