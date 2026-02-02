# Inventory Management - Helm Chart

This Helm chart deploys the Inventory Management application on Kubernetes using a **split-release architecture** where the database and application are deployed as separate Helm releases.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      inventory-ns namespace                      │
├─────────────────────────────────┬───────────────────────────────┤
│         db-release              │        app-release            │
├─────────────────────────────────┼───────────────────────────────┤
│  • postgres-statefulset         │  • inventory-app deployment   │
│  • postgres-service (headless)  │  • inventory-service (NodePort)│
│  • inventory-app-db-config      │  • inventory-app-app-config   │
│  • inventory-app-db-secret      │  • inventory-app-app-secret   │
│                                 │  • inventory-sa (ServiceAccount)│
│                                 │  • inventory-app-hpa          │
└─────────────────────────────────┴───────────────────────────────┘
```

## Chart Structure

```
helm/inventory-app/
├── Chart.yaml              # Chart metadata (name, version, description)
├── values.yaml             # Default values (combined config)
├── values-app.yaml         # App-only release configuration
├── values-db.yaml          # Database-only release configuration
├── .helmignore             # Files to ignore when packaging
├── README.md               # This file
└── templates/
    ├── _helpers.tpl        # Template helper functions
    ├── deployment.yaml     # App Deployment (conditional: app.enabled)
    ├── service.yaml        # Services (iterates over myServices map)
    ├── configmap.yaml      # ConfigMaps (conditional: app/db)
    ├── secret.yaml         # Secrets (conditional: app/db)
    ├── hpa.yaml            # HorizontalPodAutoscaler
    ├── postgres-statefulset.yaml  # PostgreSQL StatefulSet
    ├── serviceaccount.yaml # ServiceAccount
    ├── ingress.yaml        # Ingress (optional)
    └── NOTES.txt           # Post-install instructions
```

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- kubectl configured to access your cluster
- Minikube (for local development)
- Docker image `inventory_project_api:multistage` built locally

## Quick Start

### 1. Build the Docker Image (Minikube)

```bash
# Point Docker to Minikube's daemon
eval $(minikube docker-env)

# Build the image
docker build -t inventory_project_api:multistage .
```

### 2. Create Namespace

```bash
kubectl create namespace inventory-ns
```

### 3. Deploy Database Release

```bash
helm install db-release ./helm/inventory-app \
  --namespace inventory-ns \
  -f ./helm/inventory-app/values-db.yaml
```

### 4. Deploy Application Release

```bash
helm install app-release ./helm/inventory-app \
  --namespace inventory-ns \
  -f ./helm/inventory-app/values-app.yaml
```

### 5. Access the Application

```bash
minikube service inventory-service -n inventory-ns --url
# Or directly: http://<minikube-ip>:30007
```

## Values Files Explained

### values-db.yaml
Deploys **only** the database components:
- PostgreSQL StatefulSet
- Headless Service (`postgres-service`)
- Database ConfigMap and Secret

Key settings:
```yaml
app:
  enabled: false           # Don't deploy app
postgresql:
  enabled: true            # Deploy database
common:
  enabled: true            # Create shared resources
myServices:
  backend:
    enabled: false         # Don't create app service
  postgres:
    enabled: true          # Create DB service
```

### values-app.yaml
Deploys **only** the application components:
- Application Deployment
- NodePort Service (`inventory-service`)
- App ConfigMap and Secret
- HPA and ServiceAccount

Key settings:
```yaml
app:
  enabled: true            # Deploy app
postgresql:
  enabled: false           # Don't deploy database
common:
  enabled: false           # DB release created these
myServices:
  backend:
    enabled: true          # Create app service
  postgres:
    enabled: false         # Don't create DB service
```

## Command Reference

### Installation

```bash
# Install DB release
helm install db-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-db.yaml

# Install App release
helm install app-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-app.yaml
```

### Upgrade (After Editing Values)

```bash
# Upgrade DB release
helm upgrade db-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-db.yaml

# Upgrade App release
helm upgrade app-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-app.yaml
```

### Install or Upgrade (Recommended)

```bash
# Creates if not exists, upgrades if exists
helm upgrade --install db-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-db.yaml

