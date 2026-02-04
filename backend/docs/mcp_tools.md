# MCP Tools Documentation

## Overview

The Todo AI Chatbot uses Model Context Protocol (MCP) tools to enable the AI agent to perform operations on tasks and conversations. These tools provide a secure and auditable interface between the AI agent and the application's data layer.

## Architecture

The MCP tools follow a layered architecture:
1. **AI Agent**: Interprets user input and decides which tools to call
2. **MCP Tools**: Provide the interface for operations (implemented in this layer)
3. **Services**: Contain business logic and data validation
4. **Database**: Persists the data using SQLModel

## Available MCP Tools

### Task Operations

#### add_task
Creates a new task for a user.

**Parameters:**
- `user_id` (string, required): ID of the user creating the task
- `title` (string, required): Title of the task (1-255 characters)
- `description` (string, optional): Description of the task (up to 1000 characters)

**Returns:**
```json
{
  "success": true,
  "task_id": 123,
  "message": "Task 'title' created successfully"
}
```

**Usage Example:**
```python
result = await task_tools.add_task(
    user_id="user123",
    title="Buy groceries",
    description="Milk, eggs, bread"
)
```

#### list_tasks
Lists tasks for a user, optionally filtered by status.

**Parameters:**
- `user_id` (string, required): ID of the user whose tasks to list
- `status` (string, optional): Filter by status ("all", "pending", "completed"). Defaults to "all".

**Returns:**
```json
{
  "success": true,
  "tasks": [
    {
      "id": 123,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-28T10:00:00Z"
    }
  ],
  "count": 1
}
```

#### complete_task
Marks a task as completed.

**Parameters:**
- `user_id` (string, required): ID of the user who owns the task
- `task_id` (integer, required): ID of the task to complete

**Returns:**
```json
{
  "success": true,
  "message": "Task 'title' marked as completed"
}
```

#### update_task
Updates an existing task.

**Parameters:**
- `user_id` (string, required): ID of the user who owns the task
- `task_id` (integer, required): ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task

**Returns:**
```json
{
  "success": true,
  "message": "Task updated successfully"
}
```

#### delete_task
Deletes a task.

**Parameters:**
- `user_id` (string, required): ID of the user who owns the task
- `task_id` (integer, required): ID of the task to delete

**Returns:**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

#### get_task_by_id
Gets a specific task by its ID.

**Parameters:**
- `user_id` (string, required): ID of the user who owns the task
- `task_id` (integer, required): ID of the task to retrieve

**Returns:**
```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-28T10:00:00Z",
    "updated_at": "2026-01-28T10:00:00Z",
    "user_id": "user123"
  }
}
```

#### get_recent_tasks
Gets the most recent tasks for a user.

**Parameters:**
- `user_id` (string, required): ID of the user whose tasks to retrieve
- `limit` (integer, optional): Maximum number of tasks to return (default: 10)

**Returns:**
```json
{
  "success": true,
  "tasks": [...],
  "count": 2
}
```

### Conversation Operations

#### create_conversation
Creates a new conversation for a user.

**Parameters:**
- `user_id` (string, required): ID of the user creating the conversation

**Returns:**
```json
{
  "success": true,
  "conversation_id": 123,
  "message": "Conversation created successfully"
}
```

#### add_message_to_conversation
Adds a message to a conversation.

**Parameters:**
- `user_id` (string, required): ID of the user adding the message
- `conversation_id` (integer, required): ID of the conversation to add to
- `role` (string, required): Role of the message ("user" or "assistant")
- `content` (string, required): Content of the message (1-10000 characters)

**Returns:**
```json
{
  "success": true,
  "message_id": 123,
  "message": "Message added to conversation successfully"
}
```

#### get_conversation_history
Gets the message history of a conversation.

**Parameters:**
- `user_id` (string, required): ID of the user requesting the history
- `conversation_id` (integer, required): ID of the conversation to retrieve

**Returns:**
```json
{
  "success": true,
  "messages": [
    {
      "id": 123,
      "role": "user",
      "content": "Message content",
      "created_at": "2026-01-28T10:00:00Z"
    }
  ],
  "count": 1
}
```

#### get_user_conversations
Gets all conversations for a user.

**Parameters:**
- `user_id` (string, required): ID of the user whose conversations to retrieve

**Returns:**
```json
{
  "success": true,
  "conversations": [
    {
      "id": 123,
      "created_at": "2026-01-28T10:00:00Z",
      "updated_at": "2026-01-28T10:00:00Z"
    }
  ],
  "count": 1
}
```

#### update_conversation_context
Updates the context of a conversation.

**Parameters:**
- `user_id` (string, required): ID of the user who owns the conversation
- `conversation_id` (integer, required): ID of the conversation to update
- `context_updates` (object, required): Dictionary of context updates to apply

**Returns:**
```json
{
  "success": true,
  "conversation_id": 123,
  "message": "Conversation context updated successfully"
}
```

#### get_conversation_context
Gets the context of a conversation.

**Parameters:**
- `user_id` (string, required): ID of the user who owns the conversation
- `conversation_id` (integer, required): ID of the conversation to retrieve

**Returns:**
```json
{
  "success": true,
  "context": {
    // Context data as a dictionary
  }
}
```

## Security Features

### User Isolation
All MCP tools validate that the user performing an operation is the owner of the resource being operated on. This ensures that users cannot access or modify each other's data.

### Input Validation
All tools validate input parameters before processing:
- User IDs are validated for proper format
- Task titles are validated for length and content
- Message content is validated for length and safety

### Audit Trail
All operations through MCP tools are logged for audit purposes, enabling tracking of all actions taken by the AI agent.

## Error Handling

MCP tools return consistent error responses:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

Common error scenarios include:
- Invalid user ID format
- Missing required parameters
- Unauthorized access to resources
- Database connection errors
- Validation failures

## Best Practices

### For AI Agent Integration
- Always pass user context to tools to ensure proper validation
- Handle both success and error responses appropriately
- Use conversation context to maintain state across interactions

### For System Monitoring
- Monitor tool call frequency and patterns
- Track error rates for each tool
- Log tool usage for audit and debugging purposes

## Testing MCP Tools

Unit tests should cover:
- Successful operation execution
- Error case handling
- User isolation validation
- Input validation scenarios
- Edge cases (empty inputs, maximum lengths, etc.)