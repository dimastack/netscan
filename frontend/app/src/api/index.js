import api from '../services/client';

export const getApiStatus = async () => {
  const response = await api.get('/');
  return response.data;
};
