---
description: "Task list for Todo CLI App implementation"
---

# Tasks: Todo CLI App

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Manual CLI testing only - no automated test tasks generated (constitution allows tests to be optional for Phase I)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure (src/, src/models/, src/services/, src/cli/, tests/manual/)
- [x] T002 [P] Create empty __init__.py files in src/, src/models/, src/services/, src/cli/
- [x] T003 [P] Create tests/manual/test_scenarios.md with manual test checklist from spec

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Create Task dataclass in src/models/task.py with id, title, completed attributes and type hints
- [x] T005 Create TodoService class skeleton in src/services/todo_service.py with __init__, tasks dict, next_id counter
- [x] T006 [P] Create display module in src/cli/display.py with format_task_list() and show_message() functions
- [x] T007 [P] Create menu module in src/cli/menu.py with display_menu() and get_user_choice() functions

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks and view their complete task list

**Independent Test**: Launch app, add multiple tasks, view list to verify all appear with ID, title, and incomplete status. Test empty title rejection. Test empty list display.

### Implementation for User Story 1

- [x] T008 [US1] Implement add_task() method in src/services/todo_service.py with title validation, ID generation, task creation, and storage
- [x] T009 [US1] Implement get_all_tasks() method in src/services/todo_service.py to return list of all tasks from dictionary
- [x] T010 [US1] Implement "Add Task" menu handler in src/cli/menu.py that prompts for title and calls add_task()
- [x] T011 [US1] Implement "View Tasks" menu handler in src/cli/menu.py that calls get_all_tasks() and displays results
- [x] T012 [US1] Implement format_task_list() in src/cli/display.py to format tasks as table with ID, Title, Status columns
- [x] T013 [US1] Implement empty list handling in src/cli/display.py to show "No tasks found" message
- [x] T014 [US1] Create main.py entry point with main loop, menu display, and handlers for options 1 (Add) and 2 (View)
- [x] T015 [US1] Add input validation error messages in src/cli/menu.py for empty title (FR-002)
- [x] T016 [US1] Test User Story 1 manually per quickstart.md scenarios (add tasks, view tasks, empty title, empty list)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete to track progress

**Independent Test**: Add tasks, view (all incomplete), mark specific task complete by ID, view again to verify status changed. Test invalid ID handling. Test marking already complete task.

### Implementation for User Story 2

- [x] T017 [US2] Implement mark_complete() method in src/services/todo_service.py with ID validation and completed flag update
- [x] T018 [US2] Implement "Mark Complete" menu handler in src/cli/menu.py that prompts for task ID and calls mark_complete()
- [x] T019 [US2] Add menu option 5 (Mark Complete) to main loop in src/main.py
- [x] T020 [US2] Add ID validation error messages in src/cli/menu.py for invalid/non-existent task IDs (FR-009)
- [x] T021 [US2] Handle non-numeric input for task ID in src/cli/menu.py with try/except and error message
- [x] T022 [US2] Update format_task_list() in src/cli/display.py to show "Complete"/"Incomplete" status clearly
- [x] T023 [US2] Test User Story 2 manually per quickstart.md scenarios (mark complete, invalid ID, already complete)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Titles (Priority: P3)

**Goal**: Users can edit task titles when details change

**Independent Test**: Add tasks, update specific task title by ID, view to verify only that task changed. Test invalid ID and empty title rejection.

### Implementation for User Story 3

- [x] T024 [US3] Implement update_task() method in src/services/todo_service.py with ID validation, new title validation, and task title update
- [x] T025 [US3] Implement "Update Task" menu handler in src/cli/menu.py that prompts for task ID and new title, then calls update_task()
- [x] T026 [US3] Add menu option 3 (Update Task) to main loop in src/main.py
- [x] T027 [US3] Add validation for empty new title in src/cli/menu.py with error message
- [x] T028 [US3] Test User Story 3 manually per quickstart.md scenarios (update title, invalid ID, empty title)

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can remove tasks to keep list focused

