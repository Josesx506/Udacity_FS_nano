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

    You can view the cluster in the EKS cluster dashboard. If you don’t see any progress, be sure that you are viewing clusters in the same region that they are being created. <br>
    **Note**: Use a consistent `kubectl` version in your EKS Cluster, local machine, and later in the Codebuild's buildspec.yml file.

2. **Verify** - After creating the cluster, check the health of your clusters nodes: <br>
    `kubectl get nodes`

3. **Delete when the project is over** - Remember, in case you wish to delete the cluster, you can do it using eksctl: <br>
    `eksctl delete cluster simple-jwt-api  --region=us-east-2` <br>
    This deletion step is crucial after you receive your project feedback.


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


### 4. Deployment to Kubernetes using CodePipeline and CodeBuild

3. **Save a Secret in AWS Parameter Store** <br>
    You app running in the EKS cluster will need a secret text string for creating the JWT (Remember the `/auth` endpoint?). We need a way to pass your text secret to the app in kubernetes securly. You will be using [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) to do this.<br>
    
    Run this command from the project home directory to put secret into AWS Parameter Store
    ```bash
    ~ $aws ssm put-parameter --name JWT_SECRET --overwrite --value "myjwtsecret" --type SecureString
    # Verify
    ~ $aws ssm get-parameter --name JWT_SECRET
    # Once you submit your project and receive the reviews, you can consider deleting the variable from parameter-store using:
    ~ $aws ssm delete-parameter --name JWT_SECRET
    ```

6. **The working project** <br>
    dfgfre

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