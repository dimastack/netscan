import api from '../../services/client';

export const checkHttp = async (url) => {
  const response = await api.get('/web/httpcheck', {
    params: { url },
  });
  return response.data;
};
