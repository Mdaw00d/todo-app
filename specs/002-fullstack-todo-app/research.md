# Research: Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-app
**Date**: 2026-01-21
**Status**: Complete

## Overview

This document captures technology research and decisions for the Full-Stack Todo Web Application. All technologies are mandated by the constitution (v2.0.0) - research focuses on best practices and integration patterns.

---

## 1. Frontend Framework: Next.js 16+ with App Router

### Decision
Use Next.js 16+ with App Router architecture for the frontend application.

### Rationale
- **Mandated by Constitution**: Technology stack is non-negotiable
- **App Router Benefits**: Server components, improved routing, built-in layouts
- **TypeScript Support**: First-class TypeScript integration
- **API Routes**: Can proxy requests to backend if needed

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Pages Router | Constitution mandates App Router |
| React SPA | Constitution mandates Next.js |
| Vue/Angular | Constitution mandates Next.js |

### Best Practices
- Use Server Components by default, Client Components only when needed
- Implement route groups for authentication boundaries
- Use `next/navigation` for programmatic navigation
- Store JWT in httpOnly cookies or secure localStorage with proper XSS protection

---

## 2. Backend Framework: Python FastAPI

### Decision
Use FastAPI with async endpoints for the REST API backend.

### Rationale
- **Mandated by Constitution**: Technology stack is non-negotiable
- **Performance**: Async support for high concurrency
- **OpenAPI**: Automatic API documentation generation
- **Type Safety**: Pydantic models for request/response validation

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Flask | Constitution mandates FastAPI |
| Django | Constitution mandates FastAPI |
| Express.js | Constitution mandates Python |

### Best Practices
- Use dependency injection for database sessions
- Implement proper exception handlers
- Use Pydantic models for all request/response schemas
- Apply CORS middleware for frontend communication

---

## 3. ORM: SQLModel

### Decision
Use SQLModel for database operations, combining SQLAlchemy and Pydantic.

### Rationale
- **Mandated by Constitution**: Technology stack is non-negotiable
- **Type Safety**: Combines Pydantic validation with SQLAlchemy ORM
- **FastAPI Integration**: Native compatibility with FastAPI
- **Simplicity**: Single model definition for both database and API

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Raw SQLAlchemy | Constitution mandates SQLModel |
| Django ORM | Constitution mandates SQLModel |
| Tortoise ORM | Constitution mandates SQLModel |

### Best Practices
- Define relationships explicitly with `Relationship`
- Use `Field` for column constraints and validation
- Separate read models (with relationships) from create/update models
- Use async session for better performance

---

## 4. Database: Neon Serverless PostgreSQL

### Decision
Use Neon Serverless PostgreSQL for persistent data storage.

### Rationale
- **Mandated by Constitution**: Technology stack is non-negotiable
- **Serverless**: Scales automatically, cost-effective for variable workloads
- **PostgreSQL Compatible**: Full PostgreSQL feature set
- **Branching**: Database branching for development/testing

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Local PostgreSQL | Constitution mandates Neon |
| SQLite | Constitution mandates Neon PostgreSQL |
| MySQL | Constitution mandates PostgreSQL |

