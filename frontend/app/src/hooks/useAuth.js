// src/hooks/useAuth.js
import { useState, useEffect } from 'react';
import { validateToken } from '../api/auth/validateToken';

const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // To manage loading state
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkToken = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          // Validate token with the backend
          const isValid = await validateToken();
          setIsAuthenticated(isValid);
        } catch (error) {
          // If token is invalid, set to false
          setIsAuthenticated(false);
        }
      } else {
        // No token means not authenticated
        setIsAuthenticated(false);  
      }
      // Set loading to false once the check is done
      setLoading(false);
    };

    checkToken();
  }, []);

  return { isAuthenticated, loading };
};

export { useAuth };
