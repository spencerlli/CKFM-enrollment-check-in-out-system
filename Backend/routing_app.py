import random
# import MySQLdb.cursors
# from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
# import pymysql
import os
from flask_cors import CORS
import requests
from config import REST_API
from copy import deepcopy
import datetime

# pymysql.install_as_MySQLdb()

template_dir = os.path.abspath('../AttendancePro')
static_dir = os.path.abspath('../AttendancePro/sdk')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = '123456'

CORS(app, resources=r'/*', supports_credentials=True)

RES_TEMPLATE = {
    'status': 0,
    'msg': None,
    'data': {}
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if ('login' in session.keys() and session['login'] == True):
        return render_template('flask_templates/index.html')
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print(request.cookies.get('login'))
        return render_template('log_in/log_in.html')

    else:   # method == POST
        res_json = deepcopy(RES_TEMPLATE)
        if 'phone' in request.json and 'pwd' in request.json:
            phone = request.json['phone']
            pwd = request.json['pwd']
            guardian_json = requests.get(REST_API + '/guardian/phone/' + phone).json()
            if guardian_json['pwd'] == pwd:
                res_json['msg'] = 'Logged in successfully!'
                family_json = requests.get(REST_API + '/family/guardian/%d' % guardian_json['id']).json()

                res = jsonify(res_json)
                expire_date = datetime.datetime.now() + datetime.timedelta(minutes=2)
                res.set_cookie(key='login', value="1", expires=expire_date)
                res.set_cookie(key='guardian_id', value=str(guardian_json['id']), expires=expire_date)
                res.set_cookie(key='family_id', value=str(family_json[0]['id']), expires=expire_date)
                return res
            else:
                res_json['status'] = 1
                res_json['msg'] = 'Incorrect phone number or password!'
        else:
            res_json['status'] = 1
            res_json['msg'] = 'Please input phone number and password!'

        return jsonify(res_json)


@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('guardian_id', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    return render_template('flask_templates/register.html', msg=msg)


@app.route('/enrollFamily', methods=['GET', 'POST', 'OPTIONS'])
def enrollFamily():
    res = {
        'status': 0,
        'msg': 'Successfully enrolled!',
        'data': {}
    }

    if request.method == 'POST':
        # guardian
        guardian_list = []
        for guardian in request.json['guardians']:
            guardian_json = {}
            guardian_json['fname'] = guardian['fname']
            guardian_json['lname'] = guardian['lname']
            guardian_json['check_in_method'] = guardian['method']

            guardian_json['phone'] = guardian.get('phone')
            guardian_json['email'] = guardian.get('email')
            guardian_json['relationship'] = guardian.get('relationship')

            guardian_res = requests.post(
                REST_API + '/guardian', json=guardian_json)
            guardian_list.append(guardian_res.json())

        # student
        student_list = []
        for student in request.json['students']:
            student_json = {}
            student_json['fname'] = student['fname']
            student_json['lname'] = student['lname']
            student_json['check_in_method'] = student['method']

            student_json['birthdate'] = student.get('date')
            student_json['gender'] = student.get('gender')
            student_json['grade'] = student.get('grade')
            student_json['allergies'] = student.get('allergy')

            programs = ['sunday_school', 'cm_lounge', 'kid_choir',
                        'U3_friday', 'friday_lounge', 'friday_night']
            for i, program in enumerate(programs):
                student_json[program] = student['program'][0][i]['checked']

            student_res = requests.post(
                REST_API + '/student', json=student_json)
            student_list.append(student_res.json())

        # familyInfo
        familyInfo_json = {}
        familyInfo_json['street'] = request.json['guardians'][0].get('street')
        familyInfo_json['city'] = request.json['guardians'][0].get('city')
        familyInfo_json['state'] = request.json['guardians'][0].get('state')
        familyInfo_json['zip'] = request.json['guardians'][0].get('zip')

        familyInfo_json['physician'] = request.json['guardians'][0].get('physician')
        familyInfo_json['physician_phone'] = request.json['guardians'][0].get('physician_phone')
        familyInfo_json['insurance'] = request.json['guardians'][0].get('insurance')
        familyInfo_json['insurance_phone'] = request.json['guardians'][0].get('insurance_phone')
        familyInfo_json['insurance_policy'] = request.json['guardians'][0].get('insurance_number')
        familyInfo_json['group'] = request.json['guardians'][0].get('group')

        familyInfo_json['sunday_school'] = request.json['guardians'][0]['sunday']
        familyInfo_json['friday_night'] = request.json['guardians'][0]['friday']
        familyInfo_json['special_events'] = request.json['guardians'][0].get('special')

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

    return jsonify(res)


@app.route('/admin/<object>', methods=['GET', 'POST', 'DELETE'])
@app.route('/admin/<object>/<id>', methods=['PUT', 'DELETE'])
def admin(object, id=None):
    res = {
        'status': 0,
        'msg': None,
        'data': {
            'items': [],
            'hasNext': False
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
        'status': 0,
        'msg': None,
        'data': {
            'items': [],
            'hasNext': False
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


@app.route('/preCheckIn', methods=['GET', 'POST'])
def preCheckIn():
    session['login'] = True
    session['user'] = 'guardian'
    session['guardian_id'] = 1
    session['family_id'] = 1

    res = deepcopy(RES_TEMPLATE)

    if request.method == 'GET':
        # a relation object with repeat guardians and students
        family_json = requests.get(REST_API + '/family/%d' % session['family_id']).json()
        # filter repeat to be unique
        guardian_id_set, student_id_set = set(), set()
        # list of json objects
        object_list = []

        for family in family_json:
            print(family)
            if family['guardian_id'] not in guardian_id_set:    # filter repeat
                guardian_json = requests.get(REST_API + '/guardian/%d' % family['guardian_id']).json()
                object_list.append({
                    'object': 'guardian',
                    'id': guardian_json['guardian_id'],
                    'fname': guardian_json['fname'],
                    'lname': guardian_json['lname']
                })
                guardian_id_set.add(family['guardian_id'])

            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(REST_API + '/student/%d' % family['student_id']).json()
                if student_json.get('check_in') and student_json.get('check_in', 0) == 0:
                    object_list.append({
                        'object': 'student',
                        'id': student_json['student_id'],
                        'fname': student_json['fname'],
                        'lname': student_json['lname']
                    })
                    student_id_set.add(family['student_id'])

        res['data']['items'] = object_list
        res['msg'] = 'Successfully get guardians and students!'
    else:   # POST
        guardian_id = 0
        student_list = []
        for object_json in request.json.get('items'):
            if object_json['object'] == 'guardian':  # selected guardian
                guardian_id = int(request.json.get('id'))
            else:
                student_id = object_json['id']
                student_json = requests.get(REST_API + '/student/%d' % student_id).json()

                # if student_json['check_in'] != 0:
                #     res['status'] = 1
                #     res['msg'] = 'This student has already checked in!'
                # else:
                student_list.append(student_json)

        for student_json in student_list:
            student_json['check_in'] = guardian_id
            requests.put(REST_API + '/student/%d' % student_id, json=student_json)
        res['msg'] = 'Successfully pre-check in student!'

    return jsonify(res)


@app.route('/preCheckOut', methods=['GET', 'POST'])
def preCheckOut():
    session['login'] = True
    session['user'] = 'guardian'
    session['guardian_id'] = 1
    session['family_id'] = 1

    res = deepcopy(RES_TEMPLATE)

    if request.method == 'GET':
        # a relation object with repeat guardians and students
        family_json = requests.get(REST_API + '/family/%d' % session['family_id']).json()   
        # filter repeat to be unique
        guardian_id_set, student_id_set = set(), set() 
        # list of json objects
        guardian_list, student_list = [], []

        for family in family_json:
            if family['guardian_id'] not in guardian_id_set:
                guardian_json = requests.get(REST_API + '/guardian/%d' % family['guardian_id']).json()
                guardian_list.append({
                    'guardian_id': guardian_json['id'],
                    'fname': guardian_json['fname'],
                    'lname': guardian_json['lname'],
                    'relationship': guardian_json['relationship']
                })
                guardian_id_set.add(family['guardian_id'])

            if family['student_id'] not in student_id_set:
                student_json = requests.get(REST_API + '/student/%d' % family['student_id']).json()
                if student_json.get('check_in') and student_json.get('check_in', 0) != 0:
                    student_list.append({
                        'student_id': student_json['id'],
                        'fname': student_json['fname'],
                        'lname': student_json['lname'],
                    })
                    student_id_set.add(family['student_id'])

        res['data']['guardian'] = guardian_list
        res['data']['student'] = student_list
        res['msg'] = 'Successfully get guardians and students!'
    else:   # POST
        guardian_id = 0
        student_list = []
        for object_json in request.json.get('items'):
            if object_json['object'] == 'guardian':  # selected guardian
                guardian_id = int(request.json.get('id'))
            else:
                student_id = object_json['id']
                student_json = requests.get(REST_API + '/student/%d' % student_id).json()

                student_json['check_in'] = 0
                student_list.append(student_json)

        for student_json in student_list:
            student_json['check_out'] = guardian_id
            requests.put(REST_API + '/student/%d' % student_id, json=student_json)
        res['msg'] = 'Successfully pre-check out student!'

    return jsonify(res)


@app.route('/checkIn', methods=['GET', 'POST'])
def checkIn():
    res = deepcopy(RES_TEMPLATE)
    barcode = ''
    if request.method == 'POST':
        barcode = request.json['barcode']
        query_res = requests.get(REST_API + '/student/barcode/' + barcode)
        if query_res.status_code != 200:
            res['status'] = 1
            res['msg'] = "Barcode doesn't match!"
        else:
            student_json = query_res.json()
            if student_json['check_in'] == 0:
                res['status'] = 1
                res['msg'] = "Student has not been pre-checked in!"
            else:
                student_json['check_in_time'] = datetime.datetime.now().timestamp
                requests.put(REST_API + 'student/%d' % student_json['id'], json=student_json)
                res['msg'] = "Successfully check in!"
        return jsonify(res)

    return render_template('flask_check_in_out/check_in.html')


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    res = deepcopy(RES_TEMPLATE)
    barcode = ''
    if request.method == 'POST':
        barcode = request.json['barcode']
        query_req = requests.get(REST_API + 'student/barcode/' + barcode)
        if query_req.status_code == 404:
            res['status'] = 1
            res['msg'] = "Barcode doesn't match!"
        else:
            student_json = query_req.json()
            if student_json['check_out'] == 0:
                res['status'] = 1
                res['msg'] = "Student has not been pre-checked out!"
            else:
                student_json['check_out_time'] = datetime.datetime.now().timestamp
                requests.put(REST_API + 'student/%d' % student_json['id'], json=student_json)
                res['msg'] = "Successfully check out!"
            return jsonify(res)
    return render_template('flask_check_in_out/check_out.html')


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


@app.route('/checkIn2', methods=['GET', 'POST'])
def checkIn2():
    return render_template('flask_check_in_out/check_in2.html')


@app.route('/checkInSuccess', methods=['GET', 'POST'])
def checkInSuccess():
    return render_template('flask_check_in_out/s_check_in.html')


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
