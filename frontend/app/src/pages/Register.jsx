import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth/register";
import FormInput from "../components/FormInput";
import FormWrapper from "../components/FormWrapper";
import PrimaryButton from '../components/PrimaryButton';
import "../styles/globals.css";

const Register = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username || !email || !password) {
      setError("Please enter all fields.");
      return;
    }

    if (!/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/.test(email)) {
      setError("Please enter a valid email.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    try {
      setLoading(true);
      await registerUser({ username, email, password });
      setLoading(false);
      navigate("/login");
    } catch (err) {
      setLoading(false);
      setError(err.error || "Something went wrong, please try again.");
    }
  };

  return (
    <FormWrapper title="Register" error={error} onSubmit={handleSubmit}>
      <FormInput
        label="Username:"
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter your username"
      />
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
      <PrimaryButton type="submit" disabled={loading}>
        {loading ? "Registering..." : "Register"}
      </PrimaryButton>
    </FormWrapper>
  );
};

export default Register;
