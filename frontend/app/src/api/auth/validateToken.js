import api from '../../services/client';

/**
 * Validates the stored JWT access token by making a request to the backend.
 * 
 * This function is used to verify whether the current user's session is still valid.
 * It sends the token via the Authorization header. If the token is expired or invalid,
 * it should be refreshed or the user should be logged out.
 *
 * @returns {Promise<boolean>} Returns true if token is valid, otherwise throws an error.
 * @throws {Object} Error data if the token is invalid or the request fails.
 */
export async function validateToken() {
  const accessToken = localStorage.getItem('accessToken');
  if (!accessToken) {
    throw { error: 'Access token not found' };
  }

  try {
    const response = await api.get('/auth/validate-token', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.data?.valid === true;
  } catch (error) {
    console.error('Token validation error:', error.response || error);
    throw error.response?.data || { error: 'Token validation failed' };
  }
}
