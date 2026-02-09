@echo off
echo Setting up Minikube...

REM Add minikube to PATH for this session
set PATH=%PATH%;%USERPROFILE%\minikube

REM Start Minikube with Docker driver
echo Starting Minikube with Docker driver...
"%USERPROFILE%\minikube\minikube.exe" start --driver=docker --force

if %errorlevel% neq 0 (
    echo Failed to start Minikube
    exit /b %errorlevel%
)

echo Minikube started successfully!

REM Set Docker environment to point to Minikube's Docker daemon
echo Setting Docker environment to Minikube...
FOR /f "tokens=*" %%i IN ('minikube docker-env') DO %%i

REM Build the frontend image in Minikube's Docker environment
echo Building frontend image in Minikube...
docker build -f ../frontend/Dockerfile.minimal -t todo-frontend:latest ../frontend

REM Build the backend image in Minikube's Docker environment
echo Building backend image in Minikube...
docker build -f ../backend/Dockerfile -t todo-backend:latest ../backend

echo Images built successfully in Minikube!
echo You can now deploy the application using kubectl.