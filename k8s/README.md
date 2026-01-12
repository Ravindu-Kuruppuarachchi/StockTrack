# Kubernetes Manifests

This folder contains raw Kubernetes manifest files for deploying the Inventory Management application without Helm. These are static YAML files that can be applied directly using `kubectl`.

## Overview

The k8s/ folder provides a straightforward way to deploy the application to Kubernetes. While less flexible than Helm, it's simpler to understand and useful for learning Kubernetes concepts.

## Directory Structure

```
k8s/
├── app-deployment.yaml   # Application Deployment
├── app-service.yaml      # Application Service (NodePort)
├── db_deployment.yaml    # PostgreSQL StatefulSet
├── db_service.yaml       # PostgreSQL Service (Headless)
├── configmap.yaml        # Environment configuration
├── secret.yaml           # Sensitive data (passwords)
├── hpa.yaml              # Horizontal Pod Autoscaler
└── README.md             # This file
```

## File Descriptions

### app-deployment.yaml
Defines the application Deployment:
- **Image**: `inventory_project_api:multistage`
- **Replicas**: Managed by HPA
- **Port**: 8000
- **Health Checks**: Liveness and readiness probes on `/health`
- **Resources**: CPU and memory limits/requests
- **Environment**: Injected from ConfigMap and Secret

### app-service.yaml
Exposes the application:
- **Type**: NodePort
- **Port**: 8000
- **NodePort**: 30007
- **Selector**: Matches pods with `app: inventory-app`

### db_deployment.yaml
PostgreSQL database as a StatefulSet:
- **Image**: `postgres:15`
- **Storage**: 1Gi PersistentVolumeClaim
- **Port**: 5432
- **Credentials**: From ConfigMap and Secret

### db_service.yaml
Headless service for PostgreSQL:
- **Type**: ClusterIP (None - headless)
- **Port**: 5432
- **Purpose**: Allows pods to connect to `postgres-service:5432`

### configmap.yaml
Non-sensitive configuration:
- `POSTGRES_USER`: Database username
- `POSTGRES_DB`: Database name
- `ADMIN_EMAIL`: Admin email address
- `DATABASE_URL`: Connection string

### secret.yaml
Sensitive configuration (base64 encoded):
- `POSTGRES_PASSWORD`: Database password
- `ADMIN_PASSWORD`: Admin login password

### hpa.yaml
Horizontal Pod Autoscaler:
- **Min Replicas**: 1
- **Max Replicas**: 10
- **Target CPU**: 50%

## Prerequisites

- Kubernetes cluster (Minikube for local development)
- kubectl configured
- Docker image built locally (for Minikube)

## Deployment Steps

### 1. Start Minikube

```bash
minikube start
```

### 2. Build Docker Image

```bash
# Point Docker to Minikube's daemon
eval $(minikube docker-env)

# Build the image
docker build -t inventory_project_api:multistage .
```

### 3. Apply All Manifests

```bash
# Apply all files at once
kubectl apply -f k8s/

# Or apply in order (recommended for first deployment)
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/db_service.yaml
kubectl apply -f k8s/db_deployment.yaml
kubectl apply -f k8s/app-service.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/hpa.yaml
```

### 4. Verify Deployment

```bash
# Check all resources
kubectl get all

# Check pods are running
kubectl get pods

# Check services
kubectl get svc
```

### 5. Access the Application

```bash
# Get URL via Minikube
minikube service inventory-service --url

# Or access directly
echo "http://$(minikube ip):30007"
```

## Common Commands

### View Resources

```bash
# All resources
kubectl get all

# Pods with details
kubectl get pods -o wide

# Services
kubectl get svc

# ConfigMaps
kubectl get configmap

# Secrets
kubectl get secrets

# HPA status
kubectl get hpa
```

### Debugging

```bash
# View pod logs
kubectl logs -l app=inventory-app
kubectl logs -l app=postgres

# Describe pod (troubleshooting)
kubectl describe pod <pod-name>

# Get events
kubectl get events --sort-by='.lastTimestamp'

# Execute into pod
kubectl exec -it <pod-name> -- /bin/bash
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment inventory-app --replicas=3

# Check HPA status
kubectl get hpa inventory-app-hpa
```

### Updating

```bash
# After editing a manifest
kubectl apply -f k8s/<filename>.yaml

# Restart deployment (picks up ConfigMap/Secret changes)
kubectl rollout restart deployment inventory-app

# Check rollout status
kubectl rollout status deployment inventory-app
```

### Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Or delete specific resource
kubectl delete -f k8s/app-deployment.yaml
```

## Resource Specifications

### Application Deployment

| Setting | Value |
|---------|-------|
| Image | `inventory_project_api:multistage` |
| Pull Policy | `Never` (local image) |
| Container Port | 8000 |
| CPU Request | 100m |
| CPU Limit | 500m |
| Memory Request | 128Mi |
| Memory Limit | 256Mi |
| Liveness Probe | `/health` (delay: 15s) |
| Readiness Probe | `/health` (delay: 5s) |

### PostgreSQL StatefulSet

| Setting | Value |
|---------|-------|
| Image | `postgres:15` |
| Port | 5432 |
| Storage | 1Gi (ReadWriteOnce) |
| Service | Headless (ClusterIP: None) |

### HPA Configuration

| Setting | Value |
|---------|-------|
| Min Replicas | 1 |
| Max Replicas | 10 |
| Target CPU | 50% |

## Helm vs Raw Manifests

| Aspect | k8s/ (Raw) | Helm |
|--------|------------|------|
| **Pros** | Simple, no extra tools | Templating, versioning, rollback |
| **Cons** | Static, no templating | More complex setup |
| **Best For** | Learning, simple deployments | Production, multi-env |

For production deployments with multiple environments, consider using the [Helm chart](../helm/inventory-app/README.md).

## Troubleshooting

### Image Pull Error
```bash
# Ensure you're using Minikube's Docker
eval $(minikube docker-env)
docker images | grep inventory
```

### Pod CrashLoopBackOff
```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Database Connection Failed
```bash
# Check postgres is running
kubectl get pods -l app=postgres

# Check service DNS
kubectl run test --rm -it --image=busybox -- nslookup postgres-service
```

### Service Not Accessible
```bash
# Check endpoints
kubectl get endpoints inventory-service

# Verify NodePort
kubectl get svc inventory-service
```

## Related Documentation

- [Main README](../README.md) - Project overview
- [Helm Chart](../helm/inventory-app/README.md) - Helm-based deployment
- [CRUD Files](../crud_files/README.md) - Database operations
