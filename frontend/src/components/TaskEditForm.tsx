'use client';

/**
 * Task edit form component.
 * Handles updating existing tasks with title and description.
 */

import React, { useState, useEffect } from 'react';
import { Task, UpdateTaskData } from '@/services/api';

interface TaskEditFormProps {
  task: Task;
  onSubmit: (taskId: string, data: UpdateTaskData) => Promise<void>;
  onCancel: () => void;
}

export function TaskEditForm({ task, onSubmit, onCancel }: TaskEditFormProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Update form when task changes
  useEffect(() => {
    setTitle(task.title);
    setDescription(task.description || '');
  }, [task]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validate title
    if (!title.trim()) {
      setError('Task title is required');
      return;
    }

    if (title.length > 200) {
      setError('Task title cannot exceed 200 characters');
      return;
    }

    setIsLoading(true);

    try {
      await onSubmit(task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="card w-full max-w-md">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Edit Task</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              id="edit-title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="input-field"
              placeholder="What needs to be done?"
              required
              disabled={isLoading}
              maxLength={200}
              autoFocus
            />
            <p className="text-xs text-gray-400 mt-1">
              {title.length}/200 characters
            </p>
          </div>

          <div>
            <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
              Description (optional)
            </label>
            <textarea
              id="edit-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="input-field"
              placeholder="Add more details..."
              rows={3}
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="error-message bg-red-50 p-3 rounded-md">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onCancel}
              className="btn-secondary flex-1"
              disabled={isLoading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary flex-1"
              disabled={isLoading}
            >
              {isLoading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
