import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import FeatureSection from '../components/FeatureSection';
import { lookupDomain } from '../api/dns/lookup';
import { reverseDns } from '../api/dns/reverse';
import { whoisLookup } from '../api/dns/whois';
import { getBanner } from '../api/scan/banner';
import { getOsFingerprint } from '../api/scan/osfingerprint';
import { pingHost } from '../api/scan/ping';
import { synScan, tcpConnectScan, udpScan, scanPorts } from '../api/scan/portscan';
import { tracerouteHost } from '../api/scan/traceroute';
import { getHeaders } from '../api/utils/headers';
import { getLatency } from '../api/utils/latency';
import { resolveDomain } from '../api/utils/resolve';
import { reverseIp } from '../api/utils/reverse';
import { checkHttp } from '../api/web/httpcheck';
import { checkSsl } from '../api/web/sslcheck';
import '../styles/globals.css';

const apiFeatures = {
  dns: [
    {
      label: 'DNS Lookup',
      inputs: [
        { name: 'domain', label: 'Domain' },
        {
          name: 'type',
          label: 'Type',
          type: 'select',
          options: ['A', 'AAAA', 'MX', 'CNAME', 'TXT'],
          defaultValue: 'A'
        },
        { name: 'dst', label: 'DNS Server', defaultValue: '8.8.8.8' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '2' }
      ],
      apiCall: lookupDomain
    },
    { 
      label: 'Reverse DNS', 
      inputs: [
        { name: 'ip', label: 'IP Address' },
        { name: 'dst', label: 'DNS Server', defaultValue: '8.8.8.8' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '2' }
      ], 
      apiCall: reverseDns 
    },
    { label: 'WHOIS', inputs: [{ name: 'domain', label: 'Domain' }], apiCall: whoisLookup }
  ],
  scan: [
    { 
      label: 'Banner Grabbing', 
      inputs: [
        { name: 'ip', label: 'IP Address' }, 
        { name: 'port', label: 'Port' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '2' }
      ], 
      apiCall: getBanner 
    },
    { 
      label: 'OS Fingerprint', 
      inputs: [
        { name: 'ip', label: 'IP Address' },
        { name: 'ports', label: 'Ports' , defaultValue: '22,80,443,8000,8080' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '2' }
      ], 
      apiCall: getOsFingerprint 
    },
    { 
      label: 'Ping', 
      inputs: [
        { name: 'ip', label: 'IP Address' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '3' }
      ], 
      apiCall: pingHost 
    },
    { 
      label: 'TCP SYN Scan',
      inputs: [
        { name: 'ip', label: 'IP Address' }, 
        { name: 'ports', label: 'Ports' , defaultValue: '22,80,443' }
      ], 
      apiCall: synScan 
    },
    { 
      label: 'TCP Connect Scan',
      inputs: [
        { name: 'ip', label: 'IP Address' }, 
        { name: 'port', label: 'Port' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '2' }
      ], 
      apiCall: tcpConnectScan 
    },
    { 
      label: 'UDP Scan',
      inputs: [
        { name: 'ip', label: 'IP Address' }, 
        { name: 'ports', label: 'Ports' , defaultValue: '22,80,443' }
      ], 
      apiCall: udpScan 
    },
    { 
      label: 'Port Scan',
      inputs: [
        { name: 'ip', label: 'IP Address' }, 
        { name: 'range', label: 'Ports range', defaultValue: '1-1024' }
      ], 
      apiCall: scanPorts 
    },
    { label: 'Traceroute', inputs: [{ name: 'ip', label: 'IP Address' }], apiCall: tracerouteHost }
  ],
  utils: [
    { label: 'Headers', inputs: [{ name: 'url', label: 'URL' }], apiCall: getHeaders },
    { label: 'Latency', 
      inputs: [
        { name: 'host', label: 'Hostname' },
        { name: 'port', label: 'Port', defaultValue: '80' }
      ], 
      apiCall: getLatency 
    },
    { label: 'Resolve', inputs: [{ name: 'host', label: 'Hostname' }], apiCall: resolveDomain },
    { label: 'Reverse Lookup', inputs: [{ name: 'ip', label: 'IP Address' }], apiCall: reverseIp }
  ],
  web: [
    { 
      label: 'HTTP Check', 
      inputs: [
        { name: 'url', label: 'URL' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '5' }
      ], 
      apiCall: checkHttp 
    },
    { label: 'SSL Check', 
      inputs: [
        { name: 'url', label: 'URL' },
        { name: 'timeout', label: 'Timeout (seconds)', type: 'number', defaultValue: '5' }
      ], 
      apiCall: checkSsl }
  ]
};

const Dashboard = () => {
  const [collapsed, setCollapsed] = useState(true);
  const [activeSection, setActiveSection] = useState('dns');
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    const email = localStorage.getItem('userEmail');
    if (email) {
      setUserEmail(email);
    } else {
      // Redirect to login if no email found
      window.location.href = '/login';
    }
  }, []);

  const toggleSidebar = () => setCollapsed(prev => !prev);
  const handleLogout = () => {
    localStorage.removeItem('userEmail');
    window.location.href = '/login';
  };

  return (
    <DashboardLayout
      toggleSidebar={toggleSidebar}
      collapsed={collapsed}
      activeSection={activeSection}
      onSelectSection={setActiveSection}
      currentSection={activeSection.toUpperCase()}
      userEmail={userEmail}
      onLogout={handleLogout}
    >
      {apiFeatures[activeSection]?.map((feature, idx) => (
        <FeatureSection key={idx} {...feature} />
      ))}
    </DashboardLayout>
  );
};

export default Dashboard;
