import api from '../../services/client';

export const pingHost = async (ip) => {
  const response = await api.get('/scan/ping', {
    params: { ip },
  });
  return response.data;
};
