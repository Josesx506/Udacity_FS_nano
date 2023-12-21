## Setup an EKS Cluster with Web Console

### 1. Prerequesites
1. Go to the **VPC** service and ensure that you have at least one default *VPC* and a *subnet* asscoiated with it.
    - Make sure `Enable auto-assign public IPv4 address` is toggled **`ON`** for each subnet for this exercise
2. Go to the **IAM** service to ensure that there are two *roles*. One for the *cluster* and one for the *node group*
    - Create a new role for the **cluster** with 
        ```bash
        Trusted Entity Type: "AWS Service"
        Use Case: "EKS"
            Choose a use case for a specified service: "EKS-Cluster"
        
        [NEXT] -> 
        The permission is automatically assigned as 
        Permission policy: "AmazonEKSClusterPolicy"

        [NEXT] -> 
        Role name: "jo-udy-fsnd-eks-clusterRole-001"
        Description: "Allows access to other AWS service resources that are required to operate clusters managed by EKS."
        Review the "trusted entity" and "service", and ignore the "tags"
        [Create role]
        ```
    - Create a new role for the **node group** with 
        ```bash
        Trusted Entity Type: "AWS Service"
        Use Case: "EC2"

        [NEXT] -> 
        Search for these keys "eksworker","ec2container","eks_cni" and select the permissions below
        Permission policy: ["AmazonEKSWorkerNodePolicy",
                            "AmazonEC2ContainerRegistryReadOnly",
                            "AmazonEKS_CNI_Policy"] 
        
        [NEXT] -> 
        Role name: "jo-udy-fsnd-eks-workerNodeRole-001"
        Description: "Allows EC2 instances to call AWS services on your behalf.."
        Review the "trusted entity" and "service", and ignore the "tags"
        [Create role]
        ```
3. Go to the **EC2** service to create an ssh key pair. 
    - Change region to `us-east-2`
    - Navigate to `Network and Security -> "Key Pairs"` tab
    - Create a new **key pair**.
        ```bash
        name: "jo-udy-fsnd-eks-keyPair"
        Key pair type: "RSA"
        Private key file format: ".pem" # For mac and linux users
        ```

### 2. Creating an EKS Cluster
Navigate to **Elastic Kubernetes Service (Amazon EKS)** from the console <br>
Click on `Add Cluster -> Create`
```bash
Step 1: "Configure cluster"
Name: "jo-udy-fsnd-EKS_Cluster"
Kubernetes version: "1.28" # Leave as default but note it down somewhere
Cluster Service Role: "jo-udy-fsnd-eks-clusterRole-001" # Automatically selects the cluster role created above
[NEXT] -> 

Step 2: "Specify networking"
VPC: vpc-**** # Automatically selects default VPC and subnets. I had to create a new vpc for "us-east-2"
Subets:            # Automatically associated from VPC
Security groups:   # Manually Select from default VPC
# Remaining items are default
[NEXT] -> 

Step 3: "Configure logging"
# Items are default
[NEXT] -> 

Step 4: "Select add-ons"
# Items are default
[NEXT] -> 

Step 5: "Configure selected add-ons settings"
# Items are default
[NEXT] -> 

Step 6: "Review and create"
[Create]
```

### 3. Creating an EKS NodeGroup
Wait till the Cluster that was created is active. <br>
Navigate to the cluster, then click on `Compute -> Add Node Group`
```bash
Step 1: "Configure Node Group"
Name: "jo-udy-fsnd-EKS_NodeGroup"
Node IAM role: "jo-udy-fsnd-eks-workerNodeRole-001" # Role that was created in prerequisites
# Remaining items are default
[NEXT] -> 

Step 2: "Set compute and scaling configuration"
Compute Configuration -
    AMI type: "Amazon Linux 2 (AL2_x86_64)"
    Capacity type: "On-Demand"
    Instance types: "t3.micro"
    Disk size: "20 GiB"
Scaling configuration - 
    Min size: "2" # Min number of nodes for scaling in.
    Max size: "2" # Max number of nodes for scaling out.
    Desired size: "2" # Initial count
# Remaining items are default
[NEXT] -> 

Step 3: "Specify networking"
Subnets: Automatically selected from default VPC
Configure remote access to nodes: Check
    EC2 Key Pair: Select the key pair from prerequisites
    Allow remote access from: All

Step 4: "Review and create"
[Create]
```

### 4. Post Creation
The Node Group created above spins up 2 EC2 instances. You can view them under the **EC2** services tab. You can also go to the **Amazon Elastic Kubernetes Service** tab and check the newly created cluster. <br>
To avoid AWS bills from the active instances:
1. **`DELETE`** the **Node Group** underneath the cluster before you can remove the cluster.
2. **`DELETE`** the **Cluster** .
3. **`DELETE`** the custom **IAM roles** you have created in this exercise.
Note: You have to execute the delete steps in the specified order.
