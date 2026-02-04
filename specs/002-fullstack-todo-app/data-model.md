# Data Model: Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-app
**Date**: 2026-01-21
**Status**: Complete

## Overview

This document defines the data model for the Full-Stack Todo Web Application using SQLModel. The model enforces user isolation by associating all tasks with a specific user, and implements validation rules from the feature specification.

---

## 1. Entity Definitions

### 1.1 User Entity

Represents a registered user who can authenticate and manage tasks.

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    password_confirm: str = Field(min_length=8, max_length=128)

class UserUpdate(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=100)

class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

**Validation Rules:**
- `email`: Required, unique, valid email format (enforced by application logic)
- `password`: Required for creation, minimum 8 characters, maximum 128 characters
- `full_name`: Optional, maximum 100 characters
- `hashed_password`: Stored securely using bcrypt

### 1.2 Task Entity

Represents a unit of work belonging to a user.

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(nullable=False, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskPublic(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

**Validation Rules:**
- `title`: Required, minimum 1 character, maximum 200 characters (FR-013)
- `description`: Optional, no character limit (FR-014)
- `is_completed`: Boolean, default False
- `user_id`: Required foreign key to User entity (enforces user isolation)
- `created_at`: Auto-populated timestamp (FR-015)
- `updated_at`: Auto-populated timestamp (FR-015)

---

## 2. Database Schema

### 2.1 Table Structure

```sql
-- users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

### 2.2 Relationships

- **One-to-Many**: User → Task (one user can have many tasks)
- **Cascade Delete**: When a user is deleted, all their tasks are automatically deleted
- **Foreign Key Constraint**: Ensures referential integrity between users and tasks

---

## 3. Data Validation & Constraints

### 3.1 Field-Level Validation

| Field | Type | Constraints | Enforcement |
|-------|------|-------------|-------------|
| User.email | VARCHAR(255) | UNIQUE, NOT NULL | Database constraint + Application validation |
| User.hashed_password | VARCHAR(255) | NOT NULL | Application validation |
| Task.title | VARCHAR(200) | NOT NULL, MIN_LENGTH(1) | Application validation (FR-013) |
| Task.description | TEXT | Optional | Application validation (FR-014) |
| Task.user_id | UUID | NOT NULL, FOREIGN KEY | Database constraint |

### 3.2 Business Logic Validation

1. **Task Title Length**: 1-200 characters (FR-013)
2. **User Isolation**: All task queries must be filtered by user_id (FR-016, FR-017)
3. **Ownership Verification**: Before any task modification, verify user owns the task
4. **Timestamps**: Automatically managed by SQLModel (FR-015)

---

## 4. API Representation Models

### 4.1 User Models

```python
# For registration requests
class UserRegistration(SQLModel):
    email: str
    full_name: Optional[str] = None
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)

# For login requests
class UserLogin(SQLModel):
    email: str
    password: str

# For login responses
class UserToken(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic

# For API responses
class UserResponse(SQLModel):
    success: bool = True
    data: UserPublic
    error: Optional[str] = None
```

### 4.2 Task Models

```python
# For API responses
class TaskResponse(SQLModel):
    success: bool = True
    data: TaskPublic
    error: Optional[str] = None

class TaskListResponse(SQLModel):
    success: bool = True
    data: List[TaskPublic]
    error: Optional[str] = None

class TaskToggleRequest(SQLModel):
    is_completed: bool
```

---

## 5. Security Considerations

### 5.1 Data Isolation

- **User Boundary**: All task queries must include `WHERE user_id = {current_user_id}`
- **Access Control**: Before any task operation, verify the task belongs to the authenticated user
- **Error Responses**: Return 404 (Not Found) rather than 403 (Forbidden) for tasks owned by other users to prevent user enumeration

### 5.2 Sensitive Data Protection

- **Passwords**: Never stored in plain text; always hashed using bcrypt
- **JWT Claims**: User ID stored in token, not sensitive information
- **API Responses**: Never expose hashed passwords or internal database IDs in public responses

---

## 6. Performance Considerations

### 6.1 Indexing Strategy

- Primary indexes on all ID fields (automatically created)
- Index on `tasks.user_id` for user-specific queries (critical for user isolation)
- Index on `tasks.is_completed` for filtering completed/incomplete tasks
- Index on `tasks.created_at` for chronological sorting

### 6.2 Query Optimization

- Always filter task queries by user_id to leverage index
- Use pagination for task lists (though not explicitly required, good practice for scalability)
- Batch operations where appropriate to minimize database round trips

---

## 7. Migration Considerations

### 7.1 Schema Evolution

- Use Alembic or similar tool for database migrations
- Maintain backward compatibility during schema changes
- Plan for zero-downtime deployments

### 7.2 Data Migration

- When adding required fields, provide sensible defaults
- Consider the impact on existing user data
- Plan rollback procedures for schema changes

---

## 8. Integration Points

### 8.1 Authentication Integration

- User model integrates with Better Auth for JWT generation
- User ID becomes the primary claim for authorization decisions
- Password hashing follows Better Auth recommendations

### 8.2 API Layer Integration

- SQLModel entities directly map to API request/response models
- Validation occurs at both database and API layers
- Error handling follows consistent patterns across all operations

---

This data model satisfies all functional requirements (FR-001 through FR-017) while implementing proper security and validation patterns. The model enforces user isolation (FR-016, FR-017) through foreign key relationships and will be enforced at the API layer through user_id filtering.