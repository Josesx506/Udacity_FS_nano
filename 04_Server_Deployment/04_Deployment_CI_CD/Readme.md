## Server Deployment
1. **01_Deploy_Flask_App** shows how to deploy a simple flask app on an EKS cluster. It creates an EKS cluster and NodeGroup.
<br><br>

2. **02_CloudFormation** shows how to create AWS stacks. A stack is a group of resources that can be either a VPC, one or more EC2 instances, S3 buckets, IAM roles, or any other AWS resource. The stacks are created using template configuration scripts that are encoded as `yml` and `json` files. After creation the stack can also be updated using the config scripts and deleted. All commands can be run from command line and verified using the Web console.
<br><br>

3. **Continuous Delivery** is used for small incremental releases or frequent releases of code. It automates code compilation, testing and packaging. It may involve human QA before final release or automated release to production. It typically automates code compilation -> testing -> packaging -> deployment. If the code is automatically deployed, it is referred to as **Continuous Deployment**. Faster releases enable quicker customer feedback. This process can be divided into two main parts namely
    - **Continuous Integration**: frequent check-ins to a central repository which trigger automated builds and tests.
    - **Continuous Deployment**: code changes to an application are released automatically into the production environment.
<br><br>

4. **04_Create_Pipeline_S3** shows how an S3 bucket can be used to build a code pipeline. An AWS stack is created and link to an S3 bucket and Docker Image. Whenever updates are made in the buid template, the CodePipeline is rebuilt. The pipeline in this chapter only echoes `Hello from Code Build!` with the docker container and the results can be viewed in the build logs.
<br><br>

5. 
<br><br>


After screen recording important videos, convert .mov to .mp4 files using `ffmpeg -i Deploy_a_Flask_Application_Manually.mov -q:v 0 Deploy_a_Flask_Application_Manually.mp4`. This re-encodes with best quaility (-qscale 0)