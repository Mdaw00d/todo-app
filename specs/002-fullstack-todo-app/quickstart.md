# Quickstart Guide: Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-app
**Date**: 2026-01-21
**Status**: Complete

## Overview

This guide provides step-by-step instructions to set up and run the Full-Stack Todo Web Application locally. The application consists of a Next.js frontend and a FastAPI backend with PostgreSQL database.

## Prerequisites

- Node.js 18+ with npm/yarn
- Python 3.11+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd to-do-app
```

### 2. Backend Setup (FastAPI)

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory with the following content:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp

# If using Neon, use the connection string from your Neon dashboard:
# DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# JWT Configuration
BETTER_AUTH_SECRET=your-super-secret-better-auth-key-change-in-production
BETTER_AUTH_URL=http://localhost:3000

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

Run database migrations (if using alembic):

```bash
alembic upgrade head
```

Start the backend server:

```bash
uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

### 3. Frontend Setup (Next.js)

In a new terminal, navigate to the frontend directory:

```bash
cd frontend  # From repository root
npm install
```

Create a `.env.local` file in the frontend directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Development Commands

### Backend Commands

```bash
# Start development server
uvicorn src.main:app --reload --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Format code
black src tests
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run linter
npm run lint

# Run type checking
npm run type-check
```

## Environment Configuration

### Required Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/todoapp

# Better Auth
BETTER_AUTH_SECRET=supersecretkey-minimum-32-chars
BETTER_AUTH_URL=http://localhost:3000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### Frontend (.env.local)
```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Auth
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## API Endpoints

Once both servers are running:

- **Backend API**: `http://localhost:8000`
- **Frontend App**: `http://localhost:3000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **API Redoc**: `http://localhost:8000/redoc`

## Testing the Application

1. Visit `http://localhost:3000` in your browser
2. Register a new account using the registration form
3. Log in with your credentials
4. Create and manage tasks using the dashboard

## Database Setup

### Using Neon (Recommended)

1. Create a Neon account at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string from the project dashboard
4. Update your `DATABASE_URL` in the backend `.env` file

### Using Local PostgreSQL

1. Install PostgreSQL locally
2. Create a database: `CREATE DATABASE todoapp;`
3. Create a user and grant privileges
4. Update your `DATABASE_URL` in the backend `.env` file

## Troubleshooting

### Common Issues

**Issue**: `psycopg2` installation fails on Windows
**Solution**: Install PostgreSQL binaries or use pre-compiled wheels:
```bash
pip install psycopg2-binary
```

**Issue**: Frontend can't connect to backend
**Solution**: Ensure both servers are running and CORS is configured correctly

**Issue**: Database connection fails
**Solution**: Verify your connection string and ensure PostgreSQL is running

### Resetting Development Data

To reset your development environment:

1. Drop and recreate the database
2. Run migrations again
3. Restart both servers

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/  # Run all tests
pytest tests/unit/  # Run unit tests only
pytest tests/integration/  # Run integration tests only
```

### Frontend Tests
```bash
cd frontend
npm run test  # Run Jest tests
npx playwright test  # Run E2E tests
```

## Production Deployment

For production deployment, ensure you:

1. Use strong, unique values for all secret keys
2. Configure SSL certificates
3. Set up proper logging and monitoring
4. Use environment-appropriate database connections
5. Implement proper backup strategies

## Next Steps

- Explore the API documentation at `/docs`
- Review the data models in the backend
- Customize the UI components in the frontend
- Add new features following the established patterns