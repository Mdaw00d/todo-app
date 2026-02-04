---
id: 1
title: Amend Constitution Phase III
stage: constitution
date: 2026-01-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-fullstack-todo-app
user: Daw00d'sPc
command: sp.constitution
labels: [constitution, mcp, ai-chatbot, phase-iii]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

PROJECT: Phase III – Todo AI Chatbot (MCP + Agents)

ROLE:
You are Claude Code operating in a Spec-Kit Plus, spec-driven monorepo.
You must NOT write manual code unless explicitly instructed by specs.
All implementation must strictly follow the Constitution and Specification below.

==================================================
PHASE III CONSTITUTION
Todo AI Chatbot – MCP Architecture
==================================================

PURPOSE:
Build an AI-powered conversational todo chatbot that allows users to manage tasks using natural language.
The system must use MCP (Model Context Protocol) tools and OpenAI Agents SDK.
The backend must be stateless; all state must persist in the database.

GOVERNING PRINCIPLES:
1. Spec-Driven Development
   - Specs are the single source of truth
   - Any behavior must be justified by specification
   - No ad-hoc logic

2. Agentic Dev Stack Workflow (MANDATORY)
   Write spec → Generate plan → Break into tasks → Implement via Claude Code

3. Stateless Server Architecture
   - FastAPI holds no in-memory conversation state
   - Each request reconstructs context from database
   - Server must be horizontally scalable

4. Tool-Centric AI
   - AI agents must NEVER mutate data directly
   - All task operations must go through MCP tools
   - MCP tools are authoritative and auditable

5. Security & Identity
   - Authentication via Better Auth (JWT)
   - User identity must be enforced at API and MCP tool level
   - No cross-user data access is allowed

NON-GOALS:
- No long-term memory outside database
- No server-side sessions
- No direct DB access by the AI agent
- No UI-driven mutations bypassing MCP tools

SUCCESS CRITERIA:
- Tasks fully manageable via chat
- Conversations persist across restarts
- MCP tools invoked correctly
- System remains stateless and scalable

## Response snapshot

Updated the project constitution to reflect Phase III requirements for the Todo AI Chatbot with MCP Architecture. The new constitution includes principles for spec-driven development, security & identity, stateless server architecture, tool-centric AI development, and the required technology stack. The version was bumped from 2.0.0 to 3.0.0 to reflect the major changes in focus from full-stack web application to AI chatbot with MCP architecture.

## Outcome

- ✅ Impact: Constitution updated to Phase III AI chatbot requirements with MCP architecture
- 🧪 Tests: N/A (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Continue with Phase III development following new constitution
- 🧠 Reflection: Successfully transitioned from Phase II web application to Phase III AI chatbot focus

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase III spec development