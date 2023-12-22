## Server Deployment and Containerization

### Virtual Machines (VM) vs. Containers
This module explained the differences between both platforms. VMs use system resources and can operate multiple OS on the same machine. This makes them relatively slow and they're limited by the hardware resource specified when creating them e.g. allocated RAM. They can be managed with softwares like VMWare. An EC2 instance is another example of a VM. <br>

Containers on the other hand are more lightweight. They share the same OS kernel and can start faster when launched. They are however limited to the OS type of the host system, but they are restricted to specified system resources like  VMs e.g. A container can use 60% RAM while a VM is locked to the allocated RAM when it was created like 20%. Containers are popularly developed by Docker and can be scaled across cloud platforms using Kubernetes.
<br><br>


### Containers
Creating Dockerfiles, building the files to docker images, and running the images as containers. The chapter showed how to build images from scratch and run them as containers.
<br><br>


### AWS and Kubernetes
Creating S3 buckets and EC2 instances from command line. Creating kubernetes clusters and Node Groups. Creating AWS stacks which can be any type of AWS resources. Use template files to create AWS resources from command line
<br><br>


### Deployment using CI/CD
Learn how to integrate all the concepts from previous chapters for production. Code is compiled within docker containers, Authentication is created with IAM roles and permissions and EC2 instances are used to create public endpoints. Automated CI/CD involves tracking an S3 bucket or git repository for changes and automatically build a pipeline where the web application can be accessed using template files, AWS CodeBuild, and AWS CodePipeline.
<br><br>

***
<br>

***
<br>

Throughout this module, I learned about the following concepts:
- Kubernetes: A container orchestration system
- EKS: Kubernetes as a service
- awscli: a command line tool for interacting with AWS services
- eksctl: a command line tool for creating EKS clusters and their associated services
- kubectl: a command line tool for interfacing with a Kubernetes cluster
- Continuous Delivery: A software deployment practice involving Continuous Integration along with automated deployments
- Continuous Integration: A development practice combining pushing frequent small code changes alone with automated testing and build
- CodePipeline: An AWS service for designing and running continuous delivery pipelines
- CodeBuild: An AWS service for implementing continuous integration