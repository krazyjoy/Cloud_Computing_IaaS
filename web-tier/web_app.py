import concurrent.futures
import pandas as pd
from flask import Flask, request, jsonify

def image_classification(df, filename):

    basename = filename.split('.')[0]

    try:
        result = df[df['Image'] == basename]['Results'].iloc[0]
        return result
    except IndexError:
        return f"{filename} not found in imageTable"



app = Flask(__name__)
@app.route('/', methods=['POST'])
def handle_post_request():
    # print("handle post request")
    if 'inputFile' not in request.files:
        return "No inputFile key", 400

    file = request.files['inputFile']
    filename = file.filename

    try:
        # print("inside try except")
        result = image_classification(df, filename)
        return f"{filename}: {result}"
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == '__main__':
    df = pd.read_csv('./web-tier/imageTable.csv')

    app.run(debug=True, host="0.0.0.0", port=5000)
