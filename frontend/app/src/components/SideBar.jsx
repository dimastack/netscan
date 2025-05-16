import React from 'react';
import '../styles/SideBar.css';

const sections = [
  { id: 'dns', icon: '🌐', label: 'DNS' },
  { id: 'scan', icon: '🛠️', label: 'Scan' },
  { id: 'utils', icon: '⚙️', label: 'Utils' },
  { id: 'web', icon: '🕸️', label: 'Web' }
];

const SideBar = ({ collapsed, activeSection, onSelectSection }) => {
  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`} style={{ zIndex: 998 }}>
      {sections.map(({ id, icon, label }) => (
        <div
          key={id}
          className={`menu-item ${activeSection === id ? 'active' : ''}`}
          onClick={() => onSelectSection(id)}
        >
          <span className="menu-icon">{icon}</span>
          {!collapsed && <span className="menu-label">{label}</span>}
        </div>
      ))}
    </div>
  );
};

export default SideBar;
