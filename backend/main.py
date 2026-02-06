"""
Main application factory for the Todo AI Chatbot.
Creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from src.database.init import create_tables
from src.exceptions.handlers import register_exception_handlers
from src.api.health import router as health_router
from src.api.chat_router import router as chat_router
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.utils.logging import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Runs startup and shutdown events.
    """
    # Startup
    app_logger.info("Starting Todo AI Chatbot application...")
    try:
        # Initialize database tables
        await create_tables()
        app_logger.info("Database tables created successfully")
    except Exception as e:
        app_logger.error(f"Failed to initialize database: {str(e)}")
        raise

    yield

    # Shutdown
    app_logger.info("Shutting down Todo AI Chatbot application...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    # Create FastAPI app with lifespan
    app = FastAPI(
        title="Todo AI Chatbot API",
        description="AI-powered conversational todo chatbot with MCP tools",
        version="1.0.0",
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
            "https://*.vercel.app",
            "https://todo-app-wj1h.onrender.com"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Include routers
    app.include_router(health_router, prefix="/api", tags=["health"])
    app.include_router(chat_router, prefix="/api", tags=["chat"])
    app.include_router(tasks_router, prefix="/api", tags=["tasks"])
    app.include_router(auth_router, prefix="/api", tags=["auth"])

    # Add root endpoint for Render health checks
    @app.get("/")
    def root_health_check():
        return {"status": "healthy", "service": "todo-backend"}

    @app.head("/")
    def root_head_check():
        return {"status": "healthy"}

    return app


# Create the main application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=bool(os.getenv("RELOAD", "False").lower() == "true")
    )