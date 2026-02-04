---
id: 1
title: Create Spec AI Chatbot MCP
stage: spec
date: 2026-01-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-chatbot-mcp
branch: 003-ai-chatbot-mcp
user: Daw00d'sPc
command: sp.specify
labels: [spec, ai, chatbot, mcp, todo]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-chatbot-mcp/spec.md
  - specs/003-ai-chatbot-mcp/checklists/requirements.md
tests:
---

## Prompt

==================================================
PHASE III TECHNICAL SPECIFICATION
Todo AI Chatbot with MCP Tools
==================================================

OBJECTIVE:
Create an AI chatbot interface that manages todos through natural language using:
- OpenAI Agents SDK
- Official MCP SDK
- Stateless FastAPI backend
- Persistent PostgreSQL storage

--------------------------------------------------
TECHNOLOGY STACK
--------------------------------------------------
Frontend: OpenAI ChatKit
Backend: Python FastAPI
AI Framework: OpenAI Agents SDK
MCP Server: Official MCP SDK
ORM: SQLModel
Database: Neon Serverless PostgreSQL
Authentication: Better Auth
Documentation: Docusaurus

--------------------------------------------------
HIGH-LEVEL ARCHITECTURE
--------------------------------------------------
- Single stateless chat endpoint
- Agent performs reasoning and tool selection
- MCP server exposes task tools
- Database persists tasks, conversations, messages
- Frontend renders ChatKit UI

--------------------------------------------------
DATABASE MODELS
--------------------------------------------------

Task:
- id (integer)
- user_id (string)
- title (string)
- description (text)
- completed (boolean)
- created_at (timestamp)
- updated_at (timestamp)

Conversation:
- id (integer)
- user_id (string)
- created_at (timestamp)
- updated_at (timestamp)

Message:
- id (integer)
- user_id (string)
- conversation_id (integer)
- role (user | assistant)
- content (text)
- created_at (timestamp)

--------------------------------------------------
CHAT API
--------------------------------------------------

POST /api/{user_id}/chat

Request:
- conversation_id (integer, optional)
- message (string, required)

Response:
- conversation_id (integer)
- response (string)
- tool_calls (array)

All requests require valid JWT.
User ID in token must match URL user_id.

--------------------------------------------------
MCP TOOLS (MANDATORY)
--------------------------------------------------

add_task:
- user_id (string, required)
- title (string, required)
- description (string, optional)

list_tasks:
- user_id (string, required)
- status ("all" | "pending" | "completed")

complete_task:
- user_id (string, required)
- task_id (integer)

update_task:
- user_id (string, required)
- task_id (integer)
- title (optional)
- description (optional)

delete_task:
- user_id (string, required)
- task_id (integer)

--------------------------------------------------
AGENT BEHAVIOR RULES
--------------------------------------------------

Intent Mapping:
- add / remember → add_task
- list / show → list_tasks
- done / complete → complete_task
- delete / remove → delete_task
- change / update → update_task

Rules:
- Always confirm actions in natural language
- Ask clarifying questions if intent is ambiguous
- Gracefully handle missing tasks
- Never hallucinate task state
- Use MCP tools for every mutation

--------------------------------------------------
STATELESS CONVERSATION FLOW
--------------------------------------------------

1. Receive chat request
2. Fetch conversation + message history from DB
3. Persist user message
4. Run agent with MCP tools
5. Persist assistant response
6. Return response
7. Server holds no state between requests

--------------------------------------------------
FRONTEND SPEC
--------------------------------------------------

- Built using OpenAI ChatKit
- Stateless UI
- Renders full conversation history
- Uses Better Auth session for identity
- Displays confirmations and errors clearly

--------------------------------------------------
DOCUMENTATION (DOCUSAURUS)
--------------------------------------------------

The following must be documented:
- System architecture
- MCP tool definitions
- Agent behavior rules
- API reference
- Setup and deployment guide

--------------------------------------------------
DELIVERABLES
--------------------------------------------------

- Functional AI chatbot
- MCP server with task tools
- Stateless FastAPI backend
- Persistent conversations
- Docusaurus documentation site
- Monorepo with /frontend, /backend, /specs

==================================================
END OF SPECIFICATION
==================================================

INSTRUCTIONS:
- Do NOT implement until explicitly asked
- Follow this Constitution and Specification exactly
- Use Spec-Kit Plus conventions for any future specs

## Response snapshot

Created the technical specification for the Todo AI Chatbot with MCP Tools. The specification includes user scenarios for natural language todo management, stateful conversation context, and secure user data isolation. It defines functional requirements for chat API, authentication, task operations using MCP tools, and conversation persistence. Success criteria include 90% intent recognition accuracy, 3-second response times, and 99% uptime.

## Outcome

- ✅ Impact: Complete specification created for AI chatbot with MCP tools
- 🧪 Tests: N/A (specification document)
- 📁 Files: Created specs/003-ai-chatbot-mcp/spec.md and requirements checklist
- 🔁 Next prompts: Proceed to planning phase with /sp.plan
- 🧠 Reflection: Successfully captured all key requirements from the technical specification

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning phase