import api from '../../services/client';

export const getBanner = async (ip, port) => {
  const response = await api.get('/scan/banner', {
    params: { ip, port },
  });
  return response.data;
};
