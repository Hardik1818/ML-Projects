from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Load the model and scaler
model = pickle.load(open('heart_disease_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        age = float(request.form['age'])
        cp = float(request.form['cp'])
        thalach = float(request.form['thalach'])
        exang = float(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        ca = float(request.form['ca'])
        thal = float(request.form['thal'])
        
        # Create feature array
        features = np.array([[age, cp, thalach, exang, oldpeak, ca, thal]])
        
        # Scale features
        scaled_features = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(scaled_features)
        
        # Get prediction probability
        probability = model.predict_proba(scaled_features)[0][1]
        
        # Prepare result
        result = {
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'interpretation': 'High risk of heart disease' if prediction[0] == 1 else 'Low risk of heart disease'
        }
        
        return render_template('index.html', result=result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)