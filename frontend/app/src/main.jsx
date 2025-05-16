import React, { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/globals.css'
import App from './App.jsx'

// To remove 2 calls of api/v1/auth/validate-token in a row StrictMode should be removed
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
