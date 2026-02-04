---
id: 002
title: Phase II Full-Stack Constitution Upgrade
stage: constitution
date: 2026-01-19
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 001-todo-cli
user: user
command: /sp.constitution
labels: ["constitution", "phase-ii", "fullstack", "nextjs", "fastapi", "security", "monorepo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Project Constitution – Phase II
1. Purpose

This constitution defines the governing principles, constraints, and non-negotiable rules for Phase II: Todo Full-Stack Web Application. It serves as the authoritative reference for decisions, implementation boundaries, and evaluation criteria during development.

2. Core Objective

Transform the existing console-based Todo application into a modern, secure, multi-user full-stack web application with persistent storage, authentication, and RESTful APIs, implemented strictly using Claude Code + Spec-Kit Plus.

3. Development Governance
3.1 Spec-Driven Mandate

All development must follow the Agentic Dev Stack workflow:

Write or update specification

Generate an implementation plan

Break the plan into tasks

Implement exclusively via Claude Code

Manual coding is strictly prohibited.

Any change in requirements must be reflected in the specifications before implementation.

3.2 Single Source of Truth

All authoritative requirements live under /specs/**.

Code must conform to specifications at all times.

In case of conflict, specifications override implementation.

4. Security & Access Rules
4.1 Authentication Required

All backend API endpoints require authentication.

Unauthenticated requests must return 401 Unauthorized.

4.2 User Isolation

Users may only access, modify, or delete their own tasks.

Cross-user data access is considered a critical security failure.

4.3 Stateless Backend

Backend must not depend on frontend session state.

Authentication must be verified solely via JWT tokens.

5. Technology Constitution
Layer    Mandatory Technology
Frontend    Next.js 16+ (App Router)
Backend    Python FastAPI
ORM    SQLModel
Database    Neon Serverless PostgreSQL
Authentication    Better Auth (JWT-based)
Spec System    GitHub Spec-Kit + Spec-Kit Plus
Documentation    Docusaurus

No substitutions or alternatives are allowed.

6. Repository & Documentation Rules

Aandatory.

Frontend and backend must live in the same repository.

Specifications must reside under /specs/**.

Docusaurus must be used to generate and host developer-facing documentation derived from the specs.

7. Evaluation Criteria

The project will be judged on:

Correct application of spec-driven development

Quality and clarity of specifications

Secure JWT authentication flow

Correct enforcement of user-level data isolation

Clean monorepo organization monorepo structure is must

## Response snapshot

Updated constitution from v1.0.0 to v2.0.0 (MAJOR version bump) for Phase II Full-Stack Web Application.

**Key Changes:**
- Removed "In-Memory Only" principle (replaced by Neon PostgreSQL persistence)
- Removed "CLI-Only Interface" principle (replaced by Next.js frontend + FastAPI backend)
- Added "Security & Access Rules" as NON-NEGOTIABLE principle covering:
  - Authentication Required (all endpoints, 401 for unauthenticated)
  - User Isolation (users can only access their own tasks)
  - Stateless Backend (JWT-only authentication)
- Added "Monorepo Structure" as NON-NEGOTIABLE principle
- Completely overhauled Technology Stack section with mandated stack table
- Updated Project Structure to reflect frontend/backend monorepo layout
- Added Testing Requirements specific to authentication and user isolation

**Preserved:**
- Spec-Driven Development (NON-NEGOTIABLE)
- Code Quality Standards
- Scope Lock (updated to Phase II)
- Governance and Amendment Process

**Template Validation:**
- plan-template.md: Already supports web app structure (Option 2)
- spec-template.md: Technology-agnostic, compatible
- tasks-template.md: Contains web app path conventions

## Outcome

- ✅ Impact: Constitution upgraded for Phase II full-stack development, security principles codified, technology stack mandated
- 🧪 Tests: No tests (documentation artifact)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Create feature specification for authentication system with /sp.specify, or define todo CRUD features
- 🧠 Reflection: MAJOR version bump justified by fundamental changes to storage (in-memory → PostgreSQL), interface (CLI → web), and addition of security requirements. Templates already support web app structure, no template updates needed.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution upgrade successful
- Graders run and results (PASS/FAIL): N/A - no graders for constitution
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution enforcement during Phase II spec creation, especially security and technology stack compliance
