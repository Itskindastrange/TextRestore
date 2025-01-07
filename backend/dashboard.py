from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from tensorflow.keras import layers, models

# Flask app setup
app = Flask(__name__)
CORS(app)

# Directories for saving files
UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Configure upload folder

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_srcnn_model(input_shape=(None, None, 1)):
    model = models.Sequential()
    model.add(layers.Conv2D(64, (9, 9), activation='relu', padding='same', input_shape=input_shape))
    model.add(layers.Conv2D(32, (1, 1), activation='relu', padding='same'))
    model.add(layers.Conv2D(1, (5, 5), activation='linear', padding='same'))
    return model

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        result = process_image(file_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500

@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def process_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Invalid image or file not found"}
        
        input_image = preprocess_image(image)

        model_path = os.path.join(MODEL_FOLDER, 'model.h5')
        weights_path = os.path.join(MODEL_FOLDER, 'model.h5')

        model = create_srcnn_model(input_shape=(256, 256, 1))
        model.load_weights(weights_path)

        restored_image = model.predict(np.expand_dims(input_image, axis=0))[0]
        restored_image = postprocess_image(restored_image)

        output_filename = 'restored_' + os.path.basename(image_path)
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        cv2.imwrite(output_path, restored_image)

        restored_image_url = url_for('serve_file', filename=output_filename, _external=True)
        return {"message": "Image processed successfully", "restored_image": restored_image_url}
    except Exception as e:
        return {"error": f"Error processing image: {str(e)}"}

def preprocess_image(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_resized = cv2.resize(image_gray, (256, 256))
    image_normalized = image_resized / 255.0
    return np.expand_dims(image_normalized, axis=-1)

def postprocess_image(image):
    image = np.clip(image * 255.0, 0, 255).astype(np.uint8)
    return image

if __name__ == '__main__':
    app.run(debug=True)
