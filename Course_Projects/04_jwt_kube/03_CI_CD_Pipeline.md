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

***

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

    You can view the cluster in the EKS cluster dashboard. If you don’t see any progress, be sure that you are viewing clusters in the same region that they are being created. <br>
    **Note**: Use a consistent `kubectl` version in your EKS Cluster, local machine, and later in the Codebuild's buildspec.yml file.

2. **Verify** - After creating the cluster, check the health of your clusters nodes: <br>
    `kubectl get nodes`

3. **Delete when the project is over** - Remember, in case you wish to delete the cluster, you can do it using eksctl: <br>
    `eksctl delete cluster simple-jwt-api  --region=us-east-2` <br>
    This deletion step is crucial after you receive your project feedback.

***

### 2. Create an IAM Role for CodeBuild
You will need an **IAM role that the CodeBuild will assume to access your EKS cluster**. In the previous lesson, you have already created such an IAM role with a custom trust-relationship and a policy. In case you have deleted that role, you can follow the steps below to quickly set up an IAM role. Otherwise, you can ignore the current step. <br>
1. Get your AWS account id:
    ```bash
    ~ $aws sts get-caller-identity --query Account --output text
    # Returns the AWS account id similar to 
    # 519002666132
    ```
2. Update the `backend/trust.json` file with your AWS account id.
    ```bash
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<ACCOUNT_ID>:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
    }
    ```
    **Replace the <ACCOUNT_ID> with your actual AWS account ID.**
    <br>

3. Create a role, **'UdacityFlaskDeployCBKubectlRole'**, using the trust.json trust relationship:
    ```bash
    ~ $aws iam create-role --role-name UdacityFlaskDeployCBKubectlRole --assume-role-policy-document file://trust.json --output text --query 'Role.Arn'
    # Returns something similar to 
    arn:aws:iam::519002666132:role/UdacityFlaskDeployCBKubectlRole
    ```
4. Policy is also a JSON file where we will define the set of permissible actions that the Codebuild can perform. <br>
    We have given you a policy file, `backend/iam-role-policy.json`, containing the following permissible actions: "eks:Describe*" and "ssm:GetParameters".
    ```bash
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:Describe*",
                "ssm:GetParameters"
            ],
            "Resource": "*"
        }
    ]
    }
    ```
5. Attach the *iam-role-policy.json* policy to the 'UdacityFlaskDeployCBKubectlRole' as:
    ```bash
    ~ $aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file://iam-role-policy.json
    ```

***

### 3. Authorize the CodeBuild using EKS RBAC
**You will have to repeat this step every time you create a new EKS cluster.** <br>
For the CodeBuild too administer the cluster, you will have to add an entry of this new role into the [aws-auth ConfigMap](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html). The aws-auth ConfigMap is used to grant role-based access control to your cluster.
1. **Fetch** - Get the current configmap and save it to a file:
    ```bash
    # Mac/Linux - The file will be created at `/System/Volumes/Data/private/tmp/aws-auth-patch.yml` path
    ~ $kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml
    # Windows - The file will be created in the current working directory
    ~ $kubectl get -n kube-system configmap/aws-auth -o yaml > aws-auth-patch.yml
    ```
2. **Edit** - Open the aws-auth-patch.yml file using any editor, such as VS code editor:
    ```bash
    # Mac/Linux
    ~ $code /System/Volumes/Data/private/tmp/aws-auth-patch.yml
    # Windows
    ~ $code aws-auth-patch.yml
    ```
    Add the following group in the **data → mapRoles** section of this file. YAML is indentation-sensitive, therefore refer to the snapshot below for a correct indentation:
    ```bash
    - groups:
        - system:masters
        rolearn: arn:aws:iam::<ACCOUNT_ID>:role/UdacityFlaskDeployCBKubectlRole
        username: build
    ```
    Don't forget to replace the `<ACCOUNT_ID>` with your AWS account Id. Do not copy-paste the code snippet from above. Instead, look at this sample [aws-auth-patch.yml](https://github.com/udacity/cd0157-Server-Deployment-and-Containerization/blob/master/aws-auth-patch.yml) file and the snapshot below to stay careful with the indentations.
3. **Update** - Update your cluster's configmap:
    ```bash
    # Mac/Linux
    ~ $kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
    # Windows
    ~ $kubectl patch configmap/aws-auth -n kube-system --patch "$(cat aws-auth-patch.yml)"
    ```
    The command above must show you `configmap/aws-auth patched` as a response.
4. **Troubleshoot** - In case of the following error, re-run the above three steps beginning from the `kubectl get` command. <br>
Error from server (Conflict): Operation cannot be fulfilled on configmaps "aws-auth": the object has been modified; please apply your changes to the latest version and try again

5. Check the health of your clusters nodes: `kubectl get nodes`

***

