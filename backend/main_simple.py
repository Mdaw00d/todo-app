"""FastAPI application entry point - simplified version for testing."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import health, tasks
from src.api.auth import router as auth_router

# Create app without lifespan to test route registration
app = FastAPI(
    title="Todo Full-Stack Web Application API - Testing",
    description="Testing version without lifespan",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(auth_router)

@app.get("/")
def root():
    """Root endpoint for the API."""
    return {"status": "Test API is running", "version": "1.0.0"}