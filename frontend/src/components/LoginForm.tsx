'use client';

/**
 * Login form component for user authentication.
 * Fully compatible with FastAPI backend.
 */

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { signInWithEmail } from '@/services/auth';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginForm() {
  const router = useRouter();
  const { refreshAuth } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Form submission handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email.trim()) return setError('Email is required');
    if (!password.trim()) return setError('Password is required');

    setIsLoading(true);

    try {
      // 🔑 Send exact JSON FastAPI expects
      await signInWithEmail(email, password);

      refreshAuth();       // Update auth context
      router.push('/dashboard'); // Redirect after login
    } catch (err: any) {
      console.error('Login failed:', err);
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white shadow rounded-lg">
      <h2 className="text-2xl font-bold text-center mb-6">Sign in to your account</h2>

      {error && <div className="text-red-600 text-center mb-4">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-indigo-500"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-indigo-500"
        />

        <div className="flex items-center justify-between">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="mr-2"
            />
            Remember me
          </label>
          <Link href="/forgot-password" className="text-indigo-600 hover:underline text-sm">
            Forgot password?
          </Link>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
        >
          {isLoading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <p className="text-center text-sm text-gray-600 mt-4">
        Don't have an account?{' '}
        <Link href="/register" className="text-indigo-600 hover:underline">
          Sign Up
        </Link>
      </p>
    </div>
  );
}
