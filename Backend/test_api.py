import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

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


@app.route('/guardian', methods=['GET', 'POST', 'DELETE'])
@app.route('/guardian/<id>', methods=['PUT', 'DELETE'])
def guardian(id=None):
    if request.method == 'DELETE':
        return {"status": 0,
                "msg": "Successfully get crud items!",
                "data": {}}, 200
    t = {
        "status": 0,
        "msg": "Successfully get guardians!",
        "data": {
            "items": [
                {
                    "password": "123456",
                    "relationship": "Father",
                    "check_in_method": "barcode",
                    "last_name": "liuTest1",
                    "phone_number": "0000000001",
                    "id": 1,
                    "email": "chang1@test.com",
                    "first_name": "changTest1"
                },
                {
                    "password": "123456",
                    "relationship": "Mother",
                    "check_in_method": "barcode",
                    "last_name": "liuTest2",
                    "phone_number": "0000000002",
                    "id": 2,
                    "email": "chang2@test.com",
                    "first_name": "changTest2"
                },
                {
                    "password": "123456",
                    "relationship": "Father",
                    "check_in_method": "barcode",
                    "last_name": "liuTest3",
                    "phone_number": "0000000003",
                    "id": 3,
                    "email": "chang3@test.com",
                    "first_name": "changTest3"
                },
                {
                    "password": "123456",
                    "relationship": "Mother",
                    "check_in_method": "barcode",
                    "last_name": "liuTest4",
                    "phone_number": "0000000004",
                    "id": 4,
                    "email": "chang4@test.com",
                    "first_name": "changTest4"
                }
            ],
            "hasNext": False
        }
    }

    return jsonify(t)


@app.route('/student', methods=['GET', 'POST', 'DELETE'])
@app.route('/student/<id>', methods=['PUT', 'DELETE'])
def student(id=None):
    if (request.method == 'DELETE'):
        return {"status": 0,
                "msg": "Successfully get crud items!",
                "data": {}}, 200
    t = {
        "status": 0,
        "msg": "Successfully get students!",
        "data": {
            "items": [
                {
                    "sunday_school": True,
                    "kid_choir": False,
                    "birth_date": "1659337200",
                    "CM_lounge": False,
                    "U3_friday": False,
                    "id": 1,
                    "friday_lounge": False,
                    "allergies": "ibuprofen",
                    "gender": "male",
                    "first_name": "changJRTest1",
                    "grade": "1",
                    "check_in_method": "barcode",
                    "friday_night": False,
                    "last_name": "liuTest1"
                },
                {
                    "sunday_school": False,
                    "kid_choir": False,
                    "birth_date": "1659423600",
                    "CM_lounge": True,
                    "U3_friday": False,
                    "id": 2,
                    "friday_lounge": False,
                    "allergies": "none",
                    "gender": "female",
                    "first_name": "changJRTest2",
                    "grade": "2",
                    "check_in_method": "barcode",
                    "friday_night": False,
                    "last_name": "liuTest2"
                },
                {
                    "sunday_school": False,
                    "kid_choir": True,
                    "birth_date": "1659510000",
                    "CM_lounge": False,
                    "U3_friday": False,
                    "id": 3,
                    "friday_lounge": False,
                    "allergies": "ibuprofen",
                    "gender": "male",
                    "first_name": "changJRTest3",
                    "grade": "3",
                    "check_in_method": "barcode",
                    "friday_night": False,
                    "last_name": "liuTest3"
                },
                {
                    "sunday_school": False,
                    "kid_choir": False,
                    "birth_date": "1659596400",
                    "CM_lounge": False,
                    "U3_friday": True,
                    "id": 4,
                    "friday_lounge": False,
                    "allergies": "none",
                    "gender": "female",
                    "first_name": "changJRTest4",
                    "grade": "4",
                    "check_in_method": "barcode",
                    "friday_night": False,
                    "last_name": "liuTest4"
                },
                {
                    "sunday_school": False,
                    "kid_choir": False,
                    "birth_date": "1998",
                    "CM_lounge": False,
                    "U3_friday": False,
                    "id": 5,
                    "friday_lounge": False,
                    "allergies": "0",
                    "gender": "M",
                    "first_name": "changJRTest5",
                    "grade": "2",
                    "check_in_method": "barcode",
                    "friday_night": False,
                    "last_name": "liuJRTest5"
                }
            ],
            "hasNext": False
        }
    }

    return jsonify(t)


