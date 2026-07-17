Problem: Different environments lead to different behavior.
Solution: This is where docker comes into the picture.
Docker packages everything the application needs into one unit. Therefore, anyone who runs that image gets the same environment.

## Container vs Virtual Machine:

### Virtual Machine: 
- Every VM contains a complete separate operating system.
- It offers a strong isolation however it also results in Slow startup, high memory usage, slower response.

### Docker Container:
- Containers share the host OS kernel, so they are much lighter.
- It also results in less memory usage, startup in seconds and easy to distribute.
- Containers are running instances.

### Docker Image
- An image is a blueprint which contains instructions to create a container.
- One image can create many containers.

### Docker Engine
- A docker engine is a software that builds images, starts containers, stops containers, manages networking and storage etc.

### What happens when we run a container?
    docker run hello-world
            │
            ▼
    Is image available locally?
            │
       Yes ─────────► Run container
            │
           No
            ▼
    Download image from Docker Hub
            │
            ▼
    Create container
            │
            ▼
    Execute application
            │
            ▼
    Exit

### Docker commands
    list downloaded images  ─────────► docker images

    list running containers  ─────────► docker ps
    
    list containers  ─────────► docker ps -a

    remove a container ─────────► docker rm <container_id>

    remove an image ─────────► docker rmi <image>