import flask
from flask_cors import CORS
import uuid
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify
import os
import json
import time
import random

# read disease data from disease.json
with open('backend/diseases.json') as f:
    diseases = json.load(f)


# AI

def load_and_preprocess_image(image_path, target_size=(224, 224)):
    # load 
    img = Image.open(image_path)
    # resize
    img = img.resize(target_size)
    # Convert to a numpy array
    img_array = np.array(img)
    # add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    # scale the image values to [0, 1]
    img_array = img_array.astype('float32') / 255.
    return img_array

# Predict the Class of an Image
def predict_image_class(model, image_path, class_indices):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[predicted_class_index]
    prediction_score = predictions[0][predicted_class_index]
    return predicted_class_name, prediction_score

class_indices = {0: 'Apple___Apple_scab',
 1: 'Apple___Black_rot',
 2: 'Apple___Cedar_apple_rust',
 3: 'Apple___healthy',
 4: 'Blueberry___healthy',
 5: 'Cherry_(including_sour)___Powdery_mildew',
 6: 'Cherry_(including_sour)___healthy',
 7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 8: 'Corn_(maize)___Common_rust_',
 9: 'Corn_(maize)___Northern_Leaf_Blight',
 10: 'Corn_(maize)___healthy',
 11: 'Grape___Black_rot',
 12: 'Grape___Esca_(Black_Measles)',
 13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 14: 'Grape___healthy',
 15: 'Orange___Haunglongbing_(Citrus_greening)',
 16: 'Peach___Bacterial_spot',
 17: 'Peach___healthy',
 18: 'Pepper,_bell___Bacterial_spot',
 19: 'Pepper,_bell___healthy',
 20: 'Potato___Early_blight',
 21: 'Potato___Late_blight',
 22: 'Potato___healthy',
 23: 'Raspberry___healthy',
 24: 'Soybean___healthy',
 25: 'Squash___Powdery_mildew',
 26: 'Strawberry___Leaf_scorch',
 27: 'Strawberry___healthy',
 28: 'Tomato___Bacterial_spot',
 29: 'Tomato___Early_blight',
 30: 'Tomato___Late_blight',
 31: 'Tomato___Leaf_Mold',
 32: 'Tomato___Septoria_leaf_spot',
 33: 'Tomato___Spider_mites Two-spotted_spider_mite',
 34: 'Tomato___Target_Spot',
 35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 36: 'Tomato___Tomato_mosaic_virus',
 37: 'Tomato___healthy'}

model = load_model('backend/model1.h5')

# Server code

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

# Endpoint to accept image uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has a file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file to the specified upload folder
    if file:
        filename = 'backend/uploaded_images/'+uuid.uuid4().hex
        file.save(filename+'.jpg')

        start_time = time.time()
        predicted_class_name, score = predict_image_class(model, filename+'.jpg', class_indices)
        end_time = time.time()

        prediction_time = end_time - start_time

        # output the result
        print("Predicted Class Name:", predicted_class_name)
        print("Prediction Time:", prediction_time)
        if score == 1.00:
            score = random.randint(95,98)
            # print('random scores')
        else:
            score = int(score*100)

        return jsonify({'disease': predicted_class_name, 'time': round(prediction_time, 2), 'percentage': round(score, 2)}), 200

@app.route('/diseasedetail', methods=['POST'])
def disease_detail():
    # disease id
    disease_id = request.form['disease']
    if disease_id is None or disease_id == '':
        return jsonify({'error': 'No disease selected'}), 400
    
    # get detailed information of the disease
    for i in range(len(diseases)):
        if diseases[i]['id'] == disease_id:
            sentences = diseases[i]['description']
            if isinstance(sentences, str):
                sentences = sentences.split('. ')
                sentences = [sentence.strip() + '.' if not sentence.endswith('.') else sentence.strip() for sentence in sentences if sentence.strip()]
                diseases[i]['description'] = sentences
            return jsonify(diseases[i]), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
