import random
# import MySQLdb.cursors
# from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import pymysql
import os
from flask_cors import CORS
import requests
from config import REST_API

# pymysql.install_as_MySQLdb()

template_dir = os.path.abspath('../AttendancePro')
static_dir = os.path.abspath('../AttendancePro/sdk')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = '123456'

CORS(app, resources=r'/*', supports_credentials=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if ('loggedin' in session.keys() and session['loggedin'] == True):
        return render_template('flask_templates/index.html')
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['loggedin'] = True
        msg = 'Logged in successfully!'
        return render_template('flask_templates/index.html', msg=msg)

    return render_template('flask_templates/login.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    return render_template('flask_templates/register.html', msg=msg)


@app.route('/enrollFamily', methods=['GET', 'POST', 'OPTIONS'])
def enrollFamily():
    if request.method == 'POST':
        # guardian
        guardian_list = []
        for guardian in request.json['guardians']:
            guardian_json = {}
            guardian_json['first_name'] = guardian['fname']
            guardian_json['last_name'] = guardian['lname']
            guardian_json['phone_number'] = guardian['phone']
            guardian_json['email'] = guardian['email']
            guardian_json['relationship'] = guardian['relationship']
            guardian_json['check_in_method'] = guardian['method']

            guardian_res = requests.post(
                REST_API + '/guardian', json=guardian_json)
            guardian_list.append(guardian_res.json())

        # student
        student_list = []
        for student in request.json['students']:
            student_json = {}
            student_json['first_name'] = student['fname']
            student_json['last_name'] = student['lname']
            student_json['birth_date'] = student['date']
            student_json['gender'] = student['gender']
            student_json['grade'] = student['grade']
            student_json['allergies'] = student['allergy']
            student_json['check_in_method'] = student['method']

            programs = ['sunday_school', 'CM_lounge', 'kid_choir',
                        'U3_friday', 'friday_lounge', 'friday_night']
            for i, program in enumerate(programs):
                student_json[program] = student['program'][0][i]['checked']

            student_res = requests.post(
                REST_API + '/student', json=student_json)
            student_list.append(student_res.json())

        # familyInfo
        familyInfo_json = {}
        familyInfo_json['street'] = request.json['guardians'][0]['street']
        familyInfo_json['city'] = request.json['guardians'][0]['city']
        familyInfo_json['state'] = request.json['guardians'][0]['state']
        familyInfo_json['zip'] = request.json['guardians'][0]['zip']

        familyInfo_json['physician'] = request.json['guardians'][0]['physician']
        familyInfo_json['physician_phone'] = request.json['guardians'][0]['physician_phone']
        familyInfo_json['insurance'] = request.json['guardians'][0]['insurance']
        familyInfo_json['insurance_phone'] = request.json['guardians'][0]['insurance_phone']
        familyInfo_json['insurance_policy'] = request.json['guardians'][0]['insurance_number']
        familyInfo_json['group'] = request.json['guardians'][0]['group']
        familyInfo_json['sunday_school'] = request.json['guardians'][0]['sunday']
        familyInfo_json['friday_night'] = request.json['guardians'][0]['friday']
        familyInfo_json['special_events'] = request.json['guardians'][0]['special']

        familyInfo_json['pay'] = request.json['pay']
        familyInfo_json['checkbox'] = request.json['checkbox']

        familyInfo_res = requests.post(
            REST_API + '/familyInfo', json=familyInfo_json)
        familyInfo_json = familyInfo_res.json()

        # family
        family_json = {}
        family_json['id'] = familyInfo_json['id']
        for guardian in guardian_list:
            for student in student_list:

                family_json['guardian_id'] = guardian['id']
                family_json['student_id'] = student['id']

                family_res = requests.post(
                    REST_API + '/family', json=family_json)
                family_json = family_res.json()

    ans = {
        "status": 0,
        "msg": "Successfully enrolled!",
        "data": {}
    }
    return jsonify(ans)


@app.route('/admin/<object>', methods=['GET', 'POST', 'DELETE'])
@app.route('/admin/<object>/<id>', methods=['PUT', 'DELETE'])
def admin(object, id=None):
    res = {
        "status": 0,
        "msg": None,
        "data": {
            "items": [],
            "hasNext": False
        }
    }

    if request.method == 'GET':
        # guardian_json = requests.get(REST_API + '/guardian').json()
        # student_json = requests.get(REST_API + '/student').json()
        # familyInfo_json = requests.get(REST_API + '/familyInfo').json()
        # family_json = requests.get(REST_API + '/family').json()
        object_json = requests.get(REST_API + '/' + object).json()


        # get_json['guardian'] = guardian_json
        # get_json['student'] = student_json
        # get_json['familyInfo'] = familyInfo_json
        # get_json['family'] = family_json

        res['data']['items'] = object_json
        res['msg'] = 'Successfully get data!'
    elif request.method == 'PUT' or 'POST':
        object_json = dict(request.json)
        if request.method == 'PUT':
            requests.put(REST_API + '/' + object + '/' + id, json=object_json)
            res['msg'] = 'Successfully update!'
        else:
            requests.post(REST_API + '/' + object, json=object_json)
            res['msg'] = 'Successfully add!'
    else:
        if id:
            requests.delete(REST_API + '/' + object + '/' + id)
            res['msg'] = 'Successfully delete!'
        else:
            pass
            # requests.delete(REST_API + '/' + object)

    if not res['msg']:
        res['msg'] = 'Error happened.'
        res['status'] = 400

    return jsonify(res)


@app.route('/userManage', methods=['GET'])
@app.route('/userManage/<object>', methods=['POST', 'DELETE'])
@app.route('/userManage/<object>/<id>', methods=['PUT', 'DELETE'])
def userManage(object=None, id=None):
    res = {
        "status": 0,
        "msg": None,
        "data": {
            "items": [],
            "hasNext": False
        }
    }

    # family_id = session['family_id']
    family_id = 1
    family_json = requests.get(REST_API + '/family/%d' % family_id).json()
    guardian_ids, student_ids = set(), set()
    for family in family_json:
        guardian_ids.add(family['guardian_id'])
        student_ids.add(family['student_id'])

    familyInfo_json = requests.get(REST_API + '/familyInfo/%d' % family_id).json()
    familyInfo_json['object'] = 'familyInfo'
    res['data']['items'].append(familyInfo_json)
    for guardian_id in guardian_ids:
        guardian_json = requests.get(REST_API + '/guardian/%d' % guardian_id).json()
        guardian_json['object'] = 'guardian'
        res['data']['items'].append(guardian_json)
    for student_id in student_ids:
        student_json = requests.get(REST_API + '/student/%d' % student_id).json()
        student_json['object'] = 'student'
        res['data']['items'].append(student_json)
    
    return jsonify(res)


@app.route('/firstTimeEnroll', methods=['GET', 'POST'])
def firstTimeEnroll():
    msg = ''
    if request.method == 'GET':
        return render_template('flask_enrollment/GuardianEnrollment.html', msg=msg)
    else:
        return render_template('flask_enrollment/StudentEnrollment.html', msg=msg)


@app.route('/studentEnrollment', methods=['GET', 'POST'])
def studentEnrollment():
    return render_template('flask_enrollment/StudentEnrollment.html')


@app.route('/enrollmentCheck', methods=['GET', 'POST'])
def enrollmentCheck():
    return render_template('flask_enrollment/CompleteEnrollmentCheck.html')


@app.route('/checkInOut', methods=['GET', 'POST'])
def checkInOut():
    return render_template('flask_check_in_out/main.html')


@app.route('/checkIn', methods=['GET', 'POST'])
def checkIn():
    return render_template('flask_check_in_out/check_in.html')


@app.route('/checkIn2', methods=['GET', 'POST'])
def checkIn2():
    return render_template('flask_check_in_out/check_in2.html')


@app.route('/checkInSuccess', methods=['GET', 'POST'])
def checkInSuccess():
    return render_template('flask_check_in_out/s_check_in.html')


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    return render_template('flask_check_in_out/check_out.html')


@app.route('/checkOut2', methods=['GET', 'POST'])
def checkOut2():
    return render_template('flask_check_in_out/check_out2.html')


@app.route('/checkOutSuccess', methods=['GET', 'POST'])
def checkOutSuccess():
    return render_template('flask_check_in_out/s_check_out.html')


def generate_random_str(randomLength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(randomLength):
        random_str += base_str[random.randint(0, length)]
    return random_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
