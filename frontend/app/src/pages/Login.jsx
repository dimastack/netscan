import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/auth/login';
import { useAuthContext } from '../context/AuthContext';
import FormInput from '../components/FormInput';
import FormWrapper from '../components/FormWrapper';
import PrimaryButton from '../components/PrimaryButton';
import "../styles/globals.css";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuthContext();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Please enter both email and password.');
      return;
    }

    try {
      await loginUser({ email, password });
      localStorage.setItem('userEmail', email);

      login();
      navigate('/dashboard');
    } catch (err) {
      setError(err.error || 'Something went wrong, please try again.');
    }
  };

  const goToRegister = () => navigate('/register');

  return (
    <FormWrapper title="Login" error={error} onSubmit={handleSubmit}>
      <FormInput
        label="Email:"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      <FormInput
        label="Password:"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter your password"
      />
      <PrimaryButton type="submit">Login</PrimaryButton>
      <PrimaryButton onClick={goToRegister} style={{ marginTop: '1rem' }}>Register</PrimaryButton>
    </FormWrapper>
  );
};

export default Login;
