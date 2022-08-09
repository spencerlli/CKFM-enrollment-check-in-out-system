from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)


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


@app.route('/student', methods=['GET', 'POST', 'OPTIONS'])
def student():
    t = {
        "status": 0,
        "msg": "Successfully get students!",
        "data": {
            "student_list": [
                {
                    "first_name": "Yuan JR",
                    "last_name": "Zhang",
                    "birth_date": "2022-07-27",
                    "gender": "M",
                    "school": "UC",
                    "grade": "A",
                    "allergies": None,
                    "allergies_medications": None,
                    "medications": None,
                    "emergency": "Yuan Zhang",
                    "emergency_phone": "001",
                    "insurance": "UC SHIP"
                },
                {
                    "first_name": "Lingxin JR",
                    "last_name": "Li",
                    "birth_date": "2022-07-27",
                    "gender": "F",
                    "school": "UC",
                    "grade": "A",
                    "allergies": None,
                    "allergies_medications": None,
                    "medications": None,
                    "emergency": "Lingxin Li",
                    "emergency_phone": "002",
                    "insurance": "UC SHIP"
                },
                {
                    "first_name": "Chang JR",
                    "last_name": "Liu",
                    "birth_date": "2022-07-27",
                    "gender": "M",
                    "school": "UC",
                    "grade": "A",
                    "allergies": None,
                    "allergies_medications": None,
                    "medications": None,
                    "emergency": "Yuan Zhang",
                    "emergency_phone": "001",
                    "insurance": "UC SHIP"
                },
            ]
        }
    }

    return jsonify(t)


@app.route('/guardian', methods=['GET', 'POST', 'OPTIONS'])
def guardian():
    t = {
        "status": 0,
        "msg": "Successfully get guardians!",
        "data": {
            "guardian_list": [
                {
                    "first_name": "Yuan",
                    "last_name": "Zhang",
                    "relationship": "Father",
                    "special": True,
                    "phone_number": "001",
                    "email": "yuanzhang@ckfm.com",
                    "street": "16808 Armstrong Ave",
                    "city": "Irvine",
                    "state": "CA",
                    "zip_code": "92606",
                },
                {
                    "first_name": "Lingxin",
                    "last_name": "Li",
                    "relationship": "Mother",
                    "special": True,
                    "phone_number": "002",
                    "email": "lingxinli@ckfm.com",
                    "street": "16808 Armstrong Ave",
                    "city": "Irvine",
                    "state": "CA",
                    "zip_code": "92606",
                },
            ]
        }
    }

    return jsonify(t)


@app.route('/crud', methods=['GET', 'POST', 'OPTIONS', 'DELETE'])
def crud():
    if (request.method == 'DELETE'):
        return 'Successfully delete!', 200
    t = {
        "status": 0,
        "msg": "Successfully get crud items!",
        "data": {
            "items": [
                {
                    "id": 1,
                    "first_name": "Yuan JR",
                    "last_name": "Zhang",
                    "birth_date": "2022-07-27",
                    "gender": "M",
                    "school": "UC",
                    "grade": "A",
                    "allergies": None,
                    "allergies_medications": None,
                    "medications": None,
                    "emergency": "Yuan Zhang",
                    "emergency_phone": "001",
                    "insurance": "UC SHIP"
                },
                {
                    "id": 2,
                    "first_name": "Lingxin JR",
                    "last_name": "Li",
                    "birth_date": "2022-07-27",
                    "gender": "F",
                    "school": "UC",
                    "grade": "A",
                    "allergies": None,
                    "allergies_medications": None,
                    "medications": None,
                    "emergency": "Lingxin Li",
                    "emergency_phone": "002",
                    "insurance": "UC SHIP"
                },
                {
                    "id": 3,
                    "first_name": "Chang JR",
                    "last_name": "Liu",
                    "birth_date": "2022-07-27",
                    "gender": "M",
                    "school": "UC",
                    "grade": "A",
                    "allergies": None,
                    "allergies_medications": None,
                    "medications": None,
                    "emergency": "Yuan Zhang",
                    "emergency_phone": "001",
                    "insurance": "UC SHIP"
                }
            ],
            "hasNext": True
        }
    }

    return jsonify(t)


@app.route('/requestForm', methods=['GET', 'POST', 'OPTIONS'])
def requestForm():
    print(type(request.json))
    t = {
        "status": 0,
        "msg": "I am the response!",
        "data": {}
    }
    return jsonify(t)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
