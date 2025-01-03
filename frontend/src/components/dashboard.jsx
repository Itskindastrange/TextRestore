import React from "react";
import { Footer } from "./footer";

export const Dashboard = (props) => {
  return (
    <div id="dashboard" className="text-center">
      <div className="container">
        <div className="section-title">
          <h2>Dashboard</h2>
          
        </div>

        <div className="row">
          {/* Only showing 2 images side by side */}
          {
            
            <div className="images-container">
                
              <div className="col-md-6">
              <h3>Low-Resoluion:</h3>
                  <img src="img/input.jpg" className="img-responsive" alt="" />{" "}
               
              </div>
              <div className="col-md-4">
              <h3>High-Resoluion:</h3>
                <img
                 src="img/restored.jpg" className="img-responsive" alt="" />{" "}
              </div>
            </div>
          
           }
        </div>

        <div className="button-container">
          <button className="btn btn-custom">Download</button>
          <button className="btn btn-custom">Save</button>
        </div>
      </div>
      <Footer />
    </div>
  );
};
