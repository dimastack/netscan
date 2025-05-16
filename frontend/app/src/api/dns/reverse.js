import api from '../../services/client';

export const reverseDns = async ({ ip, dst = '8.8.8.8', timeout = 2 }) => {
  const response = await api.get(`/dns/reverse`, {
    params: { ip, dst, timeout },
  });
  return response.data;
};
