import api from '../../services/client';

export async function fetchCurrentUser() {
  try {
    const response = await api.get('/auth/me');
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch user' };
  }
}
