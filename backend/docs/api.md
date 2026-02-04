# Todo AI Chatbot API Documentation

## Overview

The Todo AI Chatbot API provides endpoints for interacting with the AI-powered todo management system. The API allows users to manage their tasks using natural language commands.

## Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer {jwt_token}
```

The user ID in the JWT token must match the user ID in the URL path.

## Base URL

All endpoints are prefixed with `/api`

## Endpoints

### POST /{user_id}/chat

Interact with the AI chatbot to manage todos using natural language.

#### Parameters

- `user_id` (path): The ID of the user making the request. Must match the user ID in the JWT token.

#### Request Body

```json
{
  "conversation_id": 123,
  "message": "Add a task to call mom"
}
```

- `conversation_id` (integer, optional): The ID of the conversation to continue. If not provided, a new conversation will be started.
- `message` (string, required): The natural language message to send to the AI chatbot. Must be between 1 and 10000 characters.

#### Response

```json
{
  "conversation_id": 123,
  "response": "I've added the task 'call mom' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "call mom",
        "description": null
      }
    }
  ]
}
```

- `conversation_id` (integer): The ID of the conversation
- `response` (string): The AI's response to the user's message
- `tool_calls` (array): Array of MCP tools called by the AI agent

#### Example Request

```bash
curl -X POST https://api.todo-chatbot.com/api/user123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "conversation_id": null,
    "message": "Add a task to buy groceries"
  }'
```

### GET /health

Check the health status of the application.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T10:00:00Z",
  "service": "todo-ai-chatbot",
  "version": "1.0.0"
}
```

### GET /ready

Check if the application is ready to serve traffic.

#### Response

```json
{
  "status": "ready",
  "timestamp": "2026-01-28T10:00:00Z",
  "service": "todo-ai-chatbot",
  "version": "1.0.0"
}
```

## Error Responses

The API returns standard HTTP error codes:

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token does not match URL user_id
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "error": "ErrorType",
  "message": "Human-readable error message",
  "detail": "Additional error details"
}
```

## Rate Limiting

Requests are limited to 100 per hour per user. Exceeding this limit will result in a 429 status code.

## Data Models

### Task

Represents a user's todo item.

- `id` (integer): Unique identifier
- `title` (string): Task title (1-255 characters)
- `description` (string, optional): Task description (up to 1000 characters)
- `completed` (boolean): Whether the task is completed
- `user_id` (string): ID of the user who owns the task
- `created_at` (string): Creation timestamp (ISO 8601 format)
- `updated_at` (string): Last update timestamp (ISO 8601 format)

### Conversation

Represents a logical grouping of messages.

- `id` (integer): Unique identifier
- `user_id` (string): ID of the user who owns the conversation
- `created_at` (string): Creation timestamp (ISO 8601 format)
- `updated_at` (string): Last update timestamp (ISO 8601 format)
- `context_data` (string, optional): JSON string storing conversation context

### Message

Represents individual exchanges in a conversation.

- `id` (integer): Unique identifier
- `user_id` (string): ID of the user who sent the message
- `conversation_id` (integer): ID of the conversation
- `role` (string): "user" or "assistant"
- `content` (string): Message content (1-10000 characters)
- `created_at` (string): Creation timestamp (ISO 8601 format)

## MCP Tools

The AI agent uses the following MCP tools for task operations:

### add_task
- Parameters: `user_id`, `title`, `description` (optional)
- Creates a new task for the user

### list_tasks
- Parameters: `user_id`, `status` ("all", "pending", "completed")
- Lists tasks for the user

### complete_task
- Parameters: `user_id`, `task_id`
- Marks a task as completed

### update_task
- Parameters: `user_id`, `task_id`, `title` (optional), `description` (optional)
- Updates an existing task

### delete_task
- Parameters: `user_id`, `task_id`
- Deletes a task