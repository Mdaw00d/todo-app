'use client';

/**
 * Registration page with modern UI design.
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { RegisterForm } from '@/components/RegisterForm';

export default function RegisterPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-white border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="background-gradient min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md animate-fadeIn">
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-white rounded-2xl shadow-lg mb-4">
            <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
          <p className="text-white/80">Start organizing your tasks today</p>
        </div>

        {/* Register Card */}
        <div className="card glass">
          <RegisterForm />
        </div>

        {/* Footer */}
        <p className="text-center text-white/60 text-sm mt-6">
          Join thousands of productive users
        </p>
      </div>
    </div>
  );
}
