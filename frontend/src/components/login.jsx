import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import { Footer } from "./footer";
export const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const navigate = useNavigate(); // Hook for navigation

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login logic here (e.g., calling an API)
    console.log("Login Data:", formData);
  };

  // Function to navigate to the Sign Up page
  const handleSignUp = () => {
    navigate("/signup"); // Navigate to the signup page
  };

  return (
    <div id="login" className="colorcust text-center" style={{ padding: "50px 0" }}>
      <div className="container">
        <div className="section-title">
          <h2>Login</h2>
          <p>Please enter your credentials to login.</p>
        </div>
        <div className="row justify-content-center">
          <div className="formdiv col-md-12">
            <form onSubmit={handleSubmit} className="text-center">
              <div className="form-group">
                <label htmlFor="username">Username:</label>
                <input
                  type="text"
                  className="form-control"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password:</label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary" style={{ margin: "10px" }}>
                Login
              </button>
              <br />
              <button type="button" className="btn btn-info" onClick={handleSignUp}>
                Sign Up
              </button>
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};
