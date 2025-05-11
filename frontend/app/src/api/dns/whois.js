import api from '../../services/client';

export const whoisLookup = async (domain) => {
  const response = await api.get(`/dns/whois`, {
    params: { domain },
  });
  return response.data;
};
