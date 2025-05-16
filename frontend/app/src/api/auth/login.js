import api from '../../services/client';

/**
 * Sends login credentials to the backend and stores the received tokens.
 * 
 * On successful authentication, both access and refresh tokens are stored in localStorage.
 *
 * @param {Object} credentials - The login form input: { email, password }
 * @returns {Promise<Object>} The response data including access and refresh tokens.
 * @throws {Object} Error data if login fails.
 */
export async function loginUser(credentials) {
  try {
    const response = await api.post('/auth/login', credentials);

    const { access_token, refresh_token } = response.data;

    if (!access_token || !refresh_token) {
      throw new Error('Tokens missing in response');
    }

    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);

    return response.data;
  } catch (error) {
    console.error('Login error in loginUser:', error);
    throw error?.response?.data || { error: 'Login failed' };
  }
}
