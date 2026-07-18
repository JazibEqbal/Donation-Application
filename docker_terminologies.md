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

    docker build ─────────► docker build -t <image_name>:<image_version> .

    create ans run a container: docker run -p <host_port>:<container_port> <image_name>

    start/stop a container: docker start/stop <container_id>

    view logs of a container: docker logs <container_id>

    run a container in detached mode: docker run --p <host_port>:<container_port> --name my_app <image_name>
    
### Docker File
- A Dockerfile is simply a step-by-step instructions to build a Docker image.
- Without a Dockerfile, Docker doesn't know how to package your application.