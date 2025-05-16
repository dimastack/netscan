import api from '../../services/client';


/**
 * TCP SYN Scan - specific ports
 * @param {string} ip - Target IP address
 * @param {string} ports - Comma-separated ports, e.g., "22,80,443"
 */
export const synScan = async ({ ip, ports = '22,80,443' }) => {
  const response = await api.get('/scan/synscan', {
    params: { ip, ports },
  });
  return response.data;
};

/**
 * TCP Connect Scan - single port
 * @param {string} ip - Target IP address
 * @param {number} port - Port to scan
 * @param {number} timeout - Socket timeout in seconds
 */
export const tcpConnectScan = async ({ ip, port, timeout = 2 }) => {
  const response = await api.get('/scan/tcpconnect', {
    params: { ip, port, timeout },
  });
  return response.data;
};

/**
 * UDP Scan - single port
 * @param {string} ip - Target IP address
 * @param {string} ports - Comma-separated ports, e.g., "22,80,443"
 */
export const udpScan = async ({ ip, ports = '22,80,443' }) => {
  const response = await api.get('/scan/udp', {
    params: { ip, ports },
  });
  return response.data;
};

/**
 * Port Range Scan - TCP SYN scan across a range
 * @param {string} ip - Target IP address
 * @param {string} range - Port range, e.g., "1-1024"
 */
export const scanPorts = async ({ ip, range = '1-1024' }) => {
  const response = await api.get('/scan/portscan', {
    params: { ip, range },
  });
  return response.data;
};
