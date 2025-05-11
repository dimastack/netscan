import React from 'react';
import { useNavigate } from 'react-router-dom';
import PrimaryButton from '../components/PrimaryButton';
import '../styles/globals.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <p>Welcome! You are successfully logged in.</p>
      <PrimaryButton onClick={handleLogout} style={{ marginTop: '1rem' }}>Logout</PrimaryButton>
    </div>
  );
};

export default Dashboard;
