'use client';

/**
 * Landing page with redirect logic.
 * Redirects authenticated users to dashboard, unauthenticated to login.
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function LandingPage() {
  const router = useRouter();
  const { user, isLoading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        // Redirect authenticated users to dashboard
        router.push('/dashboard');
      } else {
        // Redirect unauthenticated users to login
        router.push('/login');
      }
    }
  }, [isLoading, isAuthenticated, router]);

  // Show loading state while checking auth
  return (
    <div className="background-gradient min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <h1 className="text-xl font-semibold text-gray-700">Loading...</h1>
        <p className="text-gray-500 mt-2">Checking authentication status</p>
      </div>
    </div>
  );
}
