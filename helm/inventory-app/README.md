# Inventory Management - Helm Chart

This Helm chart deploys the Inventory Management application on Kubernetes.
It matches the configuration in the `k8s/` folder.

## What We've Done

We created a complete Helm chart that:

1. **Converted k8s/ manifests to Helm templates** - All your existing Kubernetes YAML files are now templated
2. **Created reusable values files** - Separate configurations for dev, staging, and production
3. **Added template helpers** - Reusable functions in `_helpers.tpl` for consistent naming
4. **Implemented conditional logic** - Templates adapt based on values (e.g., NodePort only when specified)

### Current Deployment

**We are currently running `values.yaml` (default)** - NOT `values-dev.yaml`.

When you run:
```bash
helm install inventory ./helm/inventory-app --namespace default
```
Helm uses `values.yaml` by default. To use environment-specific values, you must specify the `-f` flag.

## Chart Structure

```
helm/inventory-app/
├── Chart.yaml                    # Chart metadata and versioning
├── values.yaml                   # DEFAULT configuration (currently running)
├── values-dev.yaml               # Development environment overrides
├── values-stage.yaml             # Staging environment overrides
├── values-prod.yaml              # Production environment overrides
└── templates/
    ├── _helpers.tpl              # Template helper functions
    ├── deployment.yaml           # Application deployment (matches k8s/app-deployment.yaml)
    ├── service.yaml              # App service (matches k8s/app-service.yaml)
    ├── configmap.yaml            # ConfigMap (matches k8s/configmap.yaml)
    ├── secret.yaml               # Secrets (matches k8s/secret.yaml)
    ├── hpa.yaml                  # HPA (matches k8s/hpa.yaml)
    ├── postgres-statefulset.yaml # PostgreSQL (matches k8s/db_deployment.yaml)
    ├── postgres-service.yaml     # DB service (matches k8s/db_service.yaml)
    ├── serviceaccount.yaml       # Service account
    └── ingress.yaml              # Ingress configuration
```

## Environment Differences

| Setting | values.yaml (Default) | values-dev.yaml | values-prod.yaml |
|---------|----------------------|-----------------|------------------|
| Replicas | 1 | 1 | 3 |
| Image Pull Policy | Never (local) | Never (local) | IfNotPresent |
| Service Type | NodePort | NodePort | ClusterIP |
| NodePort | 30007 | auto-assign | N/A |
| Autoscaling | Enabled (1-10) | Disabled | Enabled (3-15) |
| PostgreSQL | Enabled | Enabled | Disabled (external DB) |
| Ingress | Disabled | Disabled | Enabled with TLS |
| Resources | 100m-500m CPU | 100m-500m CPU | 500m-1000m CPU |

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- kubectl configured to access your cluster
- Minikube (for local development)

## Installation

### Install Helm (if not already installed)

```bash
# Linux/macOS
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version
```

## Deployment Commands

### Current Setup (Default values.yaml)

This is what we're currently running:
```bash
# Install with default values.yaml
helm install inventory ./helm/inventory-app --namespace default

# Access the app
minikube service inventory-service --url
# Or: http://<minikube-ip>:30007
```

### How to Switch to Development Environment

```bash
# Uninstall current release
helm uninstall inventory -n default

# Install with dev values
helm install inventory-dev ./helm/inventory-app \
  -f ./helm/inventory-app/values-dev.yaml \
  --namespace dev \
  --create-namespace
```

### How to Switch to Staging Environment

```bash
helm install inventory-stage ./helm/inventory-app \
  -f ./helm/inventory-app/values-stage.yaml \
  --namespace staging \
  --create-namespace
```

### How to Switch to Production Environment

```bash
# Production requires external secrets (never commit real passwords!)
export DB_PASSWORD="your-secure-db-password"
export ADMIN_PASSWORD="your-secure-admin-password"

helm install inventory-prod ./helm/inventory-app \
  -f ./helm/inventory-app/values-prod.yaml \
  --namespace production \
  --create-namespace \
  --set secrets.postgresPassword=$DB_PASSWORD \
  --set secrets.adminPassword=$ADMIN_PASSWORD
```

### Running Multiple Environments Simultaneously

You can run all environments at the same time in different namespaces:
```bash
# Default namespace (current)
helm install inventory ./helm/inventory-app -n default

# Dev namespace
helm install inventory-dev ./helm/inventory-app -f ./helm/inventory-app/values-dev.yaml -n dev --create-namespace

# Staging namespace  
helm install inventory-stage ./helm/inventory-app -f ./helm/inventory-app/values-stage.yaml -n staging --create-namespace

# Production namespace
helm install inventory-prod ./helm/inventory-app -f ./helm/inventory-app/values-prod.yaml -n production --create-namespace
```

## Configuration

### Key Parameters (Default values.yaml)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `app.name` | Application name | `inventory-app` |
| `app.replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `inventory_project_api` |
| `image.tag` | Image tag | `multistage` |
| `image.pullPolicy` | Image pull policy | `Never` (local) |
| `service.type` | Service type | `NodePort` |
| `service.port` | Service port | `8000` |
| `service.nodePort` | NodePort | `30007` |
| `autoscaling.enabled` | Enable HPA | `true` |
| `autoscaling.minReplicas` | Min replicas | `1` |
| `autoscaling.maxReplicas` | Max replicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | CPU target | `50` |
| `postgresql.enabled` | Deploy PostgreSQL | `true` |

### Override Values

```bash
helm install my-release ./helm/inventory-app \
  --set app.replicaCount=3 \
  --set image.tag="v2.0.0"
```

## Useful Commands

### Access the Application (Minikube)

```bash
minikube service inventory-service --url
# Or directly: http://<minikube-ip>:30007
```

### View Release Status

```bash
helm status inventory
```

### View Generated Manifests (Dry Run)

```bash
helm template inventory ./helm/inventory-app
```

### Uninstall Release

```bash
helm uninstall inventory
```

### Rollback to Previous Version

```bash
helm rollback inventory 1
```

## Comparison with k8s/ folder

| k8s File | Helm Template |
|----------|---------------|
| `app-deployment.yaml` | `templates/deployment.yaml` |
| `app-service.yaml` | `templates/service.yaml` |
| `configmap.yaml` | `templates/configmap.yaml` |
| `secret.yaml` | `templates/secret.yaml` |
| `hpa.yaml` | `templates/hpa.yaml` |
| `db_deployment.yaml` | `templates/postgres-statefulset.yaml` |
| `db_service.yaml` | `templates/postgres-service.yaml` |
