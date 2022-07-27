from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():
    t = {
        "status": 0,
        "msg": "",
        "data": {
            'a': 1,
            'b': 2,
            'c': [3, 4, 5]
        }
    }
    
    return jsonify(t)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
