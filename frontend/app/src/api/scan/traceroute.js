import api from '../../services/client';

export const tracerouteHost = async ({ ip }) => {
  const response = await api.get('/scan/traceroute', {
    params: { ip },
  });
  return response.data;
};
