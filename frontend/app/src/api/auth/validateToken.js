import api from '../../services/client';

/**
 * Validates the stored JWT token by making a request to the backend API.
 * 
 * This function checks whether the user's session token is still valid.
 * If the token is invalid or expired, the caller should handle logout or redirection.
 * 
 * @returns {Promise<Object>} The response data containing validation status.
 * @throws {Object} An error object if the token is invalid or the request fails.
 */
export async function validateToken() {
  try {
    const response = await api.get('/auth/validate-token');
    return response.data;
  } catch (error) {
    console.error("Token validation error:", error.response || error);
    throw error.response?.data || { error: 'Token validation failed' };
  }
}
