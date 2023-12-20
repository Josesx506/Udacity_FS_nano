## Server Deployment and Containerization

### Virtual Machines (VM) vs. Containers
This module explained the differences between both platforms. VMs use system resources and can operate multiple OS on the same machine. This makes them relatively slow and they're limited by the hardware resource specified when creating them e.g. allocated RAM. They can be managed with softwares like VMWare. An EC2 instance is another example of a VM<br>

Containers on the other hand are more lightweight. They share the same OS kernel and can start faster when launched. They are however limited to the OS type of the host system, but they are restricted to specified system resources like  VMs e.g. A container can use 60% RAM while a VM is locked to the allocated RAM when it was created like 20%. Containers are popularly developed by Docker and can be scaled across cloud platforms using Kubernetes.


### Containers
Creating Dockerfiles, building the files to docker images, and running the images as containers. The chapter showed how to build images from scratch and run them as containers.