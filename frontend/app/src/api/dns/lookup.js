import api from '../../services/client';

export const lookupDomain = async ({ domain, type = 'A', dst = '8.8.8.8', timeout = 2 }) => {
  const response = await api.get(`/dns/lookup`, {
    params: { domain, type, dst, timeout },
  });
  return response.data;
};
