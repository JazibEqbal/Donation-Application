## Kubernetes (K8s) Architecture

Kubernetes architecture is easy to understand if you think of it as **a manager running a fleet of servers**.

- **Control Plane** → The Brain (makes decisions)
- **Worker Nodes** → The Workers (run applications)

---

## High-Level Architecture

```text
                    Kubernetes Cluster
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                  Control Plane (Brain)                     │
│                                                            │
│  API Server                                                │
│       │                                                    │
│       ▼                                                    │
│   Scheduler                                                │
│       │                                                    │
│       ▼                                                    │
│ Controller Manager                                         │
│       │                                                    │
│       ▼                                                    │
│      etcd (Database)                                       │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                    Worker Nodes                            │ 
│                                                            │
│  Node 1          Node 2          Node 3                    │
│ ┌─────────┐    ┌─────────┐    ┌─────────┐                  │
│ │ kubelet │    │ kubelet │    │ kubelet │                  │
│ │ kube-   │    │ kube-   │    │ kube-   │                  │
│ │ proxy   │    │ proxy   │    │ proxy   │                  │
│ │ Pods    │    │  Pods   │    │ Pods    │                  │
│ └─────────┘    └─────────┘    └─────────┘                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Control Plane

The **Control Plane** is the brain of Kubernetes.

Its job is to:

- Receive requests
- Decide where applications should run
- Monitor the cluster
- Recover from failures

The Control Plane consists of four major components:

- API Server
- etcd
- Scheduler
- Controller Manager

---

## 1. API Server

The **API Server** is the front door of Kubernetes.

Every request goes through the API Server.

Example:

```bash
kubectl apply -f nginx.yaml
```

Flow:

```text
kubectl
   │
   ▼
API Server
```

Responsibilities:

- Validates requests
- Authenticates users
- Stores cluster state in etcd
- Communicates with all other components

---

## 2. etcd

**etcd** is Kubernetes' database.

It stores everything about the cluster.

Examples:

- Pods
- Nodes
- Deployments
- Services
- ConfigMaps
- Secrets
- Cluster configuration

Example:

```text
Pod:
  nginx-pod

Status:
  Running

Node:
  worker-1
```

Everything is stored inside etcd.

Think of etcd as:

> **The Source of Truth** for the Kubernetes cluster.

---

## 3. Scheduler

The Scheduler decides:

> **Which Worker Node should run the Pod?**

Suppose you have:

```text
Worker 1
CPU: 80%

Worker 2
CPU: 20%

Worker 3
CPU: 50%
```

A new Pod needs to run.

Scheduler chooses:

```text
Worker 2
```

because it has enough available resources.

The Scheduler considers:

- CPU
- Memory
- Node labels
- Taints & tolerations
- Affinity rules
- Resource requests

---

## 4. Controller Manager

Controllers constantly compare:

**Desired State**

vs

**Actual State**

Example:

Desired:

```text
3 Pods
```

Actual:

```text
2 Pods
```

Controller notices:

```text
Need one more Pod
```

It immediately creates another Pod.

Controllers make Kubernetes **self-healing**.

Examples of controllers:

- Deployment Controller
- ReplicaSet Controller
- Node Controller
- Job Controller

---

## Worker Node

Worker Nodes run your applications.

Each Worker Node contains:

```text
Worker Node

kubelet
kube-proxy
Container Runtime
Pods
```

---

## 1. kubelet

kubelet is the agent running on every node.

Responsibilities:

- Receives instructions from API Server
- Starts Pods
- Monitors Pods
- Reports Pod status

Example:

API Server says:

```text
Run nginx Pod
```

kubelet starts it.

Later it reports:

```text
Status: Running
```

---

## 2. Container Runtime

The Container Runtime actually runs containers.

Examples:

- containerd
- CRI-O

Responsibilities:

- Pull images
- Create containers
- Start containers
- Stop containers
- Delete containers

Example:

```text
Pull image

nginx:latest

↓

Start container
```

---

## 3. kube-proxy

kube-proxy handles networking.

Suppose you have:

```text
Service
```

connected to

```text
3 Pods
```

Incoming traffic:

```text
Request 1 → Pod 1

Request 2 → Pod 2

Request 3 → Pod 3
```

kube-proxy routes traffic to the Pods.

---

## 4. Pods

Pods are the smallest deployable unit in Kubernetes.

A Pod usually contains one container.

Example:

```text
Pod

┌──────────────┐
│ nginx        │
└──────────────┘
```

Sometimes a Pod contains multiple containers.

Example:

```text
Pod

