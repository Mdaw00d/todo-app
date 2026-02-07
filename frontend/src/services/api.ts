/**
 * API client for communicating with the backend.
 * Handles JWT injection, error handling, and typed responses.
 */

import { getAuthToken, getSession } from './auth';

// Environment configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Task data types
 */
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
}

/**
 * API error class for handling backend errors.
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Make an authenticated API request.
 * Automatically injects JWT token from the auth service.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken(); // getAuthToken is now synchronous

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  } as Record<string, string>;

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    // Remove credentials: 'include' for cross-origin requests between Vercel and Render
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      errorData.detail || 'An error occurred',
      response.status,
      errorData.code
    );
  }

  // Handle empty responses (204 No Content)
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * Health check endpoint.
 */
export async function checkHealth(): Promise<{ status: string }> {
  return apiRequest<{ status: string }>('/health');
}

/**
 * Task API methods
 */

/**
 * Get all tasks for the authenticated user.
 */
export async function listTasks(): Promise<Task[]> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  // The backend will validate authentication and return appropriate errors
  return apiRequest<Task[]>(`/users/${session.user.id}/tasks`);
}

/**
 * Get a single task by ID.
 */
export async function getTask(taskId: string): Promise<Task> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  return apiRequest<Task>(`/users/${session.user.id}/tasks/${taskId}`);
}

/**
 * Create a new task.
 */
export async function createTask(
  data: CreateTaskData
): Promise<Task> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  return apiRequest<Task>(`/users/${session.user.id}/tasks`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing task.
 */
export async function updateTask(
  taskId: string,
  data: UpdateTaskData
): Promise<Task> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  return apiRequest<Task>(`/users/${session.user.id}/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Delete a task.
 */
export async function deleteTask(
  taskId: string
): Promise<void> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  return apiRequest<void>(`/users/${session.user.id}/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

/**
 * Toggle task completion status.
 */
export async function toggleComplete(
  taskId: string
): Promise<Task> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  return apiRequest<Task>(`/users/${session.user.id}/tasks/${taskId}/complete`, {
    method: 'PATCH',
  });
}

/**
 * Chat with the AI assistant
 */
export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
}

export async function chatWithAssistant(request: ChatRequest): Promise<ChatResponse> {
  const session = getSession(); // Get user ID from session
  if (!session) {
    throw new ApiError('Not authenticated', 401);
  }
  // The apiRequest function handles authentication via getAuthToken
  return apiRequest<ChatResponse>(`/users/${session.user.id}/chat`, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}
