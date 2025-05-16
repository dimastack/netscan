import React, { useState } from 'react';
import DynamicForm from './DynamicForm';
import '../styles/FeatureSection.css';

const FeatureSection = ({ label, inputs, apiCall }) => {
  const [open, setOpen] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (formData) => {
    const response = await apiCall(formData);
    setResult(response);
  };

  return (
    <div className="feature-section">
      <button className="dropdown-toggle" onClick={() => setOpen(!open)}>
        <span className="label">{label}</span>
        <span className="arrow">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="feature-content">
          <DynamicForm inputs={inputs} onSubmit={handleSubmit} />
          {result && <pre className="api-result">{JSON.stringify(result, null, 2)}</pre>}
        </div>
      )}
    </div>
  );
};

export default FeatureSection;
