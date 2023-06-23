from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf

app = Flask(__name__, static_folder='static')

def getpop():
    with open(r"C:\Users\91994\Desktop\oryza sativa height prediction\flask\Subpopulation.pkl", "rb") as f:
        model=pickle.load(f)
    return model

def getheight():
    model = tf.keras.models.load_model('Height.h5')
    return model

@app.route("/")
def home():
    return render_template("index.html", title="Home Page")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        modelp = getpop()
        modelh = getheight()
        seq = request.input_stream["burr"]
        seq = "".join(str({"A": 0, "C": 1, "T": 2, "G": 3}.get(char, char)) for char in seq)
        high = modelh.predict([[seq]])
        pop = modelp.predict([seq])

        pre_high = high[0]
        pred_pop = pop[0]

        return render_template("index.html", h="asdfghjk", s=pred_pop)

if __name__ == "__main__":
    app.run(debug=True)
