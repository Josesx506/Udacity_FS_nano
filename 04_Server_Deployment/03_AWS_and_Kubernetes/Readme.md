## AWS and Kubernetes
In the big picture 
1. A production repo is created first
2. Each time a commit is made to the repo, AWS CodeBuild and CodePipeline are used for automated compilation and testing.
    - This forms the bulk of the Continuous Integration / Continuous Delivery (CI/CD) pipeline
3. The compiled application is then passed on to a Kubernetes cluster for scaling
4. Consumers can access the final software application hosted on the Kube cluster.
<br>

Major AWS services that will be used include:
- Elastic Kubernetes Service
    - IAM
    - EC2
- CloudFormation
    - IAM
    - S3 (Amazon Simple Storage Service)
    - ECR

### S3 Buckets
- Create a public S3 bucket in the AWS console.
    - Region: us-east-1
    - Name: udy-fsnd-jo-aws-001
    - Object Ownership: ACLs enabled & Bucket owner preferred
    - Block Public Access settings for this bucket: False. Public access is enabled.
        - Also acknowledge the checkbox that the items of the bucket can be public
    - All remaining settings are left as default.

- Upload the `sample.html` into the bucket and set the object to public on the S3 dashbord. *<b>Note:</b> Enabling public access to the bucket doesn't automatically provide access to each file. Individual public access will have to be defined for each file*
    - Click on [Object Actions] -> [Make public using ACL] -> [Make Public].
        - Now you can access the html file using the public custom s3 link for the file `https://udy-fsnd-jo-aws-001.s3.amazonaws.com/sample.html`
    - You can `delete` the bucket after this first test. *<b>Note:</b> The bucket has to be emptied before it can be deleted*

**For this chapter, S3 buckets and EC2 instances will not be created manually. Other AWS services will be used to automatically create both services.**

Configure request limit for websites to enhance security against brute force attacks


