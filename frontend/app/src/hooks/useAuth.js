import { useState, useEffect } from 'react';
import { validateToken } from '../api/auth/validateToken';
import { refreshToken } from '../api/auth/refreshToken';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkToken = async () => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      try {
        const isValid = await validateToken();
        setIsAuthenticated(isValid);
      } catch (error) {
        try {
          await refreshToken();
          const isValid = await validateToken();
          setIsAuthenticated(isValid);
        } catch (refreshError) {
          setIsAuthenticated(false);
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
    } else {
      setIsAuthenticated(false);
    }
    setLoading(false);
  };

  useEffect(() => {
    checkToken();
  }, []);

  const login = async () => {
    setLoading(true);
    await checkToken();
  };

  return { isAuthenticated, loading, login };
};
