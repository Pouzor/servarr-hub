import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [profileLoading, setProfileLoading] = useState(false);

  // Auth methods - now handled by backend
  const signIn = async (email, password) => {
    try {
      // TODO: Implement backend authentication if needed
      console.log('Auth now handled by backend');
      return { data: null, error: { message: 'Authentication not configured' } };
    } catch (error) {
      return { error: { message: 'Network error. Please try again.' } };
    }
  };

  const signOut = async () => {
    try {
      setUser(null);
      setUserProfile(null);
      return { error: null };
    } catch (error) {
      return { error: { message: 'Network error. Please try again.' } };
    }
  };

  const updateProfile = async (updates) => {
    if (!user) return { error: { message: 'No user logged in' } };
    
    try {
      // TODO: Implement backend profile update if needed
      return { data: null, error: { message: 'Profile update not configured' } };
    } catch (error) {
      return { error: { message: 'Network error. Please try again.' } };
    }
  };

  const value = {
    user,
    userProfile,
    loading,
    profileLoading,
    signIn,
    signOut,
    updateProfile,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
