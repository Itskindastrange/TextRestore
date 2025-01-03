import React, { useState } from "react";
import { Footer } from "./footer";

export const SignUp = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle signup logic here (e.g., calling an API)
    console.log("Sign Up Data:", formData);
  };
  const handleLogin = () => {
    
  };
  return (
    <div id="signup" className="colorcust text-center" style={{ padding: "50px 0" }}>
      <div className="container">
        <div className="section-title">
          <h2>Sign Up</h2>
          <p>Please fill in the form to create an account.</p>
        </div>
        <div className="row justify-content-center">
          <div className="formdiv col-md-12 ">
            <form onSubmit={handleSubmit} className="text-center col-md-6 ">
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
                <label htmlFor="email">Email:</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  name="email"
                  value={formData.email}
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
                Sign Up
              </button>
              <button type="button" className="btn btn-info" onClick={handleLogin}>
                Login
              </button>
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};
