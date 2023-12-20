## Kubernetes
Types of scaling
1. **Vertical scaling** Increasing the host machine's hardware resources on which the container is running is called vertical scaling. Earlier, we learned that a container has no resource constraints and can use as much of a given resource as the host's kernel scheduler allows. This approach's downside is that
    - It is challenging to scale up-or-down as the demand changes automatically.
    - Larger host machines can be more expensive than smaller machines, so it is a loss if the machine is underutilized. Also, running an application in a single container alone doesn’t leverage the full power of containerization.
2. **Horizontal scaling** Running multiple instances of the same application across multiple machines is called horizontal scaling. It is effortless to run multiple containers based on the same image.


### Why is Kubernetes required?
In the last lesson, you learned to containerize your application. The containers that you created were running locally on your machine. There are limitations to containerizing applications locally, such as:
1. **Scaling** - You cannot automatically scale up-or-down the resources (number of containers) or application usage requirements based on the incoming traffic.
2. **Updates** - Assume you have manually scaled up your containers horizontally on multiple hosts. Now, develop a patch/update in your application. It will be difficult for you to update the patch in each container manually.
3. **Elasticity** - Your local computer/on-premise servers may not suffice the hardware requirements for running too many containers parallelly.<br>

The solution to auto-scaling problems #1 and #2 above is to use the Kubernetes. The solution to problem #3 above is to use elastic (unlimited) resources on the cloud.


### What is Kubernetes?
Kubernetes is one of the most popular orchestration system for containers developed by Google and open sourced in 2014. It can automate many of the manual operations of deployment and scaling of a containerized application. A few of the benefits of using Kubernetes (k8s) are:
- The ease of scaling the container instances up or down to meet varying demands (horizontal scaling).
- It can balance loads, and perform health checks.
- It helps in setting-up inter-container communication (networking). <br>

Kubernetes was born out of the lessons learned in the [Scaling containerized apps at Google](https://queue.acm.org/detail.cfm?id=2898444).

### Benefits of using Kubernetes
A few more benefits of using Kubernetes are:
- High availability architecture
- Auto-scaling
- Rich Ecosystem
- Service discovery
- Container health management
- Secrets and configuration management. <br>

The downside of these features is the high complexity and learning curve of Kubernetes.

### Key Terms
- *Cluster*: A group of machines running Kubernetes
- *Master*: The system which controls a Kubernetes cluster. You will typically interact with the master when you communicate with a cluster. The master includes an api, scheduler, and management daemon.
- *Nodes*: The machines in a cluster. These can be virtual, physical, or a combination of both.
- *[Pods](https://kubernetes.io/docs/concepts/workloads/pods/)*: It is considered as the smallest unit in a cluster. It is a logical group of containers on a node that runs a particular module/application. A pod consists of one or more containers, shared storage resources, and a unique IP address. Note that all the containers within a Pod share the namespaces and filesystem volumes. Because pod memory is temporary, they can be connected to a *volume* for long term storage. Pods are not persistent, and may be brought up and down by the master during scaling. 

## Kubernetes Cluster Architecture
The core of Kubernetes is the cluster. A cluster comprises several node machines for running containerized applications and a master for managing the nodes. Each node is capable of running multiple pods (a group of containers). Therefore, each node has a container runtime, such as Docker, installed on it. <br>
The diagram below shows a simplistic view of a Kubernetes cluster.

<p align="center">
  <img src='Kubernetes clusters consist of a master system, nodes, pods, and services.png'><br>
  <span>Kubernetes clusters consist of a master system, nodes, pods, and services.</span>
</p>
<br>

Note the following points about the Kubernetes architecture:
1. Nodes are managed by the Master system. **Each node in the cluster must have a container runtime, such as Docker**.
2. A given node can host multiple PODs.
3. The PODs (a logical group of containers) are running independent modules of an application. In the last lesson, it was a single container running a module.
4. The PODs are replicated across multiple nodes. <br>

You can view a detailed version of the cluster architecture [here](https://kubernetes.io/docs/concepts/overview/components/).

### Reliability
In the cluster diagram shown above, each POD runs a specific module (App A, App B, App C...) of an application. Moreover, the PODs are not attached to a specific node (host). Instead, multiple nodes are hosting similar PODs. This architecture mitigates the chances of a single point of failure, and thus provides high availability. The master system brings a layer of abstraction for the external client/application.

### Service and Volumes
All pods that are running the same application module share storage resources. Further, all the containers within a pod share the namespaces and filesystem volumes. Hence, in order to have a persistent way to store data, volumes can be attached to pods.<br>
Whereas, in order to have a persistent way to communicate with ephemeral pods, a higher-level service abstraction is provided, called *Kubernetes Service*.<br>
*Service*: An abstraction of a set of pods and interface for how to interact with the pods

<p align="center">
  <img src='Kubernetes pods with a connected service and attached volume.png'><br>
  <span>Kubernetes pods with a connected service and attached volume.</span>
</p>


### How does it work? (High-level)
The following diagram shows the core operations involved in Kubernetes
1. Creating a Kubernetes Cluster
2. Deploying an application into the cluster
3. Exposing application ports
4. Scaling an application
5. Updating an application

<p align="center">
  <img src='5-steps of Kubernetes basics workflow.png'><br>
  <span>5-steps of Kubernetes basics workflow</span>
</p>
<br>

### How do you set up a Kubernetes cluster?
There are two main methods:
1. Set up a local cluster (preferably with Docker Desktop) - If you are using Docker and have enabled Kubernetes then you already have a standalone Kubernetes server running. Creating local clusters is beyond the scope of this course. However, we have dropped the link to a great tutorial at the bottom of this page.
2. Provision a cloud cluster. Most cloud service providers offer a managed Kubernetes service:
- Amazon through Amazon EKS
- Google through Google Kubernetes Engine GKE
- Microsoft through Azure Kubernetes Service (AKS). **In this course, you will learn to use Amazon EKS**.

### External Resourcces
1. Must Read Moving forward, we will be using Amazon EKS to create and manage a cluster for us. Before that, we encourage you to get an insight about the Kubernetes, its components, and Kubernetes API from the official documentation. This will help you gain a good understanding of cluster architecture and its working.
2. [Optional] Want to learn how to create a cluster locally? 
<br>

Read through a [quick primer](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/) beforehand, and follow this [amazing demo](https://github.com/katacoda-scenarios/kubernetes-bootcamp-scenarios) yourself