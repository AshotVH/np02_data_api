from flask import Flask, request
from flask_cors import CORS
import requests
import os
app = Flask(__name__)

allowed_origins = [
    "https://np02test-slow-control.app.cern.ch",
    "https://np02-slow-control.app.cern.ch"
]


CORS(app, resources={r"/*": {"origins": "*"}})
API_ADDRESS = os.environ.get("API_ADDRESS")


@app.route('/np02cachedvals', methods=['GET'])
def np02cachedvals():
    args = request.args
    elemName = args.get('elemname')
    response = requests.get(f"{API_ADDRESS}/latest/{elemName}")
    return response.json()
@app.route('/np02histogram/<elem_id>/<start_date>/<end_date>')
def np02histogram(start_date, end_date, elem_id):
    response = requests.get(f"{API_ADDRESS}/range/{start_date}/{end_date}/{elem_id}")
    return response.json()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
