#!/bin/bash

# Set Docker environment to point to Minikube's Docker daemon
eval $(minikube docker-env)

# Build the frontend image in Minikube's Docker environment
docker build -f ../frontend/Dockerfile.minimal -t todo-frontend:latest ../frontend

# Build the backend image in Minikube's Docker environment
docker build -f ../backend/Dockerfile -t todo-backend:latest ../backend

echo "Images built successfully in Minikube's Docker environment!"