helm upgrade --install app-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-app.yaml
```

### Uninstall

```bash
# Uninstall both releases
helm uninstall app-release db-release -n inventory-ns

# Delete namespace (complete cleanup)
kubectl delete namespace inventory-ns
```

### Status & Debugging

```bash
# List releases
helm list -n inventory-ns

# Check release status
helm status app-release -n inventory-ns
helm status db-release -n inventory-ns

# View deployed manifests
helm get manifest app-release -n inventory-ns
helm get manifest db-release -n inventory-ns

# View used values
helm get values app-release -n inventory-ns
helm get values db-release -n inventory-ns

# Dry-run / Template preview
helm template app-release ./helm/inventory-app \
  -n inventory-ns \
  -f ./helm/inventory-app/values-app.yaml

# Lint chart
helm lint ./helm/inventory-app

# Check resources
kubectl get all -n inventory-ns

# View logs
kubectl logs -l app=inventory-app -n inventory-ns
kubectl logs -l app=postgres -n inventory-ns

# Describe pod issues
kubectl describe pod -l app=inventory-app -n inventory-ns
```

### Rollback

```bash
# View history
helm history app-release -n inventory-ns

# Rollback to previous
helm rollback app-release -n inventory-ns

# Rollback to specific revision
helm rollback app-release 1 -n inventory-ns
```

### Access Application

```bash
# Get URL via Minikube
minikube service inventory-service -n inventory-ns --url

# Or manually
export NODE_IP=$(minikube ip)
export NODE_PORT=$(kubectl get svc inventory-service -n inventory-ns -o jsonpath='{.spec.ports[0].nodePort}')
echo "http://$NODE_IP:$NODE_PORT"

# Port forward (alternative)
kubectl port-forward svc/inventory-service 8000:8000 -n inventory-ns
```

## Configuration Parameters

### Application Settings (values-app.yaml)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `app.enabled` | Deploy application | `true` |
| `app.replicaCount` | Number of replicas | `3` |
| `app.containerPort` | Container port | `8000` |
| `image.repository` | Image name | `inventory_project_api` |
| `image.tag` | Image tag | `multistage` |
| `image.pullPolicy` | Pull policy | `Never` |
| `autoscaling.enabled` | Enable HPA | `true` |
| `autoscaling.minReplicas` | Min replicas | `1` |
| `autoscaling.maxReplicas` | Max replicas | `10` |

### Database Settings (values-db.yaml)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Deploy PostgreSQL | `true` |
| `postgresql.image` | PostgreSQL image | `postgres:15` |
| `postgresql.replicas` | Number of replicas | `1` |
| `postgresql.storage.size` | PVC size | `1Gi` |

### Service Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `myServices.backend.type` | Service type | `NodePort` |
| `myServices.backend.nodePort` | NodePort | `30007` |
| `myServices.backend.port` | Service port | `8000` |
| `myServices.postgres.headless` | Headless service | `true` |

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod -l app=inventory-app -n inventory-ns
kubectl get events -n inventory-ns --sort-by='.lastTimestamp'
```

### Database connection issues
```bash
# Check if postgres is running
kubectl get pods -l app=postgres -n inventory-ns

# Check postgres logs
kubectl logs -l app=postgres -n inventory-ns

# Test connectivity
kubectl port-forward svc/postgres-service 5432:5432 -n inventory-ns
# Then connect with: psql -h localhost -U postgres -d inventory_db
```

### Service not accessible
```bash
# Check service exists
kubectl get svc -n inventory-ns

# Check endpoints
kubectl get endpoints -n inventory-ns

# Verify pod labels match service selector
kubectl get pods -n inventory-ns --show-labels
```

## Comparison: Helm vs Raw k8s/

| Feature | Raw k8s/ | Helm |
|---------|----------|------|
| Templating | No | Yes (Go templates) |
| Environment configs | Manual editing | values-*.yaml |
| Versioning | Git only | Helm revisions |
| Rollback | Manual | `helm rollback` |
| Dependencies | Manual order | Managed |
| Reusability | Copy/paste | Single chart |

## Related Documentation

- [Main README](../../README.md) - Project overview
- [k8s/README.md](../../k8s/README.md) - Raw Kubernetes manifests
- [crud_files/README.md](../../crud_files/README.md) - CRUD operations