### 4. Deployment to Kubernetes using CodePipeline and CodeBuild
1. **Generate a Github access token** <br>
    A Github access token will allow Codebuild to monitor when a repo is changed. A token is analogous to your Github password and can be generated [here](https://github.com/settings/tokens/).

2. **Create Codebuild and CodePipeline resources using CloudFormation template** <br>
    Modify the template file provided in `backend/ci-cd-codepipeline.cfn.yml`. This is the template file that you will use to create your CodePipeline pipeline and CodeBuild project. Navigate to the **Parameters** section.

    |Parameter | Possible Value| 
    | ---      |   ---         |
    | `EksClusterName` | `simple-jwt-api` # Name of the EKS cluster you created | 
    | `GitSourceRepo` | `udy_Server_Deployment_and_Containerization` # Github repo name| 
    | `GitBranch` | `master` # Or any other you want to link to the Pipeline| 
    | `GitHubUser` | `Josesx506` # Your Github username | 
    | `KubectlRoleName` | `UdacityFlaskDeployCBKubectlRole` # We created this role earlier |

    Do not use any quotes in your values. <br><br>

    Review the resources that will be created. The Cloudformation template file will create the following resources:
    - ECR repository to store your Docker image.
    - S3 bucket to store your Pipeline artifacts
    - A few IAM roles that individual services will assume
    - A Lambda function
    - CodeBuild and CodePipeline resources

    <br>

    Create a **Stack** using the template file in the AWS web-console and include the git access token generated in *step 1* of this section. Verify that the input like the git username and repository are correction configured, and leave the default argument for the remaining input fields.<br>

    If there is an indentation error in your YAML template file, the CloudFormation will raise a "Template format error". In such a case, you will have to identify the line of error in the template, using any external tools, such as - [YAML Validator](https://codebeautify.org/yaml-validator) or [YAML Lint](http://www.yamllint.com/).


3. **Save a secret key as an environment variable in AWS Parameter Store** <br>
    You app running in the EKS cluster will need a secret text string for creating the JWT (Remember the `/auth` endpoint?). We need a way to pass your text secret to the app in kubernetes securly. You will be using [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) to do this.<br>
    
    Run this command from the project home directory to put secret into AWS Parameter Store
    ```bash
    ~ $aws ssm put-parameter --name JWT_SECRET --overwrite --value "myjwtsecret" --type SecureString
    # Verify
    ~ $aws ssm get-parameter --name JWT_SECRET
    # Once you submit your project and receive the reviews, you can consider deleting the variable from parameter-store using:
    ~ $aws ssm delete-parameter --name JWT_SECRET
    ```

4. **How does CodeBuild know the build steps?** <br>
    In the previous step, the CloudFormation template file, `backend/ci-cd-codepipeline.cfn.yml`, will automatically create a CodeBuild resource. When the **build is triggered**, Codebuild will execute the commands/steps mentioned in the `backend/buildspec.yml` file. *As per AWS documentation, a buildspec is a collection of build commands and related settings, in YAML format, that CodeBuild uses to run a build.* The *buildspec.yml* file must be placed in the root of your source directory (Github repo). <br>

    Use the same (or within one minor version difference) KUBECTL version as you've used while creating an EKS cluster. Refer to the [AWS docs](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html) or [k8s docs](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) to see the available versions for Linux machines (our Codebuild will use Linux containers internally to run build commands!). <br>

    **Note** - You must use a kubectl version within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.27 kubectl client works with Kubernetes 1.26, 1.27, and 1.28 clusters. <br>

    Also, ensure that the following code is present at the end of the buildspec.yml file:
    ```bash:
    env:
      parameter-store:         
        JWT_SECRET: JWT_SECRET
    ```
    This lets CodeBuild know to set an environment variable based on a value in the parameter-store.

    <br><br>

    The buildspec.yml file specifies the different phases of a build, such as an install, pre-build, build, and post-build. Each phase has a set of commands to be automatically executed by CodeBuild.
    - *install* phase: Install Python, pip, kubectl, and update the system path
    - *pre-build* phase: Log into the ECR repo where the Codebuils will push the Docker image.
    - *build* phase: Build a Docker image
    - *post-build* phase: Push the Docker image to the ECR repo, update the EKS cluster's kubeconfig, and apply the configuration defined in the simple_jwt_api.yml to the cluster.

    You can see each command being executed in the CodeBuild log console when you trigger a build.

5. **Troubleshoot - How to debug a failed build?** <br>
    When a build fails, you can look at the logs to see the errors. Here is a popular error: <br>
    
    Error: You must be logged in to the server (the server has asked for the client to provide credentials)

    The error above infers that the Codebuild could not log into the cluster, possibly because Codebuild does not have sufficient permissions to perform the logging action. In this case, you should check and re-update the cluster's ConfigMap as:
    ```bash
    # Download a fresh copy of the configmap
    # You can choose a different path or current working directory to save the  auth-patch.yml
    ~ $kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml
    # Open the configmap in an editor, and update the **data --> mapRoles** section as described earlier while creating the cluster
    # Update the configmap
    ~ $kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
    ```
    <br>

    Another prevalent error is: <br>

    Build failed to start. The following error occurred: ArtifactsOverride must be set when using artifacts type CodePipelines <br>

    The error above could be due to the incorrect parameters used in the `backend/ci-cd-codepipeline.cfn.yml` file. To verify the existing parameters, look at the CloudFormation console → your Stack → Stack parameters.

6. **The working project** <br>
    You will not be able to trigger a manual build because the Codebuild is set to use the CodePipeline artifact. Triggering it manually may lead to this error: <br>

    Build failed to start. The following error occurred: ArtifactsOverride must be set when using artifacts type CodePipelines <br>

    A workaround for a manual build is: Go to the CodePipeline console → your Pipeline → click on the Release change button. However, we recommend the automatic builds. Try the steps below to test the automatic builds:

    1. **Push a commit** - To check if the pipeline works, Make a git push to your repository to trigger an automatic build.

    2. **Verify** - In the AWS console go to the [CodePipeline dashboard](https://console.aws.amazon.com/codesuite/codepipeline/start?region=us-east-2). You should see that the build is running, and it should succeed.

    3. **Test your Endpoint** - To test your API endpoints, get the external IP for your service:
        ```bash
        ~ $kubectl get services simple-jwt-api -o wide
        # Output
        NAME             TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)        AGE     SELECTOR
        simple-jwt-api   LoadBalancer   10.100.137.77   ae9e93acc42e54b61a47209653be30e2-644140318.us-east-2.elb.amazonaws.com   80:31188/TCP   3m44s   app=simple-jwt-api
        ```
        Now use the external IP url to test the app:
        ```bash
        # Wildcard
        ~ $export TOKEN=`curl -d '{"email":"<EMAIL>","password":"<PASSWORD>"}' -H "Content-Type: application/json" -X POST <EXTERNAL-IP URL>/auth  | jq -r '.token'`
        ~ $curl --request GET '<EXTERNAL-IP URL>/contents' -H "Authorization: Bearer ${TOKEN}" | jq
        
        # Actual implementation
        ~ $export TOKEN=`curl -d '{"email":"abc@xyz.com","password":"WindowsPwd"}' -H "Content-Type: application/json" -X POST http://ae9e93acc42e54b61a47209653be30e2-644140318.us-east-2.elb.amazonaws.com/auth  | jq -r '.token'`
        ~ $curl --request GET 'http://ae9e93acc42e54b61a47209653be30e2-644140318.us-east-2.elb.amazonaws.com/contents' -H "Authorization: Bearer ${TOKEN}" | jq
        ```

***

### 5. Adding Tests to the Build
The final part of this project involves adding tests to your deployment. You can follow the steps below to accomplish this.

1. Add running tests as part of the build. To require the unit tests to pass before our build will deploy new code to your cluster, you will add the tests to the build stage. Remember you installed the requirements and ran the unit tests locally at the beginning of this project. You will add the same commands to the buildspec.yml:
    - Open *buildspec.yml*
    - In the prebuild section, add a line to install the requirements and a line to run the tests. You may need to refer to 'pip' as 'pip3' and 'python' as 'python3', as:
        ```bash
        pre_build:
        commands:
            - echo 'Starting unit tests'
            - pip3 install -r requirements.txt 
            - python -m pytest test_main.py
        ```
    - Save the file
2. You can check the tests prevent a bad deployment by breaking the tests on purpose:
    - Open the *test_main.py* file
    - Add assert False to any of the tests
    - Commit your code and push it to Github
    - Check that the build fails in CodePipeline

***

### 6. Clean up
Remove all running kubernetes clusters, nodeGroups, stacks, unused roles, VPCs, s3 buckets, and environment variables.

```bash
# I started with deleting the stack
~ $aws cloudformation delete-stack --stack-name simple-jwt-api

# Get deployment name
~ $kubectl get deployments
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
simple-jwt-api   3/3     3            3           167m

# Delete the kubernetes deployments
~ $kubectl delete deployments/simple-jwt-api
deployment.apps "simple-jwt-api" deleted

# Get the cluster name
~ $eksctl get cluster
NAME            REGION          EKSCTL CREATED
simple-jwt-api  us-east-2       True

# Tear down the cluster - This takes a while and generates a lot of output text
~ $eksctl delete cluster simple-jwt-api
2023-12-25 00:00:37 [ℹ]  deleting EKS cluster "simple-jwt-api"

# Delete the environment variable from parameter-store
~ $aws ssm delete-parameter --name JWT_SECRET
```

- S3 buckets were manually emptied and deleted using the AWS web console.
- `UdacityFlaskDeployCBKubectlRole` IAM role was manually deleted
- `eksctl-simple-jwt-api-cluster/VPC` VPC was manually deleted. Associated subnets were also deleted.