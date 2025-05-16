import React from 'react';
import AppRouter from './router';
import { AuthProvider } from './context/AuthContext';

const App = () => {
  return (
    <div className="App">
      <AuthProvider>
        <AppRouter />
      </AuthProvider>
    </div>
  );
};

export default App;
