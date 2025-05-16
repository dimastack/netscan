import api from '../../services/client';

export const getOsFingerprint = async ({ ip, ports = '22,80,443,8000,8080', timeout = 2 }) => {
  const response = await api.get('/scan/osfingerprint', {
    params: { ip, ports, timeout },
  });
  return response.data;
};
