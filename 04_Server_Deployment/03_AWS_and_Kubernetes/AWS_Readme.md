## Amazon Web Services (AWS)
In the big picture 
1. A production repo is created first
2. Each time a commit is made to the repo, AWS CodeBuild and CodePipeline are used for automated compilation and testing.
    - This forms the bulk of the Continuous Integration / Continuous Delivery (CI/CD) pipeline
3. The compiled application is then passed on to a Kubernetes cluster for scaling
4. Consumers can access the final software application hosted on the Kube cluster.
<br>

Major AWS services that will be used include:
- **Elastic Kubernetes Service**
    - Identity Access Management (IAM)
    - Elastic Compute Cloud (EC2)
- **CloudFormation**
    - IAM
    - Amazon Simple Storage Service (S3)
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

### EC2 Instances
This chapter shows how to launch, shut down and terminate an EC2 instance.

**For this chapter, S3 buckets and EC2 instances will not be created manually. Other AWS services will be used to automatically create both services.**

### IAM
```bash
.
└── User Groups (Group of Users with same level of permissions)
    └── Users (A user can have multiple roles)
        └── Roles (Each Role can have multiple policies)
        │   └── Policies (Define user permission in JSON format)
        └── Identity Providers
```
An example IAM policy was created for an S3 bucket which allowed list and GetObject access. <br>

***
An IAM User with admin access was created for accessing the services from AWS CLI using the *v2*.
1. Install awscli v2 with instructions from https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html.
2. Generate a user under **IAM Users** with **Admin** access and generate an **access key** for the User.
3. Configure the cli with the access key id and secret in terminal. Use `us-east-2` as the default region because east-1 has some issues with kubernetes
    ```bash
    ~ $aws configure
    AWS Access Key ID [****************3PCQ]: ********
    AWS Secret Access Key [****************x1dJ]: ********
    Default region name [us-west-1]: us-east-2
    Default output format [table]: 
    ```
4. Set the session token to null to remove any pre-existing sessions. `aws configure set aws_session_token ""`. The `set` command is similar to defining an environment variable with `export`.
    - Other variables can also be defined with command line like the region `aws configure set region us-east-2`.
5. After setting up the configuration, you can test whether it's working by viewing the users or configuration.
    ```bash
    ~ $aws iam list-users
    ------------------------------------------------------------
    |                         ListUsers                        |
    +----------------------------------------------------------+
    ||                          Users                         ||
    |+------------+-------------------------------------------+|
    ||  Arn       |  arn:aws:iam::115046250033:user/joAdmin   ||
    ||  CreateDate|  2023-12-20T03:58:12+00:00                ||
    ||  Path      |  /                                        ||
    ||  UserId    |  AIDARVSKKOYY7WFTTWHHZ                    ||
    ||  UserName  |  joAdmin                                  ||
    |+------------+-------------------------------------------+|
    ~ $
    ~ $aws configure list
        Name                    Value             Type    Location
        ----                    -----             ----    --------
    profile                <not set>             None    None
    access_key     ****************7KH4 shared-credentials-file    
    secret_key     ****************i7DQ shared-credentials-file    
        region                us-east-2      config-file    ~/.aws/config
    ```
    The configuration list shows that only the default **profile** is active


***
### Create a Bucket using CLI
1. Create a public bucket in the us-east-1 region:
    ```bash
    # Bucket names are unique across the Internet, just like DNS. 
    aws s3api  create-bucket --bucket <bucketName> --acl bucket-owner-full-control --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2
    ```
    In the command above,
- `--bucket` option specifies the bucket name of your choice. It must be unique across all AWS accounts.
- `--acl` option specifies the accessibility level
- `--region` specifies the AWS region where you want to create this bucket.
- `--create-bucket-configuration`: If you want to create the bucket in the desired region outside of us-east-1, you will need something like `--region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2` which will set an appropriate LocationConstraint.<br>
Reference - [aws s3api create-bucket command](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html) 
<br><br>

2. Upload a sample file to your bucket. The command below uploads a file names `sample.html`, however, you can choose any file from your local system
    ```bash
    aws s3api put-object --bucket <bucketName> --key sample.html --body sample.html --content-type text/html
    ```
    In the command above,
- `--key` option specifies the name you want to assign to your object in the bucket
- `--body` option specifies the file name (complete path) to upload from your local system
- `--content-type` specifies the standard MIME type describing the format of the contents.
Reference [aws s3api put-object](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-object.html). After uploading the file, you may have to make it public to access it from internet. 
<br><br>

3. Verify the S3 bucket by going to the AWS web console. Alternatively, you can run `aws s3 ls` in the command line. This will show all of the S3 buckets in your account. 
<br><br>

4. Delete the bucket and its content. A bucket can only be deleted if it is empty. Therefore, first delete the `Sample.html`, and then delete the bucket, as follows:
    ```bash
    # Empty the bucket
    aws s3api delete-object --bucket <bucketName> --key sample.html
    # Delete the nucket
    aws s3api delete-bucket --bucket <bucketName>
    ```
    Reference - [aws s3api commands](https://docs.aws.amazon.com/cli/latest/reference/s3api/#available-commands)
<br><br>

5. Navigate back to the S3 dashboard (AWS web console), and verify if the bucket has been deleted successfully.



