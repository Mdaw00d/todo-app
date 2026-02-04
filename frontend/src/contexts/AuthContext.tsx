'use client';

/**
 * Auth context for managing user authentication state.
 * Provides user data and loading state to all child components.
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getSession, signOutUser, verifySession, User, Session } from '@/services/auth';

/**
 * Auth context value type.
 */
interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  logout: () => Promise<void>;
  refreshAuth: () => void;
}

/**
 * Auth context with default values.
 */
const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  isAuthenticated: false,
  logout: async () => {},
  refreshAuth: () => {},
});

/**
 * Props for the AuthProvider component.
 */
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Auth provider component that wraps the application.
 * Manages authentication state and provides it to all children.
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Check for existing session and verify with backend on mount.
   */
  const checkAuth = async () => {
    setIsLoading(true);

    try {
      // Check if we have a session in localStorage
      const session = await verifySession();

      if (session?.user) {
        setUser(session.user);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Error verifying session:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * Refresh auth state (call after login/register).
   */
  const refreshAuth = () => {
    checkAuth();
  };

  /**
   * Logout the current user.
   */
  const logout = async () => {
    try {
      await signOutUser();
      setUser(null);
      await checkAuth(); // Refresh auth state after logout
    } catch (error) {
      console.error('Logout failed:', error);
      throw error;
    }
  };

  // Determine authentication status based on user presence
  const authenticated = !!user && !isLoading;

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: authenticated,
    logout,
    refreshAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access auth context.
 * Must be used within an AuthProvider.
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export type { User };
