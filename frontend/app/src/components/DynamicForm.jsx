import React, { useState, useEffect } from 'react';
import PrimaryButton from './PrimaryButton';


const DynamicForm = ({ inputs, onSubmit }) => {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    // Set default values if provided
    const initialFormData = {};
    inputs.forEach(({ name, defaultValue }) => {
      if (defaultValue !== undefined) {
        initialFormData[name] = defaultValue;
      }
    });
    setFormData(initialFormData);
  }, [inputs]);

  const handleChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="dynamic-form">
      {inputs.map(({ name, label, type = 'text', options = [], defaultValue }) => (
        <div key={name} className="form-group">
          <label>{label}</label>
          {type === 'select' ? (
            <select
              value={formData[name] || defaultValue || ''}
              onChange={(e) => handleChange(name, e.target.value)}
              required
            >
              {options.map(opt => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          ) : (
            <input
              type={type}
              value={formData[name] || ''}
              onChange={(e) => handleChange(name, e.target.value)}
              required
            />
          )}
        </div>
      ))}
      <PrimaryButton type="submit">Run</PrimaryButton>
    </form>
  );
};

export default DynamicForm;
