# Kubernetes Deployment Kılavuzu

## Dosya Yapısı

### Temel Deployment (Development/Test)
- `deployment.yaml` - Temel deployment (2 replica)
- `service.yaml` - ClusterIP service
- `configmap.yaml` - Temel konfigürasyon

### Production Deployment
- `production/namespace.yaml` - Production namespace
- `production/deployment-prod.yaml` - Production deployment (3 replica, detaylı ayarlar)
- `production/service-prod.yaml` - Production service
- `production/configmap-prod.yaml` - Production configmap
- `production/hpa.yaml` - Horizontal Pod Autoscaler (3-10 replica arası)
- `production/pdb.yaml` - Pod Disruption Budget (min 2 pod)
- `production/ingress.yaml` - Ingress (opsiyonel)

## Deployment Adımları

### 1. Temel Deployment (Development)
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 2. Production Deployment
```bash
# Namespace oluştur
kubectl apply -f k8s/production/namespace.yaml

# ConfigMap
kubectl apply -f k8s/production/configmap-prod.yaml

# Deployment
kubectl apply -f k8s/production/deployment-prod.yaml

# Service
kubectl apply -f k8s/production/service-prod.yaml

# HPA (opsiyonel - metrics-server gerekli)
kubectl apply -f k8s/production/hpa.yaml

# PDB
kubectl apply -f k8s/production/pdb.yaml

# Ingress (opsiyonel)
kubectl apply -f k8s/production/ingress.yaml
```

## Production Özellikleri

### Deployment
- **Replicas**: 3 (başlangıç)
- **Rolling Update**: maxSurge=1, maxUnavailable=0
- **Resources**: 
  - Requests: 128Mi memory, 100m CPU
  - Limits: 256Mi memory, 200m CPU
- **Liveness Probe**: `/health/live` (15s initial delay)
- **Readiness Probe**: `/health/ready` (10s initial delay)
- **Security Context**: Non-root user, dropped capabilities

### HPA (Horizontal Pod Autoscaler)
- **Min Replicas**: 3
- **Max Replicas**: 10
- **CPU Threshold**: %70
- **Memory Threshold**: %80

### Pod Disruption Budget
- **Min Available**: 2 pod

## Endpoint'ler

- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness check
- `GET /live-down` - Live durumunu toggle et
- `POST /set-healthcheck` - Healthcheck JSON'unu ayarla

## Port Forward (Test için)
```bash
kubectl port-forward -n production svc/healthcheck-controller 8080:80
```

