import api from '../../services/client';

export const getBanner = async ({ ip, port, timeout = 2 }) => {
  const response = await api.get('/scan/bannergrab', {
    params: { ip, port, timeout },
  });
  return response.data;
};