@app.route('/familyInfo', methods=['GET', 'POST', 'DELETE'])
@app.route('/familyInfo/<id>', methods=['PUT', 'DELETE'])
def familyInfo(id=None):
    if (request.method == 'DELETE'):
        return {"status": 0,
                "msg": "Successfully get crud items!",
                "data": {}}, 200
    t = {
        "status": 0,
        "msg": "Successfully get students!",
        "data": {
            "items": [
                {
                    "friday_night": "table",
                    "city": "cityTest1",
                    "zip": "00001",
                    "state": "stateTest1",
                    "pay": 1,
                    "id": 1,
                    "street": "streetTest1",
                    "insurance": "insuranceTest1",
                    "group": 1,
                    "checkbox": True,
                    "special_events": "A",
                    "sunday_school": "table",
                    "insurance_policy": "insPhoneTest1",
                    "physician": "physicianTest1",
                    "insurance_phone": "policyTest1",
                    "physician_phone": "phyPhoneTest1"
                },
                {
                    "friday_night": "snack",
                    "city": "cityTest3",
                    "zip": "00003",
                    "state": "stateTest3",
                    "pay": 4,
                    "id": 2,
                    "street": "streetTest3",
                    "insurance": "insuranceTest3",
                    "group": 3,
                    "checkbox": True,
                    "special_events": "B",
                    "sunday_school": "teacher",
                    "insurance_policy": "insPhoneTest3",
                    "physician": "physicianTest3",
                    "insurance_phone": "policyTest3",
                    "physician_phone": "phyPhoneTest3"
                }
            ],
            "hasNext": False
        }
    }

    return jsonify(t)



@app.route('/family', methods=['GET', 'POST', 'DELETE'])
@app.route('/family/<id>', methods=['PUT', 'DELETE'])
def family(id=None):
    if (request.method == 'DELETE'):
        return {"status": 0,
                "msg": "Successfully get crud items!",
                "data": {}}, 200
    t = {
        "status": 0,
        "msg": "Successfully get students!",
        "data": {
            "items": [
                {
                    "student_id": 1,
                    "id": 1,
                    "guardian_id": 1
                },
                {
                    "student_id": 2,
                    "id": 1,
                    "guardian_id": 1
                },
                {
                    "student_id": 1,
                    "id": 1,
                    "guardian_id": 2
                },
                {
                    "student_id": 2,
                    "id": 1,
                    "guardian_id": 2
                },
                {
                    "student_id": 3,
                    "id": 2,
                    "guardian_id": 3
                },
                {
                    "student_id": 4,
                    "id": 2,
                    "guardian_id": 3
                },
                {
                    "student_id": 3,
                    "id": 2,
                    "guardian_id": 4
                },
                {
                    "student_id": 4,
                    "id": 2,
                    "guardian_id": 4
                }
            ],
            "hasNext": False
        }
    }

    return jsonify(t)


