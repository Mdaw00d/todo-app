<!-- SYNC IMPACT REPORT
==================
Version Change: 2.0.0 → 3.0.0 (MAJOR)
Modified Principles:
  - "Core Objective" → Completely overhauled for AI Chatbot with MCP Architecture
  - "Technology Stack" → Updated to include OpenAI Agents SDK, MCP tools, and stateless server architecture
  - "Security & Access Rules" → Enhanced to include MCP tool-level security enforcement
  - "Code Quality Standards" → Updated to emphasize tool-centric AI development
  - "Scope Lock for Phase II" → Updated to "Scope Lock for Phase III" with AI chatbot focus
Added Sections:
  - Tool-Centric AI Development (AI agents must use MCP tools for all operations)
  - MCP Architecture Requirements (Stateless server, database persistence)
Removed Sections:
  - Frontend-specific requirements (Next.js focus removed)
Templates Requiring Updates:
  ⚠ plan-template.md - Needs MCP architecture guidance (pending)
  ⚠ spec-template.md - Needs AI chatbot scenario alignment (pending)
  ⚠ tasks-template.md - Needs MCP tool-focused task structure (pending)
Follow-up TODOs:
  - Update templates to reflect MCP architecture
  - Add AI agent testing requirements
  - Document MCP tool security patterns
-->

# Todo AI Chatbot Constitution – Phase III

## Purpose

This constitution defines the governing principles, constraints, and non-negotiable rules for Phase III: Todo AI Chatbot with MCP Architecture. It serves as the authoritative reference for decisions, implementation boundaries, and evaluation criteria during development.

## Core Objective

Build an AI-powered conversational todo chatbot that allows users to manage tasks using natural language. The system must use MCP (Model Context Protocol) tools and OpenAI Agents SDK. The backend must be stateless; all state must persist in the database.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Specification is the single source of truth for all development work.

- **MUST** write specifications before any code implementation
- **MUST** follow strict workflow: Spec → Plan → Tasks → Implement
- **MUST** use Claude Code + Spec-Kit Plus for all development
- **MUST NOT** write manual code outside of Claude Code execution
- Any change in requirements **MUST** be reflected in specifications before implementation
- In case of conflict, specifications override implementation

**Rationale**: Spec-driven development ensures clarity, reduces rework, and maintains alignment between intent and implementation. Manual coding is prohibited to ensure traceability and consistency.

### II. Security & Identity (NON-NEGOTIABLE)

All data access must be authenticated and user-isolated with MCP-level enforcement.

#### Authentication Required
- **MUST** require authentication for all backend API endpoints
- **MUST** return 401 Unauthorized for unauthenticated requests
- **MUST** implement Better Auth with JWT-based authentication

#### User Isolation
- **MUST** ensure users can only access, modify, or delete their own tasks
- **MUST** treat cross-user data access as a critical security failure
- **MUST** enforce user isolation at the API layer and MCP tool level

#### Identity Enforcement
- **MUST** verify user identity at both API and MCP tool layers
- **MUST** ensure no cross-user data access is allowed through MCP tools
- **MUST** validate user permissions in all MCP tool operations

**Rationale**: Security is foundational for multi-user applications. JWT-based stateless authentication combined with MCP-level enforcement enables scalability while user isolation prevents data breaches and maintains privacy.

### III. Stateless Server Architecture (NON-NEGOTIABLE)

Backend must hold no in-memory conversation state.

- **MUST NOT** store conversation state in server memory
- **MUST** reconstruct context from database for each request
- **MUST** enable horizontal scalability without shared state
- **MUST** ensure server restarts do not lose conversation continuity
- **MUST** persist all conversation state in the database

**Rationale**: Stateless architecture enables horizontal scaling, improves reliability, and ensures conversations persist across server restarts. All state must be in the database to maintain consistency and enable horizontal scaling.

### IV. Tool-Centric AI Development (NON-NEGOTIABLE)

AI agents must use MCP tools for all data operations.

- **MUST NOT** allow AI agents to mutate data directly
- **MUST** route all task operations through MCP tools
- **MUST** ensure MCP tools are authoritative and auditable
- **MUST** implement all task management through MCP tools
- **MUST** maintain audit trails through MCP tool usage

**Rationale**: Tool-centric AI ensures data integrity, provides auditability, and enforces security boundaries. MCP tools act as the authoritative interface between AI agents and data operations.

### V. Technology Stack (NON-NEGOTIABLE)

No substitutions or alternatives are allowed.

| Layer           | Mandatory Technology                |
|-----------------|-------------------------------------|
| AI Framework    | OpenAI Agents SDK                   |
| MCP Tools       | Model Context Protocol tools        |
| Backend         | Python FastAPI                      |
| ORM             | SQLModel                            |
| Database        | Neon Serverless PostgreSQL          |
| Authentication  | Better Auth (JWT-based)             |
| Spec System     | GitHub Spec-Kit + Spec-Kit Plus     |

