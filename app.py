import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

def ValuePredictor(to_predict_list):
    try:
        to_predict = np.array(to_predict_list).reshape(1, 7)
        loaded_model = pickle.load(open("model.pkl", "rb"))
        result = loaded_model.predict(to_predict)
        return result[0]
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        if request.method == 'POST':
            to_predict_list = request.form.to_dict()
            to_predict_list = list(to_predict_list.values())
            to_predict_list = list(map(float, to_predict_list))
            result = ValuePredictor(to_predict_list)
            if int(result) == 1:
                prediction = 'Given transaction is fraudulent'
            else:
                prediction = 'Given transaction is NOT fraudulent'
            return render_template("result.html", prediction=prediction)
        else:
            return "Please submit the form to predict."
    except Exception as e:
        return render_template("error.html", error_message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
