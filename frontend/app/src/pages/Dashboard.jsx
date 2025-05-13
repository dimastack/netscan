import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import FeatureSection from '../components/FeatureSection';
import { lookupDomain } from '../api/dns/lookup';
import { reverseDns } from '../api/dns/reverse';
import { whoisLookup } from '../api/dns/whois';
import { getBanner } from '../api/scan/banner';
import { getOsFingerprint } from '../api/scan/osfingerprint';
import { pingHost } from '../api/scan/ping';
import { scanPorts } from '../api/scan/portscan';
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
    { label: 'Reverse DNS', inputs: [{ name: 'ip', label: 'IP Address' }], apiCall: reverseDns },
    { label: 'WHOIS', inputs: [{ name: 'domain', label: 'Domain' }], apiCall: whoisLookup }
  ],
  scan: [
    { label: 'Banner Grabbing', inputs: [{ name: 'host', label: 'Host' }, { name: 'port', label: 'Port' }], apiCall: getBanner },
    { label: 'OS Fingerprint', inputs: [{ name: 'host', label: 'Host' }], apiCall: getOsFingerprint },
    { label: 'Ping', inputs: [{ name: 'host', label: 'Host' }], apiCall: pingHost },
    { label: 'Port Scan', inputs: [{ name: 'host', label: 'Host' }, { name: 'ports', label: 'Ports' }], apiCall: scanPorts },
    { label: 'Traceroute', inputs: [{ name: 'host', label: 'Host' }], apiCall: tracerouteHost }
  ],
  utils: [
    { label: 'Headers', inputs: [{ name: 'url', label: 'URL' }], apiCall: getHeaders },
    { label: 'Latency', inputs: [{ name: 'host', label: 'Host' }], apiCall: getLatency },
    { label: 'Resolve', inputs: [{ name: 'hostname', label: 'Hostname' }], apiCall: resolveDomain },
    { label: 'Reverse Lookup', inputs: [{ name: 'ip', label: 'IP Address' }], apiCall: reverseIp }
  ],
  web: [
    { label: 'HTTP Check', inputs: [{ name: 'url', label: 'URL' }], apiCall: checkHttp },
    { label: 'SSL Check', inputs: [{ name: 'url', label: 'URL' }], apiCall: checkSsl }
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