- **MUST NOT** substitute any technology in the stack
- **MUST** use OpenAI Agents SDK for AI functionality
- **MUST** use MCP tools for all data operations
- **MUST** use SQLModel for all database operations

**Rationale**: Mandated stack ensures consistency, reduces decision fatigue, and enables focused evaluation of AI chatbot development practices with MCP architecture rather than technology choices.

### VI. Code Quality Standards

Code must be clean, readable, and modular with emphasis on tool-centric development.

- **MUST** follow single responsibility principle for functions and modules
- **MUST** use clear, descriptive naming conventions
- **MUST** implement graceful error handling with meaningful messages
- **MUST NOT** duplicate logic across functions
- **MUST** be readable without excessive comments (self-documenting code)
- **MUST NOT** hardcode secrets or tokens; use environment variables
- **MUST** ensure MCP tools are properly tested and secured

**Rationale**: High code quality ensures maintainability, reduces bugs, and makes the codebase easier to extend and audit. Special attention to MCP tool security is essential.

### VII. Scope Lock for Phase III

Feature scope is defined by spec-driven requirements only.

- **MUST** implement only features specified in approved specs under `/specs/**`
- **MUST NOT** implement features not specified in approved specifications
- **MUST** defer feature requests outside Phase III scope to future phases
- **MUST** document any scope expansion requests for future consideration
- **MUST** focus on AI chatbot functionality with MCP architecture

**Rationale**: Strict scope control prevents feature creep, ensures timely delivery, and maintains focus on validated requirements for the AI chatbot with MCP architecture.

## Project Structure

```text
/
├── backend/                 # Python FastAPI + OpenAI Agents SDK
│   ├── src/
│   │   ├── models/         # SQLModel entities
│   │   ├── services/       # Business logic
│   │   ├── api/            # API routes
│   │   ├── agents/         # AI agent implementations
│   │   ├── mcp_tools/      # MCP tools for AI interaction
│   │   └── auth/           # Better Auth integration
│   └── tests/
├── specs/                   # All specifications (Single Source of Truth)
│   └── <feature>/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── docs/                    # Documentation
├── history/                 # Prompt History Records & ADRs
│   ├── prompts/
│   └── adr/
└── .specify/               # Spec-Kit Plus templates and scripts
```

## Development Workflow

### Mandatory Sequence

1. **Specification First**: Write complete spec.md with user scenarios and requirements
2. **Architectural Planning**: Create plan.md with MCP architecture approach and structure
3. **Task Breakdown**: Generate tasks.md with actionable, testable tasks
4. **Implementation**: Execute tasks using Claude Code exclusively

### Quality Gates

- **Spec Review**: All requirements clear and testable before planning
- **Plan Review**: Architecture decisions align with constitution principles
- **Task Review**: Tasks map to spec requirements with clear acceptance criteria
- **Implementation Review**: Code passes quality standards, tests pass, security verified

### Testing Requirements

- **MUST** implement automated tests for all API endpoints
- **MUST** verify authentication and authorization in tests
- **MUST** validate user isolation in integration tests
- **MUST** ensure AI agent interactions work correctly
- **MUST** verify MCP tools function properly and securely
- **MUST** validate conversation persistence across restarts

## Evaluation Criteria

The project will be judged on:

1. **Correct application of spec-driven development**
2. **Quality and clarity of specifications**
3. **Secure JWT authentication flow**
4. **Correct enforcement of user-level data isolation**
5. **Proper implementation of MCP architecture**
6. **Effective AI chatbot functionality**
7. **Stateless server architecture compliance**

## Governance

This constitution supersedes all other practices and preferences. Any development work must comply with these principles.

### Amendment Process

1. Proposed amendments must be documented with rationale
2. Amendments require explicit approval
3. Version bump follows semantic versioning:
   - **MAJOR**: Removing or fundamentally changing core principles
   - **MINOR**: Adding new principles or sections
   - **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance

- All code reviews must verify constitutional compliance
- Deviations from mandated technology stack require constitutional amendment
- For runtime development guidance, refer to `CLAUDE.md` and `.specify/` templates
- Security violations (auth bypass, user isolation failures, direct DB access by AI) require immediate remediation

### Enforcement

- Pull requests violating principles must be rejected
- Feature requests outside Phase III scope must be deferred
- Technology substitutions are not permitted without constitutional amendment
- Direct database access by AI agents must be prevented

---

**Version**: 3.0.0 | **Ratified**: 2026-01-28 | **Last Amended**: 2026-01-28
