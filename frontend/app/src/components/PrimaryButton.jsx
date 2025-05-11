import React from 'react';

const PrimaryButton = ({ children, type = 'button', onClick, disabled = false, style = {} }) => (
  <button
    type={type}
    onClick={onClick}
    disabled={disabled}
    className="primary-button"
    style={style}
  >
    {children}
  </button>
);

export default PrimaryButton;
