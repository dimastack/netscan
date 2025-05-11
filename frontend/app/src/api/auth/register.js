import api from '../../services/client';

/**
 * Registers a new user by sending the details to the backend API.
 * 
 * @param {Object} user - The user details { username, email, password }
 * @returns {Promise<Object>} The response data or error message
 */
export async function registerUser({ username, email, password }) {
  try {
    const response = await api.post('/auth/register', {
      username,
      email,
      password,
    });
    return response.data;
  } catch (error) {
    console.error("Registration error:", error.response || error);
    throw error.response?.data || { error: 'Registration failed' };
  }
}
