# Data Model: Todo AI Chatbot with MCP Tools

## Overview
This document defines the data model for the Todo AI Chatbot with MCP Tools feature, outlining the entities, their attributes, relationships, and validation rules.

## Entities

### 1. Task
Represents a user's todo item with title, description, completion status, timestamps, and user ownership.

**Attributes**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key reference to user, indexed)
- `title`: String (Required, max 255 characters)
- `description`: Text (Optional, max 1000 characters)
- `completed`: Boolean (Default: false)
- `created_at`: DateTime (Auto-set on creation)
- `updated_at`: DateTime (Auto-updated on modification)

**Validation Rules**:
- Title must not be empty or exceed 255 characters
- User_id must correspond to an existing user
- Cannot modify another user's task

**Relationships**:
- Belongs to one user (via user_id)
- Part of one conversation (via conversation_id if applicable)

### 2. Conversation
Represents a logical grouping of messages between a user and the AI assistant.

**Attributes**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key reference to user, indexed)
- `created_at`: DateTime (Auto-set on creation)
- `updated_at`: DateTime (Auto-updated on modification)

**Validation Rules**:
- User_id must correspond to an existing user
- Cannot access another user's conversation

**Relationships**:
- Belongs to one user (via user_id)
- Contains many messages (one-to-many)

### 3. Message
Represents individual exchanges in a conversation, including user input and AI responses.

**Attributes**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key reference to user, indexed)
- `conversation_id`: Integer (Foreign Key reference to conversation, indexed)
- `role`: String (Required, values: "user" or "assistant")
- `content`: Text (Required, message content)
- `created_at`: DateTime (Auto-set on creation)

**Validation Rules**:
- Role must be either "user" or "assistant"
- Conversation_id must correspond to an existing conversation
- User_id must match the conversation owner
- Content must not be empty

**Relationships**:
- Belongs to one user (via user_id)
- Belongs to one conversation (via conversation_id)

## Relationships

```
User ||--o{ Conversation : "has"
Conversation }o--o{ Message : "contains"
User ||--o{ Task : "owns"
```

## State Transitions

### Task States
- **Pending**: completed = false (default state)
- **Completed**: completed = true (after completion operation)

### Message States
Messages are immutable once created and do not have state transitions.

## Constraints

### Primary Keys
- Each entity has a unique auto-incrementing integer ID
- Primary keys are non-null and unique

### Foreign Keys
- All foreign key relationships enforce referential integrity
- Cascading deletes are disabled to preserve historical data

### Indexes
- `user_id` fields are indexed for fast user-based queries
- `conversation_id` is indexed for fast conversation-based queries
- `created_at` fields are indexed for chronological ordering

## Security Considerations

### Access Control
- All queries must filter by user_id to enforce data isolation
- MCP tools must validate user ownership before operations
- No cross-user data access is permitted

### Data Validation
- All inputs are validated before database insertion
- Length limits prevent abuse
- Content is sanitized where appropriate