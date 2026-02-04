# Implementation Plan: Todo AI Chatbot with MCP Tools

**Branch**: `003-ai-chatbot-mcp` | **Date**: 2026-01-28 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-mcp/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an AI-powered conversational todo chatbot that allows users to manage tasks using natural language through OpenAI Agents SDK and MCP tools. The system will implement a stateless FastAPI backend that persists all conversation and task data in PostgreSQL, ensuring user data isolation and security. The architecture follows a tool-centric AI approach where all data operations are performed through MCP tools rather than direct database access.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: OpenAI Agents SDK, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, MCP SDK
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest with integration and unit tests
**Target Platform**: Linux server (cloud deployment)
**Project Type**: web - backend service with AI integration
**Performance Goals**: 95% of requests respond within 3 seconds, support 1000 concurrent users
**Constraints**: <3 second p95 response time, stateless server architecture, user data isolation
**Scale/Scope**: Multi-user support with conversation persistence, 10k+ users, horizontal scalability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven Development**: ✓ Compliant - following spec from spec.md
2. **Security & Identity**: ✓ Compliant - JWT authentication with Better Auth, user isolation enforced
3. **Stateless Server Architecture**: ✓ Compliant - no in-memory conversation state, all data persisted in DB
4. **Tool-Centric AI Development**: ✓ Compliant - all task operations through MCP tools, not direct DB access
5. **Technology Stack**: ✓ Compliant - using mandated technologies (FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, MCP tools)
6. **Code Quality Standards**: ✓ Compliant - following clean code principles
7. **Scope Lock**: ✓ Compliant - implementing only features specified in spec

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-mcp/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py          # Task entity
│   │   ├── conversation.py  # Conversation entity
│   │   └── message.py       # Message entity
│   ├── services/
│   │   ├── task_service.py     # Task business logic
│   │   ├── conversation_service.py  # Conversation management
│   │   └── auth_service.py        # Authentication logic
│   ├── api/
│   │   └── chat_router.py    # Chat API endpoints
│   ├── agents/
│   │   └── todo_agent.py     # OpenAI Agent implementation
│   ├── mcp_tools/
│   │   ├── task_mcp_tools.py    # MCP tools for task operations
│   │   └── conversation_mcp_tools.py  # MCP tools for conversation ops
│   └── auth/
│       └── jwt_handler.py      # JWT authentication handlers
├── tests/
│   ├── unit/
│   │   ├── test_models/      # Unit tests for models
│   │   └── test_services/    # Unit tests for services
│   ├── integration/
│   │   ├── test_api/         # API integration tests
│   │   └── test_agents/      # Agent integration tests
│   └── contract/
│       └── test_mcp_contracts/  # MCP tools contract tests
└── main.py                   # Application entry point
```

**Structure Decision**: Selected web application with backend only architecture, implementing the required backend structure with models, services, API routes, agents, and MCP tools in separate modules to support the AI chatbot functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
