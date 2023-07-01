from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf

app = Flask(__name__, static_folder='static')


f= open(r"./Subpopulation.pkl", "rb") 
modelp=pickle.load(f)



modelh = tf.keras.models.load_model('Height.h5')
Subpopulation_dict={
    0:'Temperate Japonica',
    1:'Indica I', 2:'Indica II', 3:'VI/Aromatic',
       4:'Indica Intermediate', 5:'Aus', 6:'Intermediate', 7:'Tropical Japonica',
       8:'Indica III', 9:'Japonica Intermediate'
}  

@app.route("/")
def home():
    return render_template("index.html", title="Home Page")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        seq = data.get('burr')
        print(seq)
        seq = "".join(str({"A": 0, "C": 1, "T": 2, "G": 3}.get(char, char)) for char in seq)
        seq=list(map(int, seq))  
        print(seq)
        high = modelh.predict([seq])
        pop = modelp.predict([seq])
        print(high)
        print(pop)

        pre_high = high[0][0]
        pred_pop = pop[0]
        pred_pop=Subpopulation_dict[pred_pop]
        

        return jsonify({'h': float(pre_high), 's': str(pred_pop)})

if __name__ == "__main__":
    app.run(debug=True)
