import api from '../../services/client';

export const resolveDomain = async (domain) => {
  const response = await api.get('/utils/resolve', {
    params: { domain },
  });
  return response.data;
};
