/**
 * Authentication service (FastAPI compatible)
 */

export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://todo-app-wj1h.onrender.com';

export interface User {
  id: string;
  email: string;
  full_name?: string;
  created_at: string;
  updated_at: string;
}

export interface Session {
  user: User;
  token: string;
}

const AUTH_STORAGE_KEY = 'todo_auth_session';

/* ===================== STORAGE ===================== */
export function getSession(): Session | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as Session;
  } catch {
    return null;
  }
}

export function saveSession(session: Session) {
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
}

export function clearSession() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
}

/**
 * Get the current auth token.
 */
export function getAuthToken(): string | null {
  const session = getSession();
  return session?.token || null;
}

/* ===================== LOGIN ===================== */
export async function signInWithEmail(email: string, password: string): Promise<Session> {
  if (!email || !password) throw new Error('Email and password are required');

  // Login expects form data
  const formData = new FormData();
  formData.append('email', email.trim());
  formData.append('password', password.trim());

  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    body: formData,
    // Don't set Content-Type header when using FormData - browser sets it automatically
  });

  if (!response.ok) {
    let errorMessage = 'Login failed';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData.detail);
      }
    } catch (e) {
      // If response is not JSON, use status text
      errorMessage = `Login failed with status: ${response.status}`;
    }

    console.error('LOGIN ERROR:', errorMessage);
    throw new Error(errorMessage);
  }

  const data = await response.json();
  const session: Session = {
    user: data.user,
    token: data.access_token
  };
  saveSession(session);
  return session;
}

/* ===================== REGISTER ===================== */
export async function signUpWithEmail(
  email: string,
  password: string,
  fullName?: string,
  passwordConfirm?: string
): Promise<Session> {
  if (!email || !password) throw new Error('Email and password are required');

  // Register expects JSON
  const payload = {
    email: email.trim(),
    password: password.trim(),
    full_name: fullName?.trim() || null,
    password_confirm: passwordConfirm || password.trim(),
  };

  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorMessage = 'Registration failed';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === 'string'
          ? errorData.detail
          : Array.isArray(errorData.detail)
            ? errorData.detail.map((e: any) => e.msg || e).join(' | ')
            : JSON.stringify(errorData.detail);
      }
    } catch (e) {
      // If response is not JSON, use status text
      errorMessage = `Registration failed with status: ${response.status}`;
    }

    console.error('REGISTER ERROR:', errorMessage);
    throw new Error(errorMessage);
  }

  const data = await response.json();
  const session: Session = {
    user: data.user,
    token: data.access_token
  };
  saveSession(session);
  return session;
}

/* ===================== LOGOUT ===================== */
export function signOutUser() {
  clearSession();
}

/* ===================== VERIFY ===================== */
export async function verifySession(): Promise<Session | null> {
  const session = getSession();
  if (!session) return null;

  // Since there's no /auth/me endpoint, just return the stored session
  // In a real implementation, you might want to create a /auth/me endpoint on the backend
  return session;
}
