import api from '../../services/client';

export const lookupDomain = async (domain) => {
  const response = await api.get(`/dns/lookup`, {
    params: { domain },
  });
  return response.data;
};
