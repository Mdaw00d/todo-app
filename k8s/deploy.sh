#!/bin/bash

# Apply the namespace first
kubectl apply -f namespace.yaml

# Wait for the namespace to be ready
sleep 5

# Apply config and secrets
kubectl apply -f config.yaml

# Wait for config and secrets to be ready
sleep 5

# Apply backend deployment and service
kubectl apply -f backend.yaml

# Wait for backend to be ready
sleep 10

# Apply frontend deployment and service
kubectl apply -f frontend.yaml

# Wait for frontend to be ready
sleep 10

# Apply ingress
kubectl apply -f ingress.yaml

echo "All resources deployed successfully!"
echo "Access the application at http://localhost:3000 (if using minikube tunnel)"