import api from '../../services/client';

export const checkHttp = async ({ url, timeout = 5 }) => {
  const response = await api.get('/web/httpcheck', {
    params: { url, timeout },
  });
  return response.data;
};
