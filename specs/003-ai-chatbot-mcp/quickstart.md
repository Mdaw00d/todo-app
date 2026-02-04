# Quickstart Guide: Todo AI Chatbot with MCP Tools

## Overview
This guide provides instructions for setting up and running the Todo AI Chatbot with MCP Tools locally for development and testing.

## Prerequisites
- Python 3.11 or higher
- Poetry (dependency manager) or pip
- Neon PostgreSQL account and database
- OpenAI API key
- Better Auth configuration

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies
Using Poetry:
```bash
poetry install
poetry shell
```

Using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@neon_host/db_name
NEON_PROJECT_ID=your_neon_project_id
JWT_SECRET=your_jwt_secret_key
BETTER_AUTH_SECRET=your_better_auth_secret
```

## Database Setup

### 1. Initialize the Database
```bash
cd backend
python -m src.models.init_db
```

### 2. Run Migrations
```bash
python -m src.models.migrate
```

## Running the Application

### 1. Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Verify the Service
Open your browser or use curl to verify the service is running:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T10:00:00Z"
}
```

## API Usage

### 1. Authentication
All API calls require a valid JWT token. Obtain a token by authenticating through Better Auth.

### 2. Chat Endpoint
Send a message to the AI chatbot:

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'
```

### 3. Expected Response
```json
{
  "conversation_id": 1,
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

## Development

### 1. Running Tests
Unit tests:
```bash
pytest tests/unit/
```

Integration tests:
```bash
pytest tests/integration/
```

Contract tests:
```bash
pytest tests/contract/
```

### 2. Code Structure
- `src/models/` - Data models using SQLModel
- `src/services/` - Business logic and data operations
- `src/api/` - API routes and request handling
- `src/agents/` - AI agent implementation
- `src/mcp_tools/` - MCP tools for AI interaction
- `src/auth/` - Authentication and authorization

### 3. Adding New MCP Tools
To add new MCP tools for the AI agent:

1. Create a new function in `src/mcp_tools/`
2. Decorate it appropriately for MCP exposure
3. Register it with the AI agent
4. Add tests for the new functionality

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Verify DATABASE_URL is correct
2. **Authentication Failures**: Check JWT token validity and secret configuration
3. **AI Service Errors**: Confirm OPENAI_API_KEY is valid and has sufficient quota
4. **Rate Limiting**: Respect API limits and implement appropriate delays

### Logs
Application logs are written to the console by default. For production, configure logging to write to files or external services.