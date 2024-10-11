import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navigation } from "./components/navigation"; // Navbar
import { Header } from "./components/header"; // Landing page Header
import { Features } from "./components/features"; // Landing page Features section
import { About } from "./components/about"; // Landing page About section
// Landing page Services section
import { Contact } from "./components/contact"; // Footer
import { Login } from "./components/login"; // Login page
import { SignUp } from "./components/SignUp"; // Sign Up page
import { Dashboard } from "./components/dashboard"; // Dashboard page
import JsonData from "./data/data.json";
import SmoothScroll from "smooth-scroll";
import "./App.css";

// Smooth scroll setup
export const scroll = new SmoothScroll('a[href*="#"]', {
  speed: 1000,
  speedAsDuration: true,
});

const App = () => {
  const [landingPageData, setLandingPageData] = useState({});

  useEffect(() => {
    setLandingPageData(JsonData);
  }, []);

  return (
    <Router>
      {/* Common Navigation for all routes */}
      <Navigation />

      <Routes>
        {/* Main Landing Page Route */}
        <Route
          path="/"
          element={
            <div>
              <Header data={landingPageData.Header} />
              <Features data={landingPageData.Features} />
              
              <About data={landingPageData.About} />
              <Contact data={landingPageData.Contact} />
            </div>
          }
        />

        {/* Login Page Route */}
        <Route
          path="/login"
          element={
           
              <Login />
              
          }
        />

        {/* Sign Up Page Route */}
        <Route path="/signup" element={<SignUp />} />

        {/* Dashboard Page Route */}
        <Route
          path="/dashboard"
          element={
           
              <Dashboard />
              
           
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
