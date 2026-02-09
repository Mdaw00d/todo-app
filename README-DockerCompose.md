# Todo App - Docker Compose Deployment

This directory contains a Docker Compose configuration to deploy the Todo application locally.

## Prerequisites

- Docker installed
- Docker Compose installed
- Docker images built (todo-frontend:latest and todo-backend:latest)

## Setup Instructions

1. Make sure you have built the Docker images as described in previous steps.

2. Start the services:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## Managing the Services

Start services in detached mode:
```bash
docker-compose -f docker-compose.yml up -d
```

Stop services:
```bash
docker-compose -f docker-compose.yml down
```

View logs:
```bash
docker-compose -f docker-compose.yml logs
```

View logs for a specific service:
```bash
docker-compose -f docker-compose.yml logs backend
docker-compose -f docker-compose.yml logs frontend
```

Restart services:
```bash
docker-compose -f docker-compose.yml restart
```

## Service Configuration

- **Backend**:
  - Port: 8000
  - Environment variables: DATABASE_URL, BETTER_AUTH_SECRET
  - Volume: Persistent storage for database

- **Frontend**:
  - Port: 3000
  - Environment variable: NEXT_PUBLIC_API_URL
  - Depends on: backend service

## Troubleshooting

Check if containers are running:
```bash
docker ps
```

Check container logs for errors:
```bash
docker logs todo-backend-container
docker logs todo-frontend-container
```

If you encounter issues with the authentication, make sure the environment variables are properly set in the docker-compose.yml file.