### Best Practices
- Use connection pooling (Neon's built-in pooler)
- Set appropriate connection timeouts for serverless cold starts
- Use environment variables for connection strings
- Implement database migrations for schema changes

### Connection Configuration
```python
# Example connection string format
DATABASE_URL = "postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"
```

---

## 5. Authentication: Better Auth with JWT

### Decision
Use Better Auth library with JWT-based stateless authentication.

### Rationale
- **Mandated by Constitution**: Technology stack is non-negotiable
- **Stateless**: JWT enables horizontal scaling
- **Security**: Industry-standard authentication patterns
- **Flexibility**: Works with various frontend frameworks

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Session-based auth | Constitution mandates JWT stateless |
| Auth0/Firebase | Constitution mandates Better Auth |
| Custom JWT implementation | Better Auth provides tested patterns |

### Best Practices
- Store JWT in httpOnly cookies when possible
- Implement token refresh mechanism
- Set appropriate token expiration (24 hours as per spec assumptions)
- Validate tokens on every protected request
- Include user ID in token claims for user isolation

### Security Considerations
- Use HTTPS in production
- Implement CSRF protection
- Hash passwords with bcrypt (minimum 12 rounds)
- Never expose sensitive data in JWT payload

---

## 6. Documentation: Docusaurus

### Decision
Use Docusaurus for developer-facing documentation generated from specifications.

### Rationale
- **Mandated by Constitution**: Technology stack is non-negotiable
- **MDX Support**: Rich documentation with React components
- **Versioning**: Built-in documentation versioning
- **Search**: Algolia search integration available

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Nextra | Constitution mandates Docusaurus |
| GitBook | Constitution mandates Docusaurus |
| ReadTheDocs | Constitution mandates Docusaurus |

### Best Practices
- Organize docs by category (overview, api, database)
- Auto-generate API docs from OpenAPI spec
- Include code examples for common operations
- Keep docs in sync with specification changes

### Content Sources (per Phase II requirements)
```
/specs/overview.md
/specs/features/**
/specs/api/**
/specs/database/**
```

---

## 7. Testing Strategy

### Decision
Multi-layer testing approach with pytest (backend) and Jest + Playwright (frontend).

### Backend Testing
- **Unit Tests**: pytest for service layer logic
- **Integration Tests**: pytest with test database for API endpoints
- **Coverage Target**: Minimum 80% code coverage

### Frontend Testing
- **Unit Tests**: Jest + React Testing Library for components
- **E2E Tests**: Playwright for critical user flows
- **Coverage Target**: Critical paths fully covered

### Best Practices
- Use fixtures for test data setup
- Mock external services in unit tests
- Use separate test database for integration tests
- Run E2E tests against staging environment

---

## 8. User Isolation Strategy

### Decision
Enforce user isolation at the API layer with JWT claims.

### Implementation Pattern
```python
# Every task query includes user filter
async def get_tasks(user_id: str, db: Session):
    return db.query(Task).filter(Task.user_id == user_id).all()

# Ownership verification before modification
async def update_task(task_id: str, user_id: str, data: TaskUpdate, db: Session):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404)  # Or 403 for explicit denial
    # ... update logic
```

### Security Principles
- Extract user_id from verified JWT, never from request body
- Filter all queries by user_id
- Return 404 (not 403) for resources belonging to other users (prevents enumeration)
- Log all access attempts for audit trail

---

## 9. API Design Patterns

### Decision
RESTful API with consistent response formats and error handling.

### Response Format
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

### Error Format
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title is required",
    "details": { ... }
  }
}
```

### HTTP Status Codes
| Status | Usage |
|--------|-------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE |
| 400 | Validation error |
| 401 | Authentication required |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 500 | Internal server error |
| 503 | Service unavailable (database down) |

---

## 10. Environment Configuration

### Decision
Use environment variables for all configuration with `.env` files for local development.

### Required Variables
```env
# Database
DATABASE_URL=postgresql://...

# Authentication
BETTER_AUTH_SECRET=<secure-random-string>
BETTER_AUTH_URL=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Best Practices
- Never commit `.env` files to version control
- Provide `.env.example` with placeholder values
- Validate required environment variables at startup
- Use different secrets for each environment

---

## Summary

All technology decisions align with the constitution v2.0.0 mandates. Research focused on best practices for integration and security patterns rather than technology selection. Key findings:

1. **Authentication**: JWT with Better Auth, stored securely, validated on every request
2. **User Isolation**: Enforced at API layer by filtering all queries with user_id from JWT
3. **Data Model**: SQLModel for type-safe database operations
4. **API Design**: RESTful patterns with consistent response formats
5. **Documentation**: Docusaurus with content sourced from specs directory

No NEEDS CLARIFICATION items remain - all technical decisions are resolved.