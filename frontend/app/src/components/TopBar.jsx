import React from 'react';
import PrimaryButton from './PrimaryButton';
import '../styles/TopBar.css';

const TopBar = ({ toggleSidebar, isSidebarCollapsed, currentSection, userEmail, onLogout }) => {
  return (
    <div className="top-bar">
      <div className="left-section">
        <button className="menu-toggle-btn" onClick={toggleSidebar}>
          {isSidebarCollapsed ? '☰' : '←'}
        </button>
        <h3 className="section-title">{currentSection}</h3>
      </div>
      <div className="right-section">
        <span className="user-email">{userEmail}</span>
        <PrimaryButton onClick={onLogout} className="logout-btn">Logout</PrimaryButton>
      </div>
    </div>
  );
};

export default TopBar;
