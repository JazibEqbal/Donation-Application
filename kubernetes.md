# Kubernetes (K8s) Architecture

Kubernetes architecture is easy to understand if you think of it as **a manager running a fleet of servers**.

- **Control Plane** → The Brain (makes decisions)
- **Worker Nodes** → The Workers (run applications)

---

# High-Level Architecture

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

# Control Plane

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

# 1. API Server

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

# 2. etcd

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

# 3. Scheduler

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

# 4. Controller Manager

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

# Worker Node

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

# 1. kubelet

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

# 2. Container Runtime

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

# 3. kube-proxy

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

# 4. Pods

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

# End-to-End Flow

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

# Self-Healing Example

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

# Complete Architecture Flow

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

| Command                              | Purpose                                    |
| ------------------------------------ |--------------------------------------------|
| `kubectl apply -f k8s/resource.yaml` | Create or update a resource                |
| `kubectl get <resource>`             | List resources of a specific type          |
| `kubectl get <resource> <name>`      | Get a specific resource by name            |
| `kubectl describe <resource> <name>` | Show detailed information about a resource |
| `kubectl logs <pod-name>`            | View logs for a pod's container            |
| `kubectl delete <resource> <name>`   | Delete a resource                          |
| `minikube image load <image-name>`   | Load a local image into Minikube           |
| `kubectl get pods -n <namespace>`    | Get pods in a specific namespace           |
| `kubectl get pods -w`                | Watch pods continuously                    |
| `kubectl get pods -A`                | Get pods from all namespaces               |

Deployment is needed because it manage Pods by handling restarts, scaling, and updates automatically.

Difference between a Pod and a Deployment?
- Pod: Runs one or more containers but doesn't automatically recover if deleted or crashed.
- Deployment: Manages Pods, keeps the desired number running, supports scaling, rolling updates, and self-healing.