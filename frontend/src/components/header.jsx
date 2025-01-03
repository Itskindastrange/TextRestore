import React from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom

export const Header = (props) => {
  return (
    <header id="header">
      <div className="intro">
        <div className="overlay">
          <div className="container">
            <div className="row">
              <div className="col-md-8 col-md-offset-2 intro-text">
                <h1>
                  {props.data ? props.data.title : "Loading"}
                  <span></span>
                </h1>
                <p>{props.data ? props.data.paragraph : "Loading"}</p>
                {/* Use Link component to navigate to the login page */}
                <Link to="/login" className="btn btn-custom btn-lg page-scroll">
                  Login
                </Link>
                <Link to="/SignUp" className="btn btn-custom btn-lg page-scroll">
                  Sign Up
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
