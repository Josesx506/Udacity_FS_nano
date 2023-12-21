### Deploy a simple flask app on Elastic Kubernetes Service
1. Create and EKS cluster using `eksctl create cluster --name eksctl-demo --nodes=2 --version=1.28 --instance-types=t2.me
dium --region=us-east-2`
2. Create a repo called **"simple-flask"** in your docker-hub account and make it accessible by the public.
3. Build the docker image `docker build -t <dockerhubUserName>/simple-flask`. My username is josesomojola.
4. Verify the image was built correctly using the `docker image ls` command. This should return a table of existing docker images where one of them has the specified tag name *simple-flask*, and a default tag of *latest*
    ```bash
    REPOSITORY                   TAG               IMAGE ID       CREATED              SIZE
    josesomojola/simple-flask    latest            6d147f45d4be   About a minute ago   165MB
    ```
5. Login to docker hub from terminal so you can push the local image to remote `docker login -u <dockerhubUserName>`
6. Push the image to docker-hub `docker push <dockerhubUserName>/simple-flask:latest`
    - If the online repo has a different name from the local image, the tag name of the local image can be modified with `docker tag <local-image-name>:<tag-name> <Repo-name>:<tag-name>`
7. The `EKS cluster` should be ready by now or whenver it's ready, check the health of the nodes with `kubectl get nodes`.
8. Open the configuration file `deployment.yml` and change line **25** to `image: <dockerhubUserName>/simple-flask`
9. Apply the configuration file to the cluster with `kubectl apply -f deployment.yml`
10. View the services, pods and nodes from the cluster with `kubectl get svc,pods,nodes`. This should return 
    ```bash
    NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
    service/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   17m

    NAME                                           READY   STATUS    RESTARTS   AGE
    pod/simple-flask-deployment-84fc89798d-2782n   1/1     Running   0          62s
    pod/simple-flask-deployment-84fc89798d-sxr57   1/1     Running   0          62s
    pod/simple-flask-deployment-84fc89798d-wm58l   1/1     Running   0          62s

    NAME                                                STATUS   ROLES    AGE   VERSION
    node/ip-192-168-20-235.us-east-2.compute.internal   Ready    <none>   10m   v1.28.3-eks-e71965b
    node/ip-192-168-85-179.us-east-2.compute.internal   Ready    <none>   10m   v1.28.3-eks-e71965b
    ```
    Note how the **`EXTERNAL-IP=<none>`** for the default kubernetes service, which is not the service for the application running. Without an external IP, we cannot access the app, and we need to expose an IP for the service of interest
11. To expose an IP `kubectl expose deployment simple-flask-deployment --type=LoadBalancer --name=my-service`. This will create a new `LoadBalancer` service called `my-service` within the deployment named `simple-flask-deployment` and expose a public IP.
12. View the new service with  `kubectl get svc`. This returns 
    ```bash
    NAME         TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)          AGE
    kubernetes   ClusterIP      10.100.0.1      <none>                                                                    443/TCP          23m
    my-service   LoadBalancer   10.100.179.30   a2bf34d8c10bc4ec1a186a78e5deff83-1115164121.us-east-2.elb.amazonaws.com   8080:31741/TCP   3s
    ```
13. Copy the `EXTERNAL-IP` for the new service into the browser. Check the deployment file for the `containerPort` which is **8080** and paste the link into the browser to access the app. `a2bf34d8c10bc4ec1a186a78e5deff83-1115164121.us-east-2.elb.amazonaws.com:8080`
14. The simple app only shows `Hello, World from Flask!`
15. Other useful **kubectl** commands include
    ```bash
    # Verify the deployment
    kubectl get deployments
    # Check the rollout status
    kubectl rollout status deployment/simple-flask-deployment
    # IMPORTANT: Show the service, nodes, and pods in the cluster
    # You will notice that the service does not have an external IP
    kubectl get svc,nodes,pods
    # Show the services in the cluster
    kubectl describe services
    # Display information about the cluster
    kubectl cluster-info
    ```
    Troubleshooting commands for if your pods do not show up as "Ready" while running the `kubectl get nodes` command
    ```bash
    # List all namespaces, all pods
    kubectl get all -A
    # Show all events
    kubectl get events -w
    # Show component status
    kubectl get componentstatuses
    ```

### Clean up
If you do not wish to continue to the next page right away, delete the deployment as well the Kubernetes cluster:
```bash
# Delete your deployment
kubectl delete deployments/simple-flask-deployment
# Tear down your cluster
eksctl delete cluster eksctl-demo --region=us-east-2
```

### Additional Reading
The following are some additional information on interacting with Kubernetes
- [Kubernetes Cheatsheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [`kubectl` Overview](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/)
- [`kubectl` Documentation](https://kubectl.docs.kubernetes.io/)