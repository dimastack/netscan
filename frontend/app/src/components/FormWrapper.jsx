import React from 'react';

const FormWrapper = ({ title, error, onSubmit, children }) => (
  <div className={`${title.toLowerCase()}-form`}>
    <h2>{title}</h2>
    {error && <p className="error">{error}</p>}
    <form onSubmit={onSubmit}>
      {children}
    </form>
  </div>
);

export default FormWrapper;
