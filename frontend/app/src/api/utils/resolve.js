import api from '../../services/client';

export const resolveDomain = async ({ host }) => {
  const response = await api.get('/utils/resolve', {
    params: { host },
  });
  return response.data;
};
