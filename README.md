# Donation Platform Application

A learning-focused backend project built to practice **Python, FastAPI, Pytest, Docker, GitHub Actions, Kubernetes, and Azure DevOps**.

The application provides APIs for managing donations, donors, NGOs, and related operations.

---

### Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pytest
- Docker
- Docker Compose
- GitHub Actions
- Kubernetes
- Minikube
- Azure DevOps

---

### Project Flow

```text
Development
    ↓
FastAPI
    ↓
Database
    ↓
Pytest
    ↓
Docker
    ↓
GitHub Push
    ↓
GitHub Actions
    ├── Test
    ├── Build Docker Image
    └── Push Image → GHCR
                         ↓
                    Kubernetes
                         ↓
                    Deployment
                         ↓
                      Pods
                         ↓
                     Service
                         ↓
                    Application
```
---

### CI/CD Flow

```text
Git Push
   ↓
GitHub
   ↓
GitHub Actions
   ├── Install dependencies
   ├── Run Pytest
   ├── Build Docker Image
   └── Push Image to GHCR
   ↓
Kubernetes / Minikube
   ├── Deployment
   ├── Service
   ├── ConfigMap
   ├── Secret
   ├── Health Probes
   └── Rolling Updates
```
---

### Additionaly

```text
GitHub
   ↓
Azure Pipeline
   ├── Test
   ├── Build
   ├── Test Results
   ├── Artifacts
   └── Stages / Environments
```