@app.route('/userManage', methods=['GET'])
@app.route('/userManage/<object>', methods=['POST', 'DELETE'])
@app.route('/userManage/<object>/<id>', methods=['PUT', 'DELETE'])
def userManage(object=None, id=None):
    res = {
        "status": 0,
        "msg": None,
        "data": {
            "items": [
                {
                    "checkbox": True,
                    "city": "cityTest1",
                    "friday_night": "table",
                    "group": 1,
                    "id": 1,
                    "insurance": "insuranceTest1",
                    "insurance_phone": "policyTest1",
                    "insurance_policy": "insPhoneTest1",
                    "object": "familyInfo",
                    "pay": 1,
                    "physician": "physicianTest1",
                    "physician_phone": "phyPhoneTest1",
                    "special_events": "A",
                    "state": "stateTest1",
                    "street": "streetTest1",
                    "sunday_school": "table",
                    "zip": "00001"
                },
                {
                    "check_in_method": "barcode",
                    "email": "chang1@test.com",
                    "first_name": "changTest1",
                    "id": 1,
                    "last_name": "liuTest1",
                    "object": "guardian",
                    "password": "123456",
                    "phone_number": "0000000001",
                    "relationship": "Father"
                },
                {
                    "check_in_method": "barcode",
                    "email": "chang2@test.com",
                    "first_name": "changTest2",
                    "id": 2,
                    "last_name": "liuTest2",
                    "object": "guardian",
                    "password": "123456",
                    "phone_number": "0000000002",
                    "relationship": "Mother"
                },
                {
                    "CM_lounge": False,
                    "U3_friday": False,
                    "allergies": "ibuprofen",
                    "birth_date": "1659337200",
                    "check_in_method": "barcode",
                    "first_name": "changJRTest1",
                    "friday_lounge": False,
                    "friday_night": False,
                    "gender": "male",
                    "grade": "1",
                    "id": 1,
                    "kid_choir": False,
                    "last_name": "liuTest1",
                    "object": "student",
                    "sunday_school": True
                },
                {
                    "CM_lounge": True,
                    "U3_friday": False,
                    "allergies": "none",
                    "birth_date": "1659423600",
                    "check_in_method": "barcode",
                    "first_name": "changJRTest2",
                    "friday_lounge": False,
                    "friday_night": False,
                    "gender": "female",
                    "grade": "2",
                    "id": 2,
                    "kid_choir": False,
                    "last_name": "liuTest2",
                    "object": "student",
                    "sunday_school": False
                }
            ],
            "hasNext": False
        }
    }
    
    return jsonify(res)


# @app.route('/crud', methods=['GET', 'PUT', 'POST', 'DELETE'])
# def crud():
#     if (request.method == 'DELETE'):
#         return {"status": 0,
#                 "msg": "Successfully get crud items!",
#                 "data": {}}, 200
#     t = {
#         "status": 0,
#         "msg": "Successfully get crud items!",
#         "data": {
#             "items": [
#                 {
#                     "id": 1,
#                     "first_name": "Yuan JR",
#                     "last_name": "Zhang",
#                     "birth_date": "2022-07-27",
#                     "gender": "M",
#                     "school": "UC",
#                     "grade": "A",
#                     "allergies": None,
#                     "allergies_medications": None,
#                     "medications": None,
#                     "emergency": "Yuan Zhang",
#                     "emergency_phone": "001",
#                     "insurance": "UC SHIP"
#                 },
#                 {
#                     "id": 2,
#                     "first_name": "Lingxin JR",
#                     "last_name": "Li",
#                     "birth_date": "2022-07-27",
#                     "gender": "F",
#                     "school": "UC",
#                     "grade": "A",
#                     "allergies": None,
#                     "allergies_medications": None,
#                     "medications": None,
#                     "emergency": "Lingxin Li",
#                     "emergency_phone": "002",
#                     "insurance": "UC SHIP"
#                 },
#                 {
#                     "id": 3,
#                     "first_name": "Chang JR",
#                     "last_name": "Liu",
#                     "birth_date": "2022-07-27",
#                     "gender": "M",
#                     "school": "UC",
#                     "grade": "A",
#                     "allergies": None,
#                     "allergies_medications": None,
#                     "medications": None,
#                     "emergency": "Yuan Zhang",
#                     "emergency_phone": "001",
#                     "insurance": "UC SHIP"
#                 }
#             ],
#             "hasNext": True
#         }
#     }

#     return jsonify(t)


@app.route('/requestForm', methods=['GET', 'POST', 'OPTIONS'])
def requestForm():
    t = {
        "status": 0,
        "msg": "I am the response!",
        "data": {}
    }
    with open("c.json", "w+") as f:
        f.write(json.dumps(request.json))
    # print(type(json.loads(request.json)))
    return jsonify(t)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
