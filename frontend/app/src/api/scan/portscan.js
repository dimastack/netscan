import api from '../../services/client';

export const scanPorts = async (ip) => {
  const response = await api.get('/scan/portscan', {
    params: { ip },
  });
  return response.data;
};
