'use client';

/**
 * Dashboard page with modern task management UI.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { LogoutButton } from '@/components/LogoutButton';
import { TaskForm } from '@/components/TaskForm';
import { TaskList } from '@/components/TaskList';
import { TaskEditForm } from '@/components/TaskEditForm';
import ChatComponent from '@/components/ChatComponent';
import {
  Task,
  CreateTaskData,
  UpdateTaskData,
  listTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleComplete,
  ApiError,
} from '@/services/api';

export default function DashboardPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await listTasks();
      setTasks(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load tasks');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (data: CreateTaskData) => {
    const newTask = await createTask(data);
    setTasks((prev) => [newTask, ...prev]);
    setShowAddForm(false);
  };

  const handleUpdateTask = async (taskId: string, data: UpdateTaskData) => {
    const updatedTask = await updateTask(taskId, data);
    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? updatedTask : task))
    );
    setEditingTask(null);
  };

  const handleDeleteTask = async (taskId: string) => {
    await deleteTask(taskId);
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  const handleToggleComplete = async (taskId: string) => {
    const updatedTask = await toggleComplete(taskId);
    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? updatedTask : task))
    );
  };

  const completedCount = tasks.filter((t) => t.completed).length;
  const totalCount = tasks.length;

  return (
    <ProtectedRoute>
      <div className="min-h-screen">
        {/* Header */}
        <header className="bg-white/95 backdrop-blur-sm shadow-sm sticky top-0 z-40">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">My Tasks</h1>
                  <p className="text-sm text-gray-500">{user?.email}</p>
                </div>
              </div>
              <LogoutButton className="btn btn-ghost btn-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Sign Out
              </LogoutButton>
            </div>
          </div>
        </header>

        {/* Main content */}
        <main className="max-w-4xl mx-auto px-4 py-6">
          {/* Stats bar */}
          <div className="card mb-6 animate-fadeIn">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <p className="text-3xl font-bold text-gray-900">{totalCount}</p>
                  <p className="text-sm text-gray-500">Total Tasks</p>
                </div>
                <div className="h-12 w-px bg-gray-200"></div>
                <div className="text-center">
                  <p className="text-3xl font-bold text-green-600">{completedCount}</p>
                  <p className="text-sm text-gray-500">Completed</p>
                </div>
                <div className="h-12 w-px bg-gray-200"></div>
                <div className="text-center">
                  <p className="text-3xl font-bold text-indigo-600">{totalCount - completedCount}</p>
                  <p className="text-sm text-gray-500">Remaining</p>
                </div>
              </div>

              <button
                onClick={() => setShowAddForm(!showAddForm)}
                className="btn btn-primary"
              >
                {showAddForm ? (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Cancel
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Add Task
                  </>
                )}
              </button>
            </div>

            {/* Progress bar */}
            {totalCount > 0 && (
              <div className="mt-4">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Progress</span>
                  <span>{Math.round((completedCount / totalCount) * 100)}%</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full transition-all duration-500"
                    style={{ width: `${(completedCount / totalCount) * 100}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>

          {/* Error message */}
          {error && (
            <div className="mb-6 error-message animate-fadeIn">
              <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span>{error}</span>
              <button
                onClick={fetchTasks}
                className="ml-auto text-red-700 underline hover:no-underline"
              >
                Try again
              </button>
            </div>
          )}

          {/* Task creation form */}
          {showAddForm && (
            <div className="mb-6 animate-fadeIn">
              <TaskForm onSubmit={handleCreateTask} onCancel={() => setShowAddForm(false)} />
            </div>
          )}

          {/* Task list */}
          <TaskList
            tasks={tasks}
            isLoading={isLoading}
            onToggleComplete={handleToggleComplete}
            onEdit={setEditingTask}
            onDelete={handleDeleteTask}
          />

          {/* Chat Component */}
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">AI Task Assistant</h2>
            <ChatComponent />
          </div>
        </main>

        {/* Edit modal */}
        {editingTask && (
          <TaskEditForm
            task={editingTask}
            onSubmit={handleUpdateTask}
            onCancel={() => setEditingTask(null)}
          />
        )}
      </div>
    </ProtectedRoute>
  );
}
