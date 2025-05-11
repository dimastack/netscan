import api from '../../services/client';

export const checkSsl = async (url) => {
  const response = await api.get('/web/sslcheck', {
    params: { url },
  });
  return response.data;
};
