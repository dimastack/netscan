import api from '../../services/client';

export const checkSsl = async ({ url, timeout = 5 }) => {
  const response = await api.get('/web/sslcheck', {
    params: { url, timeout },
  });
  return response.data;
};
