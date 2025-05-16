import api from '../../services/client';

export const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) throw new Error('No refresh token');

  const response = await api.post('/auth/refresh', null, {
    headers: {
      Authorization: `Bearer ${refreshToken}`
    }
  });

  const { access_token } = response.data;
  localStorage.setItem('accessToken', access_token);
  return access_token;
};