┌─────────────────────┐
│ Main Application    │
│ Logging Sidecar     │
└─────────────────────┘
```

Containers inside the same Pod share:

- Network
- Storage
- IP Address

---

## End-to-End Flow

Suppose you execute:

```bash
kubectl apply -f nginx.yaml
```

### Step 1

kubectl sends the request to the API Server.

```text
kubectl
    │
    ▼
API Server
```

---

### Step 2

API Server validates the request.

---

### Step 3

API Server stores the desired state inside etcd.

```text
Desired State

1 nginx Pod
```

---

### Step 4

Controller Manager checks:

```text
Desired:
1 Pod

Actual:
0 Pods
```

Difference detected.

Controller requests a new Pod.

---

### Step 5

Scheduler chooses the best Worker Node.

Example:

```text
Worker A

Worker B

Worker C
```

Scheduler selects:

```text
Worker B
```

---

### Step 6

kubelet on Worker B receives the instruction.

```text
Run nginx Pod
```

---

### Step 7

Container Runtime pulls the image.

```text
docker.io/nginx:latest
```

---

### Step 8

Container starts.

```text
Pod

↓

Running
```

---

### Step 9

kubelet reports status.

```text
Running
```

API Server updates etcd.

---

## Self-Healing Example

Suppose your Pod crashes.

Cluster state becomes:

```text
Desired:
1 Pod

Actual:
0 Pods
```

Controller detects the mismatch.

↓

Creates a replacement Pod.

↓

Scheduler selects a node.

↓

kubelet starts the Pod.

↓

Application becomes available again.

This feature is called **Self-Healing**.

---

## Complete Architecture Flow

```text
            kubectl
                │
                ▼
         +----------------+
         |   API Server   |
         +----------------+
                │
        Stores desired state
                ▼
             +------+
             | etcd |
             +------+
                ▲
                │
     Controller Manager
      (maintains desired state)
                │
                ▼
         +----------------+
         |   Scheduler    |
         +----------------+
                │
         Chooses a Worker Node
                ▼
     +-----------------------+
     |     Worker Node       |
     |                       |
     | kubelet               |
     | kube-proxy            |
     | Container Runtime     |
     |        │              |
     |      Pods             |
     +-----------------------+
```

### Commands

| Command                                           | Purpose                                    |
|---------------------------------------------------|--------------------------------------------|
| `kubectl apply -f k8s/resource.yaml`              | Create or update a resource                |
| `kubectl get <resource>`                          | List resources of a specific type          |
| `kubectl get <resource> <name>`                   | Get a specific resource by name            |
| `kubectl describe <resource> <name>`              | Show detailed information about a resource |
| `kubectl logs <pod-name>`                         | View logs for a pod's container            |
| `kubectl delete <resource> <name>`                | Delete a resource                          |
| `minikube image load <image-name>`                | Load a local image into Minikube           |
| `kubectl get pods -n <namespace>`                 | Get pods in a specific namespace           |
| `kubectl get pods -w`                             | Watch pods continuously                    |
| `kubectl get pods -A`                             | Get pods from all namespaces               |
| `kubectl rollout status dep.yml -n <namespace>`   | Watch a rollout                            |
| `kubectl rollout history dep.yml -n <namespace>`  | Check rollout history                      |
| `kubectl rollout undo dep.yml -n <namespace>`     | Rollback to previous version               |
| `minikube service <name> -n <namespace> --url`    | Get the service url                        |

Deployment is needed because it manage Pods by handling restarts, scaling, and updates automatically.

Difference between a Pod and a Deployment?
- Pod: Runs one or more containers but doesn't automatically recover if deleted or crashed.
- Deployment: Manages Pods, keeps the desired number running, supports scaling, rolling updates, and self-healing.

Service: A Service provides a stable network endpoint for a group of Pods. The Service uses labels to find the Pods.

ConfigMap: A ConfigMap stores non-sensitive configuration.<br>
Secrets: Secrets are intended for sensitive configuration.

## Probes
| Probe               | Purpose                                               | What happens if it fails?                                                                                                                                                                      |
| ------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Liveness Probe**  | Checks if the application is still running.           | Kubernetes restarts the container.                                                                                                                                                             |
| **Readiness Probe** | Checks if the application is ready to serve requests. | The pod is removed from the Service endpoints until it becomes ready again.                                                                                                                    |
| **Startup Probe**   | Checks whether the application has finished starting. | Kubernetes keeps checking; if it repeatedly fails beyond the configured threshold, the container is restarted. While the startup probe is running, liveness and readiness probes are disabled. |

## Resource Requests & Limits

Requests: Simply means "Kubernetes, please reserve at least this much for my container."
Kubernetes looks at their requests when deciding where Pods can run.<br>

Limits: "Don't allow this container to use more than this amount."
exceeding the limit can result in the container being terminated and restarted.
This prevents one application from consuming all available memory on the node.

## Deployment Strategies

### Rolling Update:
Default deployment strategy. When we want to deploy a new version say v2 of our application, but we can't stop all v1 pods as this will result in application downtime.
Instead, we can do this gradually and for this Kubernetes provides a rolling update strategy.

- maxSurge means number of pods we can have temporarily during update.

How Does Kubernetes Know the New Pod Is Healthy?<br>
This is where readiness probe becomes important, health checks and rolling updates work together.


### Recreate:
It is used when application needs complete restart. It stops all the pods, then creates the new pods. Hence, it has a downtime.
```yaml
strategy:
  type: Recreate
