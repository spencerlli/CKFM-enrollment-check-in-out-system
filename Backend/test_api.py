from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def root():
    t = {
        "status": 0,
        "msg": "I'm test message",
        "data": {
            'a': 1,
            'b': 2,
            'c': [3, 4, 5]
        }
    }
    
    return jsonify(t)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
