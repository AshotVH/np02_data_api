from flask import Flask, request
from flask_cors import CORS
import requests
import os
app = Flask(__name__)

allowed_origins = [
    "https://np02test-slow-control.app.cern.ch",
    "https://np02-slow-control.app.cern.ch"
]


# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
CORS(app)

API_ADDRESS = os.environ.get("API_ADDRESS")


@app.route('/np02cachedvals', methods=['GET'])
def np02cachedvals():
    args = request.args
    elemName = args.get('elemname')
    try:
        response = requests.get(f"{API_ADDRESS}/latest/{elemName}", timeout=30)
        print(f">>> INTERNAL RESPONSE | status={response.status_code} | body={response.text[:300]}", flush=True)
        return response.json()
    except requests.exceptions.Timeout:
        print(f">>> TIMEOUT for elemName={elemName}", flush=True)
        return {"error": "Internal API timeout"}, 504
    except Exception as e:
        print(f">>> EXCEPTION | {type(e).__name__}: {str(e)}", flush=True)
        return {"error": f"Failed to fetch data: {str(e)}"}, 500
    

@app.route('/np02histogram/<elem_id>/<start_date>/<end_date>')
def np02histogram(start_date, end_date, elem_id):
    try:
        response = requests.get(f"{API_ADDRESS}/range/{start_date}/{end_date}/{elem_id}", timeout=30)
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Internal API timeout"}, 504
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}, 500

@app.route('/np02histogram_average/<elem_id>/<start_date>/<end_date>')
def np02histogram_average(start_date, end_date, elem_id):
    try:
        response  = requests.get(f"{API_ADDRESS}/average/{start_date}/{end_date}/{elem_id}", timeout=30)
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Internal API timeout"}, 504
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}, 500

@app.route('/sensorname/<elem_id>/')
def sensorname(elem_id):
    try:
        response = requests.get(f"{API_ADDRESS}/sensor-name/{elem_id}", timeout=30)
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Internal API timeout"}, 504
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
