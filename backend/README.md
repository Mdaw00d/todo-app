# Todo AI Chatbot

AI-powered conversational todo chatbot with MCP tools that allows users to manage tasks using natural language.

## Features

- Natural language task management (add, list, complete, update, delete tasks)
- Stateful conversations with context awareness
- User data isolation and security
- MCP (Model Context Protocol) tools for AI interaction
- Stateless server architecture with persistent storage
- JWT-based authentication

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (via SQLModel)
- **AI**: OpenAI Agents SDK
- **MCP Tools**: Custom MCP implementation
- **Authentication**: JWT with Better Auth
- **Deployment**: Docker-ready

## Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key
- JWT secret key

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-ai-chatbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install poetry
   poetry install
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

5. Set up the database:
   ```bash
   # Make sure your DATABASE_URL is set in .env
   python -c "from src.database.init import create_tables; import asyncio; asyncio.run(create_tables())"
   ```

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key for AI functionality
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS265)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `BETTER_AUTH_SECRET`: Better Auth secret key
- `NEON_PROJECT_ID`: Neon PostgreSQL project ID
- `ENVIRONMENT`: Environment (development/production)
- `DEBUG`: Debug mode (true/false)

## Running the Application

### Development

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Or using Docker:
```bash
docker build -t todo-ai-chatbot .
docker run -p 8000:8000 todo-ai-chatbot
```

## API Usage

### Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer {jwt_token}
```

### Chat Endpoint

Interact with the AI chatbot:

```
POST /api/{user_id}/chat
```

Example request:
```json
{
  "conversation_id": null,
  "message": "Add a task to buy groceries"
}
```

Example response:
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "buy groceries",
        "description": null
      }
    }
  ]
}
```

### Health Check

Check if the service is running:
```
GET /api/health
```

## Architecture

### Components

- `models/`: SQLModel database models (Task, Conversation, Message)
- `services/`: Business logic layers
- `mcp_tools/`: MCP tools for AI agent interaction
- `agents/`: AI agent implementation
- `api/`: FastAPI endpoints
- `auth/`: Authentication and authorization
- `database/`: Database initialization and session management
- `exceptions/`: Custom exception handlers
- `middleware/`: Request processing middleware
- `utils/`: Utility functions and helpers

### Data Flow

1. User sends natural language message to chat endpoint
2. Request is authenticated and validated
3. AI agent processes the message and determines intent
4. AI agent calls appropriate MCP tools based on intent
5. MCP tools execute operations through service layer
6. Services interact with database models
7. Results are returned to AI agent
8. AI agent generates natural language response
9. Response is returned to user

## Development

### Adding New MCP Tools

1. Create a new method in the appropriate MCP tools class (`task_mcp_tools.py` or `conversation_mcp_tools.py`)
2. Implement proper validation and error handling
3. Call the corresponding service method
4. Return consistent response format
5. Add unit tests

### Running Tests

```bash
cd backend
pytest tests/
```

### Code Formatting

```bash
# Format code with black
black .

# Lint code with flake8
flake8 .
```

## Deployment

### Docker

A Dockerfile is included for containerized deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

Make sure to set appropriate values for production:

- `ENVIRONMENT=production`
- `DEBUG=false`
- Proper database connection string
- Valid OpenAI API key
- Strong JWT secret key

## Security

- All API endpoints require authentication
- User data is isolated by user ID
- Input validation on all user-facing endpoints
- Rate limiting to prevent abuse
- JWT tokens with configurable expiration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

[License information would go here]