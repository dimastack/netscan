import api from '../../services/client';

export const reverseDns = async (ip) => {
  const response = await api.get(`/dns/reverse`, {
    params: { ip },
  });
  return response.data;
};
