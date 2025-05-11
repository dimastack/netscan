import api from '../../services/client';

export const getOsFingerprint = async (ip) => {
  const response = await api.get('/scan/osfingerprint', {
    params: { ip },
  });
  return response.data;
};
