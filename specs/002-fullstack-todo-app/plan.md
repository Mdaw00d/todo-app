# Implementation Plan: Full-Stack Todo Web Application

**Branch**: `002-fullstack-todo-app` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-todo-app/spec.md`

## Summary

Transform the existing console-based Todo application into a modern, secure, multi-user full-stack web application. The system will provide web-based task management with user authentication, persistent PostgreSQL storage via Neon, and user-isolated data access. Technical approach uses Next.js frontend with Python FastAPI backend, connected via RESTful API with JWT-based authentication through Better Auth.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.x (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, Next.js 16+ (App Router), shadcn/ui
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (Backend), Jest + Playwright (Frontend)
**Target Platform**: Web (Desktop + Mobile responsive)
**Project Type**: Web application (monorepo with frontend + backend)
**Performance Goals**: <2s page load, <500ms API response, support 1000 tasks per user
**Constraints**: JWT stateless auth, user data isolation, mobile-responsive UI
**Scale/Scope**: Multi-user application, ~6 API endpoints, ~5 frontend pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | ✅ PASS | Spec exists at `/specs/002-fullstack-todo-app/spec.md` with user scenarios and requirements |
| II. Security & Access Rules | ✅ PASS | JWT auth via Better Auth planned; user isolation in spec FR-016, FR-017 |
| III. Monorepo Structure | ✅ PASS | frontend/ and backend/ directories exist in repository root |
| IV. Technology Stack | ✅ PASS | Using mandated: Next.js, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Docusaurus |
| V. Code Quality Standards | ✅ PASS | Will follow single responsibility, no hardcoded secrets |
| VI. Scope Lock for Phase II | ✅ PASS | Features match approved spec only |

**Gate Result**: PASS - All constitution principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel entities (User, Task)
│   ├── services/        # Business logic (task_service, auth_service)
│   ├── api/             # FastAPI routes (/auth, /tasks)
│   └── auth/            # Better Auth integration
├── tests/
│   ├── unit/            # Unit tests for services
│   └── integration/     # API integration tests
├── requirements.txt
└── main.py              # FastAPI application entry

frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   │   ├── page.tsx           # Landing/Login page
│   │   ├── register/          # Registration page
│   │   ├── dashboard/         # Task list (protected)
│   │   └── layout.tsx         # Root layout with auth provider
│   ├── components/      # React components
│   │   ├── ui/          # shadcn/ui primitives
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthForms.tsx
│   └── services/        # API client services
│       ├── api.ts       # Base API client with auth
│       ├── auth.ts      # Authentication service
│       └── tasks.ts     # Task CRUD operations
├── tests/
│   ├── unit/            # Component tests (Jest)
│   └── e2e/             # End-to-end tests (Playwright)
└── package.json

docs/                    # Docusaurus documentation site
├── docusaurus.config.js
├── docs/
│   ├── overview.md
│   ├── api/
│   └── database/
└── sidebars.js
```

**Structure Decision**: Web application with monorepo layout as mandated by constitution. Frontend and backend in separate directories with shared specs directory.

## Complexity Tracking

> No constitution violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Architecture Overview

### Authentication Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│  Next.js    │────▶│   FastAPI   │
│             │     │  Frontend   │     │   Backend   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │    1. Login       │                   │
       │──────────────────▶│   2. POST /auth   │
       │                   │──────────────────▶│
       │                   │                   │ 3. Validate
       │                   │   4. JWT Token    │    credentials
       │                   │◀──────────────────│
       │   5. Store token  │                   │
       │◀──────────────────│                   │
       │                   │                   │
       │   6. API Request  │  7. Bearer Token  │
       │──────────────────▶│──────────────────▶│
       │                   │                   │ 8. Verify JWT
       │   9. Render       │   10. Response    │    + user isolation
       │◀──────────────────│◀──────────────────│
```

### Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                     │
├──────────────────────────────────────────────────────────────┤
│  AuthContext ─────▶ TaskService ─────▶ APIClient             │
│       │                  │                 │                  │
│       ▼                  ▼                 ▼                  │
│  Login/Register    CRUD Operations   HTTP + JWT Headers      │
└────────────────────────────┬─────────────────────────────────┘
                             │ REST API
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                        Backend (FastAPI)                      │
├──────────────────────────────────────────────────────────────┤
│  Auth Routes ─────▶ Task Routes ─────▶ Middleware            │
│       │                  │                 │                  │
│       ▼                  ▼                 ▼                  │
│  Better Auth       TaskService        JWT Validation         │
│       │                  │                                    │
│       ▼                  ▼                                    │
│  User Model ←────▶ Task Model ←────▶ SQLModel ORM           │
└────────────────────────────┬─────────────────────────────────┘
                             │ SQL
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                   Neon PostgreSQL                             │
├──────────────────────────────────────────────────────────────┤
│  users table                tasks table                       │
│  ├── id (PK)               ├── id (PK)                       │
│  ├── email (UNIQUE)        ├── user_id (FK)                  │
│  └── password_hash         ├── title                         │
│                            ├── description                    │
│                            ├── is_completed                   │
│                            ├── created_at                     │
│                            └── updated_at                     │
└──────────────────────────────────────────────────────────────┘
```

## API Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register | Create new user account | No |
| POST | /auth/login | Authenticate and receive JWT | No |
| POST | /auth/logout | Invalidate session | Yes |
| GET | /api/{user_id}/tasks | List all tasks for current user | Yes |
| POST | /api/{user_id}/tasks | Create new task | Yes |
| GET | /api/{user_id}/tasks/{id} | Get single task by ID | Yes |
| PUT | /api/{user_id}/tasks/{id} | Update task | Yes |
| DELETE | /api/{user_id}/tasks/{id} | Delete task | Yes |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion status | Yes |

## Next Steps

1. **Phase 0**: Generate `research.md` with technology research findings
2. **Phase 1**: Generate `data-model.md` with SQLModel entity definitions
3. **Phase 1**: Generate `contracts/openapi.yaml` with full API specification
4. **Phase 1**: Generate `quickstart.md` with development setup instructions