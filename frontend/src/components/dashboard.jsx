import React, { useState } from "react";
import { Footer } from "./footer";
import axios from "axios";

export const Dashboard = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [lowResImage, setLowResImage] = useState(null);
  const [highResImage, setHighResImage] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setErrorMessage("");
    setSuccessMessage("");

    if (event.target.files[0]) {
      setLowResImage(URL.createObjectURL(event.target.files[0]));
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setErrorMessage("Please select a file before uploading.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", selectedFile);
  
    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      if (response.data.restored_image) {
        // Correctly construct the image URL relative to the backend
        const restoredImageUrl = `${response.data.restored_image}?t=${Date.now()}`;
        setHighResImage(restoredImageUrl); // Update state
        console.log("High-Res Image URL:", restoredImageUrl); // Log for debugging
        setErrorMessage("");
        setSuccessMessage("Image restored successfully!");
      } else {
        setErrorMessage("Failed to restore the image.");
      }
    } catch (error) {
      setErrorMessage("An error occurred during the upload process.");
      console.error(error);
    }
  };
  
  

  const handleSaveImage = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/save", { image: highResImage });
      if (response.status === 200) {
        setSuccessMessage("Image saved successfully!");
      } else {
        setErrorMessage("Failed to save the image.");
      }
    } catch (error) {
      setErrorMessage("An error occurred while saving the image.");
      console.error(error);
    }
  };

  return (
    <div id="dashboard" className="text-center">
      <div className="container">
        <div className="section-title">
          <h2>Dashboard</h2>
        </div>

        <div className="row">
          <div className="images-container">
            <div className="col-md-6">
              <h3>Low-Resolution:</h3>
              {lowResImage ? (
                <img src={lowResImage} className="img-responsive" alt="Low-Resolution Preview" />
              ) : (
                <p>No image selected</p>
              )}
            </div>

            <div className="col-md-6">
              <h3>High-Resolution:</h3>
              {highResImage ? (
                <img src={highResImage} className="img-responsive" alt="Restored Image" />
              ) : (
                <p>Restored image will appear here after upload.</p>
              )}
            </div>
          </div>
        </div>

        <div className="button-container">
          <div className="upload-section">
            <input type="file" accept=".jpeg,.jpg,.png" onChange={handleFileChange} />
            <button className="btn btn-custom" onClick={handleFileUpload}>
              Upload
            </button>
          </div>

          <button
            className="btn btn-custom"
            disabled={!highResImage}
            onClick={() => {
              const link = document.createElement("a");
              link.href = highResImage;
              console.log(highResImage)
              link.download = "restored_image.png";
              link.click();
            }}
          >
            Download
          </button>
          <button className="btn btn-custom" disabled={!highResImage} onClick={handleSaveImage}>
            Save
          </button>
        </div>

        {errorMessage && <p className="error-message text-danger">{errorMessage}</p>}
        {successMessage && <p className="success-message text-success">{successMessage}</p>}
      </div>
      <Footer />
    </div>
  );
};
