# Todo App - Kubernetes Deployment

This directory contains Kubernetes manifests to deploy the Todo application using Minikube.

## Prerequisites

- Minikube installed
- kubectl installed
- Docker running

## Setup Instructions

1. Start Minikube:
   ```bash
   minikube start
   ```

2. Build the Docker images directly in Minikube's Docker environment:
   ```bash
   # On Linux/Mac:
   eval $(minikube docker-env)
   docker build -f ../frontend/Dockerfile.minimal -t todo-frontend:latest ../frontend
   docker build -f ../backend/Dockerfile -t todo-backend:latest ../backend
   
   # Or use the provided script (after making it executable):
   chmod +x build_images_minikube.sh
   ./build_images_minikube.sh
   ```

   On Windows PowerShell:
   ```powershell
   & minikube docker-env | Invoke-Expression
   docker build -f ../frontend/Dockerfile.minimal -t todo-frontend:latest ../frontend
   docker build -f ../backend/Dockerfile -t todo-backend:latest ../backend
   ```
   
   Or use the provided PowerShell script:
   ```powershell
   .\build_images_minikube.ps1
   ```

3. Navigate to the k8s directory:
   ```bash
   cd k8s
   ```

4. Deploy the application:
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f config.yaml
   kubectl apply -f backend.yaml
   kubectl apply -f frontend.yaml
   kubectl apply -f ingress.yaml
   ```

   Or run the deployment script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

5. Access the application:
   - Using port forwarding: `minikube service todo-frontend-service -n todo-app`
   - Using ingress: Enable ingress addon and access via Minikube IP
   - Using tunnel: Run `minikube tunnel` in a separate terminal and access via NodePort

## Enable Ingress (Optional)

If you want to use the ingress resource:
```bash
minikube addons enable ingress
```

## Alternative Access Methods

Using port forwarding:
```bash
minikube service todo-frontend-service -n todo-app --url
```

Using tunnel:
```bash
minikube tunnel
```
Then access the frontend at http://localhost:3000

## Troubleshooting

Check the status of pods:
```bash
kubectl get pods -n todo-app
```

View pod logs:
```bash
kubectl logs -n todo-app deployment/todo-frontend-deployment
kubectl logs -n todo-app deployment/todo-backend-deployment
```

Describe a pod for detailed information:
```bash
kubectl describe pod -n todo-app -l app=todo-frontend
```

Delete all resources:
```bash
kubectl delete namespace todo-app
```