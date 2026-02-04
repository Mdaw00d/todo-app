# Manual Test Scenarios: Todo CLI App

**Feature**: 001-todo-cli
**Date**: 2026-01-04
**Purpose**: Manual testing checklist for all user stories

## Test Scenario 1: Add and View Tasks (User Story 1 - P1)

### Test 1.1: Add Task Successfully
- [ ] Start application
- [ ] Select option 1 (Add Task)
- [ ] Enter task title: "Buy groceries"
- [ ] Verify success message with task ID 1
- [ ] Expected: Task created with ID 1

### Test 1.2: View Tasks with Content
- [ ] Add 3 tasks: "Buy groceries", "Write report", "Call dentist"
- [ ] Select option 2 (View Tasks)
- [ ] Verify all 3 tasks display with ID, title, and "Incomplete" status
- [ ] Expected: Table showing all 3 tasks

### Test 1.3: Empty Title Validation
- [ ] Select option 1 (Add Task)
- [ ] Enter empty title (just press Enter)
- [ ] Verify error message: "Task title cannot be empty"
- [ ] Expected: No task created, error displayed

### Test 1.4: Empty List Display
- [ ] Start fresh application (or delete all tasks)
- [ ] Select option 2 (View Tasks)
- [ ] Verify message: "No tasks found"
- [ ] Expected: Helpful empty state message

---

## Test Scenario 2: Mark Tasks Complete (User Story 2 - P2)

### Test 2.1: Mark Task Complete Successfully
- [ ] Add tasks with IDs 1, 2, 3
- [ ] Select option 5 (Mark Complete)
- [ ] Enter task ID: 2
- [ ] Verify success message
- [ ] View tasks - verify only task 2 shows "Complete"
- [ ] Expected: Task 2 status changed to Complete

### Test 2.2: Invalid Task ID
- [ ] Select option 5 (Mark Complete)
- [ ] Enter task ID: 999
- [ ] Verify error: "Task ID 999 not found"
- [ ] Expected: Clear error message, no changes

### Test 2.3: Mark Already Complete Task
- [ ] Mark task 1 as complete
- [ ] Mark task 1 as complete again
- [ ] Verify no error, task remains complete
- [ ] Expected: Idempotent operation

### Test 2.4: Non-Numeric ID Input
- [ ] Select option 5 (Mark Complete)
- [ ] Enter "abc" instead of number
- [ ] Verify error: "Please enter a valid number"
- [ ] Expected: Graceful error handling

---

## Test Scenario 3: Update Task Titles (User Story 3 - P3)

### Test 3.1: Update Task Successfully
- [ ] Add task "Buy milk"
- [ ] Select option 3 (Update Task)
- [ ] Enter task ID: 1
- [ ] Enter new title: "Buy almond milk"
- [ ] View tasks - verify title changed
- [ ] Expected: Only task 1 title updated

### Test 3.2: Update with Invalid ID
- [ ] Select option 3 (Update Task)
- [ ] Enter task ID: 999
- [ ] Verify error: "Task ID 999 not found"
- [ ] Expected: No changes, clear error

### Test 3.3: Update with Empty Title
- [ ] Select option 3 (Update Task)
- [ ] Enter valid task ID
- [ ] Enter empty title
- [ ] Verify error: "Task title cannot be empty"
- [ ] Expected: Title unchanged, error displayed

---

## Test Scenario 4: Delete Tasks (User Story 4 - P4)

### Test 4.1: Delete Task Successfully
- [ ] Add 5 tasks
- [ ] Select option 4 (Delete Task)
- [ ] Enter task ID: 3
- [ ] Verify success message
- [ ] View tasks - verify task 3 gone, others remain
- [ ] Expected: Task 3 deleted, 4 tasks remain

### Test 4.2: Delete with Invalid ID
- [ ] Select option 4 (Delete Task)
- [ ] Enter task ID: 999
- [ ] Verify error: "Task ID 999 not found"
- [ ] Expected: No changes, clear error

### Test 4.3: ID Not Reused After Deletion
- [ ] Note current task IDs (e.g., 1, 2, 4, 5)
- [ ] Delete task 2
- [ ] Add new task
- [ ] Verify new task gets next sequential ID (not 2)
- [ ] Expected: IDs never reused

---

## Test Scenario 5: Exit Application (User Story 5 - P5)

### Test 5.1: Normal Exit
- [ ] Add several tasks
- [ ] Select option 6 (Exit)
- [ ] Verify application terminates with goodbye message
- [ ] Expected: Clean exit

### Test 5.2: Data Not Persisted
- [ ] Add 3 tasks
- [ ] Exit application
- [ ] Restart application
- [ ] View tasks
- [ ] Verify list is empty
- [ ] Expected: All data lost (in-memory only)

### Test 5.3: Ctrl+C Graceful Exit
- [ ] Start application
- [ ] Press Ctrl+C
- [ ] Verify application exits gracefully
- [ ] Expected: No error, clean termination

---

## Test Scenario 6: Edge Cases

### Test 6.1: Invalid Menu Choice
- [ ] Enter menu choice: 10
- [ ] Verify error: "Invalid choice. Please enter 1-6"
- [ ] Expected: Menu displayed again

### Test 6.2: Long Task Title
- [ ] Add task with 500 character title
- [ ] Verify task created and displays correctly
- [ ] Expected: No truncation, full title stored

### Test 6.3: Many Tasks (100+)
- [ ] Add 100+ tasks
- [ ] View all tasks
- [ ] Verify all display correctly
- [ ] Expected: All tasks shown, no pagination

### Test 6.4: Non-Numeric Menu Input
- [ ] Enter "abc" at menu prompt
- [ ] Verify error message
- [ ] Expected: Menu displayed again

---

## Test Scenario 7: Complete Workflow (Success Criterion SC-007)

**Goal**: Complete workflow in under 2 minutes

- [ ] Start timer
- [ ] Add 3 tasks: "Task A", "Task B", "Task C"
- [ ] View all tasks
- [ ] Mark task 2 complete
- [ ] Update task 1 title to "Updated Task A"
- [ ] Delete task 3
- [ ] View final state (2 tasks: 1 incomplete, 1 complete)
- [ ] Stop timer
- [ ] Verify completed in < 2 minutes
- [ ] Expected: All operations successful, time target met

---

## Cross-Platform Testing

### Windows Testing
- [ ] Run on Windows 10/11
- [ ] Test all features
- [ ] Verify all operations work
- [ ] Note any platform-specific issues

### macOS Testing
- [ ] Run on macOS
- [ ] Test all features
- [ ] Verify all operations work
- [ ] Note any platform-specific issues

### Linux Testing
- [ ] Run on Linux (Ubuntu/Debian/etc.)
- [ ] Test all features
- [ ] Verify all operations work
- [ ] Note any platform-specific issues

---

## Performance Validation

- [ ] SC-001: Add task in < 5 seconds ✓ Expected: < 1 second
- [ ] SC-002: View tasks in < 2 seconds ✓ Expected: < 1 second
- [ ] SC-003: All operations error-free ✓
- [ ] SC-004: All 5 features work correctly ✓
- [ ] SC-005: Invalid inputs handled gracefully ✓
- [ ] SC-006: Cross-platform compatibility ✓
- [ ] SC-007: Complete workflow < 2 minutes ✓

---

## Final Validation Checklist

- [ ] All 14 functional requirements (FR-001 through FR-014) verified
- [ ] All 5 user stories tested independently
- [ ] All edge cases validated
- [ ] Cross-platform testing complete
- [ ] Performance targets met
- [ ] No crashes or unexpected errors
- [ ] Ready for production use
