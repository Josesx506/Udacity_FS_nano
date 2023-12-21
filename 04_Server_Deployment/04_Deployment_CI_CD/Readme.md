### AWS Cloud Formation
1. **01_Deploy_Flask_App** shows how to deploy a simple flask app on an EKS cluster. It creates an EKS cluster and NodeGroup.
2. **02_CloudFormation** shows how to create AWS stacks. A stack is a group of resources that can be a VPC, one or more EC2 instances, S3 buckets, IAM roles, or any other AWS resource. The stacks are created using template configuration scripts that are encoded as `yml` and `json` files. After creation the stack can also be updated using the config scripts and deleted. All commands can be run from command line and verified using the Web console.



After screen recording important videos, convert .mov to .mp4 files using `ffmpeg -i Deploy_a_Flask_Application_Manually.mov -q:v 0 Deploy_a_Flask_Application_Manually.mp4`. This re-encodes with best quaility (-qscale 0)