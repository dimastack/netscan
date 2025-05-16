import api from '../../services/client';

export const getLatency = async ({ host, port = 80 }) => {
  const response = await api.get('/utils/latency', {
    params: { host, port },
  });
  return response.data;
};