**Independent Test**: Add multiple tasks, delete specific task by ID, view to verify only that task removed. Test invalid ID handling. Verify IDs not reassigned.

### Implementation for User Story 4

- [x] T029 [US4] Implement delete_task() method in src/services/todo_service.py with ID validation and task removal from dictionary
- [x] T030 [US4] Implement "Delete Task" menu handler in src/cli/menu.py that prompts for task ID and calls delete_task()
- [x] T031 [US4] Add menu option 4 (Delete Task) to main loop in src/main.py
- [x] T032 [US4] Test User Story 4 manually per quickstart.md scenarios (delete task, invalid ID, verify IDs not reused)

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Exit Application (Priority: P5)

**Goal**: Users can cleanly exit the application

**Independent Test**: Run app, perform operations, select Exit, verify app terminates. Restart and verify task list empty.

### Implementation for User Story 5

- [x] T033 [US5] Implement exit handling in main loop in src/main.py for menu option 6
- [x] T034 [US5] Add goodbye message when exiting in src/cli/display.py
- [x] T035 [US5] Add KeyboardInterrupt (Ctrl+C) handling in src/main.py to exit gracefully
- [x] T036 [US5] Test User Story 5 manually per quickstart.md scenarios (exit app, restart, verify data lost)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Add invalid menu choice handling in src/main.py with error message (FR-013)
- [x] T038 [P] Add type hints to all functions across all modules (models, services, cli, main)
- [x] T039 [P] Add docstrings to public methods in src/services/todo_service.py
- [x] T040 [P] Review code for PEP 8 compliance (naming conventions, line length, spacing)
- [x] T041 Run complete end-to-end test workflow per quickstart.md (add 3, view, mark 1 complete, update 1, delete 1, view final, exit)
- [x] T042 [P] Test cross-platform compatibility on Windows, macOS, Linux
- [x] T043 Test all edge cases from spec (non-numeric ID input, invalid menu choice, long titles, 100+ tasks)
- [x] T044 Final review: verify all 14 functional requirements (FR-001 through FR-014) are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - Depends on User Story 1 for testing workflow, but independently implementable
  - User Story 3 (P3): Can start after Foundational - Independent of other stories
  - User Story 4 (P4): Can start after Foundational - Independent of other stories
  - User Story 5 (P5): Can start after Foundational - Independent of other stories
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 data structures but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses Task entity from Foundational, independent of other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Uses Task entity from Foundational, independent of other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Uses main loop structure, independent of other stories

### Within Each User Story

- Foundational tasks (Task model, TodoService skeleton) MUST complete before any user story
- Service layer methods before menu handlers
- Menu handlers before main.py integration
- Implementation before testing

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003)
- All Foundational tasks marked [P] can run in parallel (T004, T006, T007 - after T005 skeleton exists)
- Once Foundational phase completes, all user stories CAN start in parallel if team capacity allows
- All Polish tasks marked [P] can run in parallel (T037, T038, T039, T040, T042)

---

## Parallel Example: Foundational Phase

```bash
# After T001 creates directory structure, these can run together:
Task T002: Create all __init__.py files
Task T003: Create test_scenarios.md
Task T004: Create Task dataclass
Task T006: Create display module
Task T007: Create menu module

# Then sequentially:
Task T005: Create TodoService skeleton (needs Task model from T004)
```

---

## Parallel Example: User Story 1

