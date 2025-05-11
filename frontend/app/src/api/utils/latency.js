import api from '../../services/client';

export const getLatency = async (url) => {
  const response = await api.get('/utils/latency', {
    params: { url },
  });
  return response.data;
};
