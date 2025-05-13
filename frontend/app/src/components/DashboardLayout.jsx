import React from 'react';
import TopBar from './TopBar';
import SideBar from './SideBar';
import '../styles/DashboardLayout.css';

const DashboardLayout = ({ children, isSidebarCollapsed, ...props }) => {
  return (
    <div className={`dashboard-layout ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      <TopBar {...props} />
      <div className="dashboard-body" style={{ marginTop: '60px' }}>
        <SideBar isCollapsed={isSidebarCollapsed} {...props} />
        <main className="dashboard-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
