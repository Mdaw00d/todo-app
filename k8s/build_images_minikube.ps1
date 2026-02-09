# Set Docker environment to point to Minikube's Docker daemon
& minikube docker-env | Invoke-Expression

# Build the frontend image in Minikube's Docker environment
docker build -f ../frontend/Dockerfile.minimal -t todo-frontend:latest ../frontend

# Build the backend image in Minikube's Docker environment
docker build -f ../backend/Dockerfile -t todo-backend:latest ../backend

Write-Host "Images built successfully in Minikube's Docker environment!"