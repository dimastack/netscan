import api from '../../services/client';

/**
 * Sends login credentials and receives a JWT token.
 * 
 * @param {Object} credentials - { email, password }
 * @returns {Promise<Object>} response data or error
 */
export async function loginUser(credentials) {
  try {
    const response = await api.post('/auth/login', credentials);

    // Save token for later use
    if (response.data.access_token) {
      localStorage.setItem('accessToken', response.data.access_token);
    }

    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Login failed' };
  }
}