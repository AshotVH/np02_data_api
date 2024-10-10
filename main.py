from flask import Flask
import requests
import os
app = Flask(__name__)

@app.route('/response')
def response():
    response = requests.get("http://188.185.78.106:5000/latest/cryostat")
    return response.json()
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
