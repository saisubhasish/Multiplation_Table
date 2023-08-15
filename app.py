import sys
from flask import Flask, request, jsonify, url_for, render_template
from flask_cors import CORS, cross_origin
import numpy as np
from dask import dataframe as dd
from multiplicationTable.predictor import ModelResolver
from multiplicationTable.logger import logging
from multiplicationTable.utils import load_object
from multiplicationTable.exception import MultiplicationException

app = Flask(__name__)
CORS(app)


logging.info("Creating model resolver object")
model_resolver = ModelResolver(model_registry="saved_models")   # Location where models are saved


# Load the model
transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
model = load_object(file_path=model_resolver.get_latest_model_path())

@app.route('/')
@cross_origin()
def home():
    try:
        return render_template('home.html')
    
    except Exception as e:
        raise MultiplicationException(error_message=e, error_detail=sys)

@app.route('/predict_api', methods=['POST'])
@cross_origin()
def predict_api():
    try:
        data = [float(x) for x in request.form.values()]
        final_data = np.array(data).reshape(1,-1)
        logging.info(f"The input for the real time prediction: {final_data}")
        prediction = model.predict(final_data)
        print(prediction)
        logging.info(f"The predicted output on the real time data: {prediction}")
        
        return render_template('home.html', output_text="The prediction of Sales on advertisement is: {}.".format(prediction))
    
    except Exception as e:
        raise MultiplicationException(error_message=e, error_detail=sys)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
