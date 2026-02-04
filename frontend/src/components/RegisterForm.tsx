'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signUpWithEmail } from '@/services/auth';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';

export function RegisterForm() {
  const router = useRouter();
  const { refreshAuth } = useAuth();

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== passwordConfirm) return setError('Passwords do not match');
    if (password.length < 8) return setError('Password must be at least 8 characters');

    setIsLoading(true);

    try {
      await signUpWithEmail(email, password, fullName, passwordConfirm);
      refreshAuth();
      router.push('/dashboard');
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-12 space-y-4 p-6 bg-white shadow rounded-lg">
      <h2 className="text-2xl font-bold text-center">Create an account</h2>

      {error && <div className="text-red-600 text-center">{error}</div>}

      <input
        type="text"
        placeholder="Full Name"
        value={fullName}
        onChange={e => setFullName(e.target.value)}
        required
        className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-indigo-500"
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
        className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-indigo-500"
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
        minLength={8}
        className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-indigo-500"
      />

      <input
        type="password"
        placeholder="Confirm Password"
        value={passwordConfirm}
        onChange={e => setPasswordConfirm(e.target.value)}
        required
        minLength={8}
        className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-indigo-500"
      />

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        {isLoading ? 'Creating account...' : 'Sign Up'}
      </button>

      <p className="text-center text-sm text-gray-600">
        Already have an account?{' '}
        <Link href="/login" className="text-indigo-600 hover:underline">
          Sign In
        </Link>
      </p>
    </form>
  );
}
