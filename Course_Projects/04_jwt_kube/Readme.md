##
The app is a simple flask app that shows how to encode and decode tokens using json web tokens (jwts).

```bash
.
├── Dockerfile
├── aws-auth-patch.yml           # TODO - A sample EKS Cluster configMap file. 
├── ci-cd-codepipeline.cfn.yml   # TODO - YAML template to create CodePipeline pipeline and CodeBuild resources
├── buildspec.yml
├── simple_jwt_api.yml
├── trust.json                   # TODO - Used for creating an IAM role for Codebuild
├── iam-role-policy.json    
├── main.py				 
├── requirements.txt		
└── test_main.py                 # TODO - Unit Test file
```

https://115046250033.signin.aws.amazon.com/console