import api from '../../services/client';

export const reverseIp = async (ip) => {
  const response = await api.get('/utils/reverse', {
    params: { ip },
  });
  return response.data;
};