```

### Blue-Green Deployment:
Blue-Green is usually implemented using two separate application versions. When v2 is ready, change the Service selector.<br>
Advantage is very fast rollback, test of new version, old version remains available.<br>
Disadvantage is it requires roughly double the resources and db can be complicated.

### Canary Deployment:
Canary means releasing the new version to a small percentage of users first to a newer version and then if everything works fine then gradually shifting the users to the newer version.<br>
A common approach is to run two Deployments with the same service so it routes traffic to both the Deployments.


## PersistentVolumeClaim & Persistent Volume
To retain data even when a pod is deleted. Pods usually don't directly ask for a PV. Pods use a PVC.

PV = the actual storage i.e., "I have 10 GB of storage available."<br>
PVC = request for the actual storage i.e., "I need 5 GB of storage."

Create a PV:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: donation-application-pv
spec:
  capacity:
    storage: 10Gi

  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain # what happens to the PV's underlying storage when the PVC is deleted.

  hostPath:
    path: /mnt/donation-data
```

Create the PVC (will request PV for storage)
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: donation-application-pvc
  namespace: donation-platform
spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 5Gi
```

Pod references the PVC not the PV:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: donation-app
  namespace: donation-platform

spec:
  containers:
    - name: donation-app
      image: donation-app:latest

      volumeMounts:
        - name: donation-storage
          mountPath: /app/uploads

  volumes:
    - name: donation-storage
      persistentVolumeClaim:
        claimName: donation-application-pvc
```

Static provisioning: You manually create the PV, You manually define the storage.<br><br>
Dynamic provisioning: You only create PVC, and Kubernetes automatically creates/provisions the underlying PV using a StorageClass.<br>
You define a StorageClass, and Kubernetes provisions the storage automatically i.e., `Pod → PVC → StorageClass → dynamically created PV → Storage backend`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi
``` 

Storage Class:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard

provisioner: ebs.csi.aws.com

parameters:
  type: gp3
  fsType: ext4

reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

## StatefulSet

A StatefulSet is a Kubernetes workload controller designed for applications that need stable identity and persistent storage. StatefulSets normally work with a Headless Service i.e., `clusterIP: None` and hence the Pods can have stable DNS identities. Kubernetes uses the template to create a different PVC for each StatefulSet Pod.<br>
Unlike a deployment, StatefulSet gives each Pod a stable name and can give each Pod its own persistent volume.
Deployment is usually for stateless applications. StatefulSet is for stateful applications.

### Need of StatefulSet over Deployment:
Suppose you have a database with 2 Pods.
With a Deployment, the pod are created with random names like `pod-crr4654, pod-abc43`. If `pod-abc43` dies, kubernetes creates a new pod with name `pod-new34` which results in identity change. But with stateful application this is not ideal and that's where StatefulSet comes in and provides pods with stable identity i.e., if `pod-abc43 `dies, kubernetes recreates `pod-abc43`.<br><br>
Deployment is generally used for stateless applications where Pods are interchangeable. StatefulSet is used for stateful applications that require stable Pod identity, stable network identity, and persistent storage associated with each Pod.
Eg: A web application can usually use a Deployment, while a database cluster such as MySQL may use a StatefulSet.
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3

  selector:
    matchLabels:
      app: mysql

  template:
    metadata:
      labels:
        app: mysql

    spec:
      containers:
        - name: mysql
          image: mysql:8
          volumeMounts:
            - name: mysql-data
              mountPath: /var/lib/mysql

  volumeClaimTemplates:
    - metadata:
        name: mysql-data
      spec:
        storageClassName: standard # dynamic provisioning (storage class needs to be defined)
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
```
What gets created?

Pods:

        mysql-0
        mysql-1
        mysql-2

PVCs:

        mysql-data-mysql-0
        mysql-data-mysql-1
        mysql-data-mysql-2