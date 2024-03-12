# Import libraries
import re
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect
import pickle

app = Flask(__name__)

# Load the model
all_models = pickle.load(open('models.pkl', 'rb'))
# Import the len function from the builtins module
from builtins import len

# Update the Flask app configuration to add the len function as a global function in the Jinja2 environment
app.jinja_env.globals['len'] = len


@app.route('/', methods=['GET', 'POST'])
def hey():
    return render_template("signin.html")

@app.route('/index', methods=['GET', 'POST'])
def hello():
    return render_template("index.html")

@app.route('/heart', methods=['GET', 'POST'])
def heart():
    return render_template("heart.html")

@app.route('/chatu', methods=['GET', 'POST'])
def chatu():
    return render_template('chatu.html')

@app.route('/api', methods=['POST'])
def predict():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    fgender = request.form['gender']
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    chol = request.form['chol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang']
    oldpeak = request.form['oldpeak']
    slope = request.form['slope']
    ca = request.form['ca']
    thal = request.form['thal']

    # Convert empty values to default values
    if not trestbps:
        trestbps = 95
    if not chol:
        chol = 150
    if not thalach:
        thalach = 72
    if not oldpeak:
        oldpeak = 2

    # Convert 'thal' string to integer based on mapping
    thal_map = {'Normal': 0, 'Fixed Defect': 1, 'Reversible Defect': 2}
    thal = thal_map.get(thal, -1)  # Default to -1 if thal value is not found in the mapping

    # Convert 'restecg' string to integer based on mapping
    restecg_map = {'Normal': 0, 'STT Abnormality': 1, 'IV Hypertrophy': 2}
    restecg = restecg_map.get(restecg, -1)  # Default to -1 if restecg value is not found in the mapping

    features = [int(age), 1 if fgender == "Male" else 0, int(cp), int(trestbps), int(chol), int(fbs),
                int(restecg), int(thalach), int(exang), int(oldpeak), int(slope), int(ca), thal]

    result_dict = {}
    avg = 0
    for model in all_models:
        res = model.predict([features])
        if res[0] == 1:
            result_dict[model] = "High Chance of Heart Disease"
        else:
            result_dict[model] = "Low Chance of Heart Disease"
        avg += res
    accuracy = round(avg[0] / 5, 2)

    personal_info = [name, email]
    responses = [result_dict, personal_info, accuracy]

    return render_template("result.html", result=responses)

@app.route('/login', methods=['POST'])
def login():
    # Extract email and password from the request JSON data
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Perform authentication logic (example)
    # You should replace this with your actual authentication logic
    if email == email and password == password:
        # If authentication succeeds, redirect to index.html
        return jsonify({'redirect': '/index'})
    else:
        # If authentication fails, return an error response
        return jsonify({'error': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
