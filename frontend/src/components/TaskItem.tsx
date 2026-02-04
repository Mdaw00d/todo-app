'use client';

/**
 * Individual task item component.
 * Displays task details with completion toggle, edit, and delete actions.
 */

import React, { useState } from 'react';
import { Task } from '@/services/api';

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
}

export function TaskItem({ task, onToggleComplete, onEdit, onDelete }: TaskItemProps) {
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggleComplete(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }
    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div
      className={`card mb-3 transition-all ${
        task.completed ? 'bg-gray-50 opacity-75' : 'bg-white'
      }`}
    >
      <div className="flex items-start gap-4">
        {/* Completion checkbox */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
            task.completed
              ? 'bg-green-500 border-green-500 text-white'
              : 'border-gray-300 hover:border-blue-500'
          }`}
          aria-label={task.completed ? 'Mark incomplete' : 'Mark complete'}
        >
          {task.completed && (
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </button>

        {/* Task content */}
        <div className="flex-grow min-w-0">
          <h3
            className={`font-medium text-gray-900 ${
              task.completed ? 'line-through text-gray-500' : ''
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`text-sm mt-1 ${
                task.completed ? 'text-gray-400 line-through' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            Created {formatDate(task.created_at)}
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex-shrink-0 flex gap-2">
          <button
            onClick={() => onEdit(task)}
            className="text-gray-400 hover:text-blue-600 transition-colors"
            aria-label="Edit task"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50"
            aria-label="Delete task"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
