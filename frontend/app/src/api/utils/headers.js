import api from '../../services/client';

export const getHeaders = async ({ url }) => {
  const response = await api.get('/utils/headers', {
    params: { url },
  });
  return response.data;
};
