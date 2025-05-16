import api from '../../services/client';

export const pingHost = async ({ ip, timeout = 3 }) => {
  const response = await api.get('/scan/ping', {
    params: { ip, timeout },
  });
  return response.data;
};