```bash
# These service methods can be implemented in parallel:
Task T008: Implement add_task() in todo_service.py
Task T009: Implement get_all_tasks() in todo_service.py

# These CLI functions can be implemented in parallel (after service layer):
Task T010: Add Task menu handler
Task T011: View Tasks menu handler
Task T012: Format task list function
Task T013: Empty list handling
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007) - CRITICAL blocking phase
3. Complete Phase 3: User Story 1 (T008-T016)
4. **STOP and VALIDATE**: Test User Story 1 independently per quickstart.md
5. Deploy/demo if ready - you now have a working MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T008-T016) → Test independently → You have MVP (add + view tasks)
3. Add User Story 2 (T017-T023) → Test independently → Can now track completion
4. Add User Story 3 (T024-T028) → Test independently → Can now edit tasks
5. Add User Story 4 (T029-T032) → Test independently → Can now delete tasks
6. Add User Story 5 (T033-T036) → Test independently → Complete feature set
7. Complete Polish (T037-T044) → Production ready

Each story adds value without breaking previous stories.

### Sequential Implementation (Single Developer)

1. Setup (Phase 1): T001 → T002 → T003
2. Foundational (Phase 2): T004 → T005 → T006 → T007
3. User Story 1 (P1): T008 → T009 → T010 → T011 → T012 → T013 → T014 → T015 → T016 (TEST)
4. User Story 2 (P2): T017 → T018 → T019 → T020 → T021 → T022 → T023 (TEST)
5. User Story 3 (P3): T024 → T025 → T026 → T027 → T028 (TEST)
6. User Story 4 (P4): T029 → T030 → T031 → T032 (TEST)
7. User Story 5 (P5): T033 → T034 → T035 → T036 (TEST)
8. Polish (Phase 8): T037 → T038 → T039 → T040 → T041 → T042 → T043 → T044

Total: 44 tasks in priority order

---

## Task Summary by Phase

| Phase | Task Count | Purpose | Parallel Tasks |
|-------|-----------|---------|----------------|
| Phase 1: Setup | 3 | Project structure initialization | T002, T003 |
| Phase 2: Foundational | 4 | Core infrastructure (BLOCKS all stories) | T004, T006, T007 |
| Phase 3: User Story 1 (P1) | 9 | Add and View tasks (MVP) | T008-T009, T010-T013 |
| Phase 4: User Story 2 (P2) | 7 | Mark tasks complete | None |
| Phase 5: User Story 3 (P3) | 5 | Update task titles | None |
| Phase 6: User Story 4 (P4) | 4 | Delete tasks | None |
| Phase 7: User Story 5 (P5) | 4 | Exit application | T033-T034 |
| Phase 8: Polish | 8 | Quality, testing, cross-cutting | T037-T040, T042 |
| **TOTAL** | **44 tasks** | **Complete feature** | **13 parallelizable** |

---

## File Modification Summary

| File | Tasks | Purpose |
|------|-------|---------|
| src/models/task.py | T004 | Task dataclass definition |
| src/services/todo_service.py | T005, T008, T009, T017, T024, T029, T039 | Business logic and validation |
| src/cli/display.py | T006, T012, T013, T022, T034 | Output formatting |
| src/cli/menu.py | T007, T010, T011, T015, T018, T020, T021, T025, T027, T030 | Input handling and menu |
| src/main.py | T014, T019, T026, T031, T033, T035, T037 | Entry point and main loop |
| tests/manual/test_scenarios.md | T003 | Manual test documentation |
| All Python files | T038, T040 | Type hints and PEP 8 compliance |

---

## Success Criteria Mapping

| Success Criterion | Related Tasks | Validation |
|-------------------|--------------|------------|
| SC-001: Add task in < 5 sec | T008-T015 | Test in T016 |
| SC-002: View tasks in < 2 sec | T009-T013 | Test in T016 |
| SC-003: All operations error-free | T008-T036 | Test in T041 |
| SC-004: All features work | T008-T036 | Test in T041 |
| SC-005: Handle invalid inputs | T015, T020, T021, T027, T037 | Test in T043 |
| SC-006: Cross-platform | T042 | Test on Windows, macOS, Linux |
| SC-007: Complete workflow < 2 min | T008-T036 | Test in T041 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Foundational phase (T004-T007) is CRITICAL - all user stories depend on it
- Commit after each task or logical group
- Stop at any user story checkpoint to validate independently
- MVP = Phase 1 + Phase 2 + Phase 3 (Setup + Foundational + User Story 1)
- Constitution compliance: Exactly 5 features (Add, View, Update, Delete, Mark Complete, Exit), no persistence, CLI-only, Python stdlib only
- No automated test tasks - manual testing per quickstart.md is sufficient for Phase I per constitution
