## Run the app on AWS Cloud

This section of the project aims to create a CI/CD pipeline. The steps you will follow are:
#### 1. Create an EKS Cluster, IAM Role for CodeBuild, and Authorize the CodeBuild
1. **Create an EKS Cluster** - Start with creating an EKS cluster in your preferred region, using `eksctl` command.
2. **IAM Role for CodeBuild** - Create an IAM role that the Codebuild will assume to access your k8s/EKS cluster. This IAM role will have the necessary access permissions (attached JSON policies),
3. **Authorize the CodeBuild using EKS RBAC** - Add IAM Role to the Kubernetes cluster's configMap.


### 2. Deployment to Kubernetes using CodePipeline and CodeBuild
1. **Generate a Github access token** <br>
    Cenerate an access-token from your Github account. We will share this token with the Codebuild service so that it can listen to the the repository commits.
2. **Create Codebuild and CodePipeline resources using CloudFormation template** <br>
    Create a pipeline watching for commits to your Github repository using Cloudformation template (.yaml) file.
3. **Set a Secret using AWS Parameter Store** <br>
    In order to pass your JWT secret to the app in Kubernetes securely, you will set the JWT secret using AWS parameter store.
4. **Build and deploy** <br>
    Finally, you will trigger the build based on a Github commit.


## Implementation
### Prerequisite
You must have the following:
1. AWS CLI installed and configured using the `aws configure` command.
2. The EKSCTL and KUBECTL command-line utilities installed in your system. Check and note down the KUBECTL version, using: <br>
    `kubectl version` <br>
    **Note** - You must use a kubectl version within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.21 kubectl client works with Kubernetes 1.20, 1.21, and 1.22 clusters.
3. You current working directory must be: <br>
    `cd cd0157-Server-Deployment-and-Containerization`

### 1. Create an EKS (Kubernetes) Cluster
1. **Create** - Create an EKS cluster named “simple-jwt-api” in a region of your choice: <br>
    `eksctl create cluster --name simple-jwt-api --nodes=2 --version=1.28 --instance-types=t2.medium --region=us-east-2` <br>
    **Known Issue** - If your default region is us-east-1, then the cluster creation may fail. <br>
    The command above will take a few minutes to execute, and create the following resources:
    - EKS cluster
    - A nodegroup containing two nodes.
    
    You can view the cluster in the EKS cluster dashboard. If you don’t see any progress, be sure that you are viewing clusters in the same region that they are being created.

