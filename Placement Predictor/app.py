from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get inputs
        cgpa = float(request.form["cgpa"])
        iq = float(request.form["iq"])
        
        # Prepare and scale input
        input_features = np.array([[cgpa, iq]])
        input_scaled = scaler.transform(input_features)
        
        # Predict
        result = model.predict(input_scaled)[0]
        outcome = "Placed" if result == 1 else "Not Placed"
        
        return render_template("index.html", prediction_text=f"Prediction: {outcome}")
    except:
        return render_template("index.html", prediction_text="Invalid input. Please try again.")

if __name__ == "__main__":
    app.run(debug=True)
