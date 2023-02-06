import random
# import MySQLdb.cursors
# from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
# import pymysql
import os
from flask_cors import CORS
import requests
from routing_config import REST_API
from copy import deepcopy
import datetime

# pymysql.install_as_MySQLdb()

template_dir = os.path.abspath('../../AttendancePro')
static_dir = os.path.abspath('../../AttendancePro/sdk')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = '123456'

CORS(app, resources=r'/*', supports_credentials=True)

AMIS_RES_TEMPLATE = {
    'status': 0,
    'msg': None,
    'data': {}
}

COOKIE_EXPIRE_TIME = int((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp())

'''
COOKIES: {
    'login': ('1', '0'),
    'user_group': ('guardian','admin'),
    'user_id': user_id,
    'family_id': family_id,
    'classes_id': classes_id
} (all str)
'''

@app.route('/guardianSignUp', methods=['POST'])
def guardianSignUp():
    res = deepcopy(AMIS_RES_TEMPLATE)
    if request.json['password'] != request.json['confirm_password']:
        res['status'] = 1
        res['msg'] = "Confirmed password doesn't match!"
        return jsonify(res)
    
    guardian_json = {'phone': request.json['phone'], 'pwd': request.json['password']}
    if requests.get(REST_API + '/guardian/phone/%s' % guardian_json['phone']).status_code == 200:
        # duplicate phone number
        res['status'] = 1
        res['msg'] = 'Account already existed! Please use the phone number to login.'
        return jsonify(res)
    else:
        requests.post(REST_API + '/guardian', json=guardian_json)
        res['msg'] = 'Successfully create an account! Please use your account to login.'
        res = jsonify(res)
        res.set_cookie('phone', guardian_json['phone'])
        return res


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'login' in request.cookies.keys() and request.cookies['login'] == "1":
        if request.cookies.get('user_group') == 'guardian':
            if not request.cookies.get('family_id'):    # guardian has not enroll family yet
                return redirect('enrollPage')
            else:
                return render_template('flask_templates/guardian/index.html')
        else:
            return render_template('flask_templates/admin/index.html')
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in request.cookies.keys() and request.cookies['login'] == "1":
            return redirect(url_for('index'))
        else:
            return render_template('flask_templates/general/sign_in.html')
    else:   # method == POST
        res_json = deepcopy(AMIS_RES_TEMPLATE)
        if 'phone' in request.json and 'pwd' in request.json:
            phone = request.json['phone']
            pwd = request.json['pwd']

            guardian_query = requests.get(REST_API + '/guardian/phone/' + phone)
            admin_query = requests.get(REST_API + '/admin/phone/' + phone)

            if guardian_query.status_code == 200:
                if 'phone' in guardian_query.json().keys() and guardian_query.json()['pwd'] == pwd:
                    res_json['data']['object'] = 'guardian'
                    res_json['msg'] = 'Logged in successfully!'
                    res = jsonify(res_json)

                    res.set_cookie(key='login', value="1", expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='user_id', value=str(guardian_query.json()['id']), expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='user_group', value='guardian', expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='phone', value=phone, expires=COOKIE_EXPIRE_TIME)

                    family_json = requests.get(REST_API + '/family/guardian/%d' % guardian_query.json()['id']).json()
                    if len(family_json) != 0:
                        family_id = family_json[0]['id']
                        res.set_cookie(key='family_id', value=str(family_id), expires=COOKIE_EXPIRE_TIME)
                    
                    return res
                else:
                    res_json['status'] = 1
                    res_json['msg'] = 'Incorrect phone number or password!'
            elif admin_query.status_code == 200:
                if 'phone' in admin_query.json().keys() and admin_query.json()['pwd'] == pwd:
                    res_json['data']['object'] = 'admin'
                    res_json['msg'] = 'Logged in successfully!'
                    res = jsonify(res_json)

                    classes_id = requests.get(REST_API + '/classes/admin/%d' % admin_query.json()['id']).json()[0]['id']
                    res.set_cookie(key='login', value="1", expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='user_id', value=str(admin_query.json()['id']), expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='classes_id', value=str(classes_id), expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='user_group', value='admin', expires=COOKIE_EXPIRE_TIME)
                    return res
                else:
                    res_json['status'] = 1
                    res_json['msg'] = 'Incorrect phone number or password!'
            else:
                res_json['status'] = 1
                res_json['msg'] = 'Incorrect phone number or password!'
        else:
            res_json['status'] = 1
            res_json['msg'] = 'Please input phone number and password!'

        return jsonify(res_json)


@app.route('/logout', methods=['POST'])
def logout():
    res = deepcopy(AMIS_RES_TEMPLATE)
    res['msg'] = 'Successfully logout!'
    res = jsonify(res)
    res.delete_cookie('login')
    res.delete_cookie('user_id')
    res.delete_cookie('family_id')
    res.delete_cookie('classes_id')
    res.delete_cookie('user_group')
    res.delete_cookie('phone')
    return res


@app.route('/enrollPage', methods=['GET'])
def enrollPage():
    return render_template('flask_templates/general/form.html')


@app.route('/enrollFamily', methods=['POST'])
def enrollFamily():
    res = deepcopy(AMIS_RES_TEMPLATE)

    # TODO: fault tolerant: what if user exit during enrollment process
    # guardian
    guardian_list = []
    for i, guardian in enumerate(request.json['guardians']):
        guardian_json = {}
        guardian_json['fname'] = guardian['fname']
        guardian_json['lname'] = guardian['lname']
        guardian_json['check_in_method'] = guardian['method']
        guardian_json['phone'] = guardian['phone']  # allow non-primary guardians to have their phone numbers
        guardian_json['email'] = guardian.get('email')
        guardian_json['relationship'] = guardian.get('relationship')
        guardian_json['barcode'] = guardian['fname'][0].upper() + guardian['lname'][0].upper() + generate_random_str(5)

        if i == 0:
            guardian_res = requests.put(
                REST_API + '/guardian/%s' % request.cookies['user_id'], json=guardian_json)
        else:
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
        student_json['barcode'] = student['fname'][0].upper() + student['lname'][0].upper() + generate_random_str(5)

        programs = ['sunday_school', 'cm_lounge', 'kid_choir',
                    'u3_friday', 'friday_lounge', 'friday_night']
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

    familyInfo_json['pay'] = request.json.get('pay')
    familyInfo_json['checkbox'] = request.json.get('checkbox')

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

    res['msg'] = 'Successfully enrolled family!'
    res = jsonify(res)
    res.set_cookie(key='family_id', value=str(family_json['id']))    # add id cookie for later checkings
    return res


@app.route('/adminManagePage', methods=['GET'])
def adminManagePage():
    return render_template('flask_templates/admin/management.html')


@app.route('/adminManage/<object>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def adminManage(object):
    res = {
        'status': 0,
        'msg': None,
        'data': {
            'items': [],
            'hasNext': False
        }
    }
    if request.method == 'GET':
        object_json = requests.get(REST_API + '/' + object).json()
        res['data']['items'] = object_json
        res['msg'] = 'Successfully get data!'
    elif request.method == 'PUT' or request.method == 'POST':
        object_json = dict(request.json)
        if request.method == 'PUT':
            requests.put(REST_API + '/' + object + '/' + str(object_json['id']), json=object_json)
            res['msg'] = 'Successfully update!'
        else:
            requests.post(REST_API + '/' + object, json=object_json)
            res['msg'] = 'Successfully add!'
    else:   # DELETE
        requests.delete(REST_API + '/' + object + '/' + request.args.get('id'))
        res['msg'] = 'Successfully delete!'
    

    if not res['msg']:
        res['msg'] = 'Error happened.'
        res['status'] = 400

    return jsonify(res)


@app.route('/userManagePage', methods=['GET'])
def userManagePage():
    return render_template('flask_templates/guardian/management.html')


@app.route('/userManage', methods=['GET', 'POST', 'PUT', 'DELETE'])
def userManage():
    res = {
        'status': 0,
        'msg': None,
        'data': {
            'items': [],
            'hasNext': False
        }
    }

    if request.method == 'GET':
        family_id = int(request.cookies.get('family_id'))
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
    else:
        object = request.args.get('object')
        if request.method == 'POST':
            object_json = request.json
            # check duplicate guardian
            if object == 'guardian' and \
                    requests.get(REST_API + '/phone/%s' % object_json['phone']).status_code == 200:
                res['status'] = 1
                res['msg'] = 'Guardian phone number cannot be duplicated!'
            else:
                if object == 'guardian':
                    object_json['pwd'] = object_json['phone']
                else:   # object == student
                    object_json['barcode'] = object_json['fname'][0].upper() + object_json['lname'][0].upper() + generate_random_str(5)
                    programs = ['sunday_school', 'cm_lounge', 'kid_choir',
                                'u3_friday', 'friday_lounge', 'friday_night']
                    for i, program in enumerate(programs):
                        object_json[program] = object_json['program'][0][i]['checked']
                
                object_id = requests.post(REST_API + '/%s' % object, json=object_json).json()['id']
                
                family_id = int(request.cookies.get('family_id'))
                family_json = requests.get(REST_API + '/family/%d' % family_id).json()
                guardian_ids, student_ids = set(), set()
                for family in family_json:
                    guardian_ids.add(family['guardian_id'])
                    student_ids.add(family['student_id'])

                if object == 'guardian':
                    for student_id in student_ids:
                        new_family_json = {'id': family_id, 'guardian_id': object_id, 'student_id': student_id}
                        requests.post(REST_API + '/family', json=new_family_json)
                else:   # object == student
                    for guardian_id in guardian_ids:
                        new_family_json = {'id': family_id, 'guardian_id': guardian_id, 'student_id': object_id}
                        requests.post(REST_API + '/family', json=new_family_json)
            
                res['msg'] = 'Successfully add new %s!' % object

        elif request.method == 'PUT':
            object_id = request.args.get('id')
            object_json = request.json

            if object == 'student':
                object_json['barcode'] = object_json['fname'][0].upper() + object_json['lname'][0].upper() + generate_random_str(5)
                programs = ['sunday_school', 'cm_lounge', 'kid_choir',
                            'u3_friday', 'friday_lounge', 'friday_night']
                for i, program in enumerate(programs):
                    object_json[program] = object_json['program'][0][i]['checked']

            requests.put(REST_API + '/%s/%s' % (object, object_id), json=object_json)
            res['msg'] = 'Successfully update %s!' % object
        else:   # DELETE
            object_id = request.args.get('id')
            requests.delete(REST_API + '/family/%s/%s' % (object, object_id))
            if object == 'student' and requests.get(REST_API + '/classes/%s/%s' % (object, object_id)).status_code == 200:
                requests.delete(REST_API + '/classes/%s/%s' % (object, object_id))
            requests.delete(REST_API + '/%s/%s' % (object, object_id))
            res['msg'] = 'Successfully delete %s!' % object
    
    return jsonify(res)


@app.route('/preCheckInPage', methods=['GET'])
def preCheckInPage():
    return render_template('flask_templates/guardian/pre_check_in.html')


@app.route('/preCheckIn', methods=['GET', 'POST'])
def preCheckIn():
    res = deepcopy(AMIS_RES_TEMPLATE)

    if request.method == 'GET':
        family_id = int(request.cookies.get('family_id'))
        # a relation object with repeat guardians and students
        family_json = requests.get(REST_API + '/family/%d' % family_id).json()
        # filter repeat to be unique
        guardian_id_set, student_id_set = set(), set()
        # list of json objects
        object_list = []

        for family in family_json:
            if family['guardian_id'] not in guardian_id_set:    # filter repeat
                guardian_json = requests.get(REST_API + '/guardian/%d' % family['guardian_id']).json()
                object_list.append({
                    'object': 'guardian',
                    'id': guardian_json['id'],
                    'fname': guardian_json['fname'],
                    'lname': guardian_json['lname']
                })
                guardian_id_set.add(family['guardian_id'])

            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(REST_API + '/student/%d' % family['student_id']).json()
                if student_json.get('check_in', 0) == 0:
                    object_list.append({
                        'object': 'student',
                        'id': student_json['id'],
                        'fname': student_json['fname'],
                        'lname': student_json['lname']
                    })
                    student_id_set.add(family['student_id'])
        object_list = sorted(object_list, key=lambda d: d['object'])
        res['data']['items'] = object_list
        res['msg'] = 'Successfully get guardians and students!'
    else:   # POST
        guardian_id = 0
        student_list = []
        for object_json in request.json.get('items'):
            if object_json['object'] == 'guardian':  # selected guardian
                guardian_id = object_json['id']
            else:
                student_id = object_json['id']
                student_json = requests.get(REST_API + '/student/%d' % student_id).json()

                # if student_json['check_in'] != 0:
                #     res['status'] = 1
                #     res['msg'] = 'This student has already checked in!'
                # else:
                student_list.append(student_json)

        for student_json in student_list:
            student_json['check_out'] = 0
            student_json['check_in'] = guardian_id
            requests.put(REST_API + '/student/%d' % student_id, json=student_json)
        res['msg'] = 'Successfully pre-check in student!'

    return jsonify(res)


@app.route('/preCheckOutPage', methods=['GET'])
def preCheckOutPage():
    return render_template('flask_templates/guardian/pre_check_out.html')


@app.route('/preCheckOut', methods=['GET', 'POST'])
def preCheckOut():
    res = deepcopy(AMIS_RES_TEMPLATE)

    if request.method == 'GET':
        family_id = int(request.cookies.get('family_id'))
        # a relation object with repeat guardians and students
        family_json = requests.get(REST_API + '/family/%d' % family_id).json()
        # filter repeat to be unique
        guardian_id_set, student_id_set = set(), set()
        # list of json objects
        object_list = []

        for family in family_json:
            if family['guardian_id'] not in guardian_id_set:    # filter repeat
                guardian_json = requests.get(REST_API + '/guardian/%d' % family['guardian_id']).json()
                object_list.append({
                    'object': 'guardian',
                    'id': guardian_json['id'],
                    'fname': guardian_json['fname'],
                    'lname': guardian_json['lname']
                })
                guardian_id_set.add(family['guardian_id'])

            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(REST_API + '/student/%d' % family['student_id']).json()
                if student_json.get('check_in', 0) != 0:
                    object_list.append({
                        'object': 'student',
                        'id': student_json['id'],
                        'fname': student_json['fname'],
                        'lname': student_json['lname']
                    })
                    student_id_set.add(family['student_id'])
        object_list = sorted(object_list, key=lambda d: d['object'])
        res['data']['items'] = object_list
        res['msg'] = 'Successfully get guardians and students!'
    else:   # POST
        guardian_id = 0
        student_list = []
        for object_json in request.json.get('items'):
            if object_json['object'] == 'guardian':  # selected guardian
                guardian_id = object_json['id']
            else:
                student_id = object_json['id']
                student_json = requests.get(REST_API + '/student/%d' % student_id).json()
                student_list.append(student_json)

        for student_json in student_list:
            student_json['check_in'] = 0
            student_json['check_out'] = guardian_id
            requests.put(REST_API + '/student/%d' % student_id, json=student_json)
        res['msg'] = 'Successfully pre-check out student!'

    return jsonify(res)


@app.route('/checkInPage', methods=['GET'])
def checkInPage():
    return render_template('flask_templates/admin/check_in_barcode.html')


@app.route('/checkIn', methods=['POST'])
def checkIn():
    res = deepcopy(AMIS_RES_TEMPLATE)
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
                student_json['check_out_time'] = 0  # once checked in, set last check out time to 0
                student_json['check_in_time'] = int(datetime.datetime.now().timestamp())
                requests.put(REST_API + '/student/%d' % student_json['id'], json=student_json)
                res['msg'] = "Successfully check in!"
        return jsonify(res)

    return render_template('flask_templates/admin/check_in.html')


@app.route('/checkOutPage', methods=['GET'])
def checkOutPage():
    return render_template('flask_templates/admin/check_out_barcode.html')


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    res = deepcopy(AMIS_RES_TEMPLATE)
    if request.method == 'POST':
        if len(request.json.keys()) == 1:
            guardian_barcode = request.json.get('barcode')
            guardian_query = requests.get(REST_API + '/guardian/barcode/' + guardian_barcode)
            if guardian_query.status_code == 404:
                res['status'] = 1
                res['msg'] = "Barcode doesn't match!"
            else:
                guardian_id = guardian_query.json().get('id')
                family_id = requests.get(REST_API + '/family/guardian/%d' % guardian_id).json()[0].get('guardian_id')
                res['msg'] = 'Verified guardian barcode!'
                res = jsonify(res)
                res.set_cookie(key='family_id', value=str(family_id), expires=COOKIE_EXPIRE_TIME)
                return res
        else:
            student_barcode = request.json['barcode']
            student_query = requests.get(REST_API + '/student/barcode/' + student_barcode)
            if student_query.status_code == 404:
                res['status'] = 1
                res['msg'] = "Barcode doesn't match!"
            else:
                student_json = student_query.json()
                if student_json['check_out'] == 0:
                    res['status'] = 1
                    res['msg'] = "Student has not been pre-checked out!"
                else:
                    student_json['check_in_time'] = 0  #  once checked out, set last check in time to 0
                    student_json['check_out_time'] = int(datetime.datetime.now().timestamp())
                    requests.put(REST_API + '/student/%d' % student_json['id'], json=student_json)
                    res['data']['key'] = student_json['id']
                    res['msg'] = "Successfully check out!"
    else:   # GET
        family_id = int(request.cookies.get('family_id'))
        family_json = requests.get(REST_API + '/family/%d' % family_id).json()
        # filter repeat to be unique
        student_id_set = set()
        # list of json objects
        student_info_list = []

        for family in family_json:
            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(REST_API + '/student/%d' % family['student_id']).json()
                if student_json['check_in'] == 0 and student_json['check_in_time'] != '0' and student_json['check_out'] != 0:
                    student_info_list.append({
                        'id': student_json['id'],
                        'fname': student_json['fname'],
                        'lname': student_json['lname']
                    })
                    student_id_set.add(family['student_id'])
        if len(student_info_list) > 0:
            res['data']['items'] = student_info_list
        else:
            res['status'] = 1
            res['msg'] = "No pre-checked out student!"

    return jsonify(res)


# @app.route('/firstTimeEnroll', methods=['GET', 'POST'])
# def firstTimeEnroll():
#     msg = ''
#     if request.method == 'GET':
#         return render_template('flask_templates/guardian/GuardianEnrollment.html', msg=msg)
#     else:
#         return render_template('flask_templates/StudentEnrollment.html', msg=msg)

@app.route('/msgBoardPage', methods=['GET'])
def msgBoardPage():
    user_group = request.cookies.get('user_group')
    if user_group == 'guardian':
        return render_template('flask_templates/guardian/communication.html')
    else:
        return render_template('flask_templates/admin/admin_communication.html')


@app.route('/msgBoard', methods=['GET', 'POST'])
def msgBoard():
    t = {
        "status": 0,
        "msg": None,
        "data": None
    }
    user_group = request.cookies.get('user_group')
    user_id = int(request.cookies.get('user_id'))
    
    if request.method == 'GET':
        if user_group == 'guardian':
            guardian_json = requests.get(REST_API + '/guardian/%d' % user_id).json()
            fname, lname = guardian_json['fname'], guardian_json['lname']
            
            msg_show = []
            msgBoard_json = requests.get(REST_API + '/msgBoard/guardian/%d' % user_id).json()
            for msg in msgBoard_json:
                if msg['sender_group'] == 'admin':
                    admin_json = requests.get(REST_API + '/admin/%d' % int(msg['sender_id'])).json()
                    msg_show.append({'id': msg['id'], 'fname': 'Admin - ' + admin_json['fname'], 'lname': admin_json['lname'],
                                    'msg': msg['content'], 'timestamp': msg['time']})
                else:
                    msg_show.append({'id': msg['id'], 'fname': fname, 'lname': lname,
                                    'msg': msg['content'], 'timestamp': msg['time']})

            t['data'] = {'items': msg_show}
            t["msg"] = "Successfully get historical messages!"
        else:   # admin
            admin_json = requests.get(REST_API + '/admin/%d' % user_id).json()
            fname, lname = admin_json['fname'], admin_json['lname']
            
            msg_show = []
            msgBoard_json = requests.get(REST_API + '/msgBoard/admin/%d' % user_id).json()
            for msg in msgBoard_json:
                if msg['sender_group'] == 'guardian':
                    guardian_json = requests.get(REST_API + '/guardian/%d' % int(msg['sender_id'])).json()
                    msg_show.append({'id': msg['id'], 'fname': 'Guardian - ' + guardian_json['fname'], 'lname': guardian_json['lname'],
                                    'msg': msg['content'], 'timestamp': msg['time'], 'read': 'Yes' if msg['been_read'] else 'No'})
                else:
                    msg_show.append({'id': msg['id'], 'fname': fname, 'lname': lname,
                                    'msg': msg['content'], 'timestamp': msg['time'], 'read': 'Yes' if msg['been_read'] else 'No'})

            t['data'] = {'items': msg_show}
            t["msg"] = "Successfully get historical messages!"
    else:   # POST
        if user_group == 'guardian':
            student_id_list = list(map(int, request.json.get('student_id').split(',')))
            for student_id in student_id_list:
                # query admin corresponding to student
                admin_id = requests.get(REST_API + '/classes/student/%d' % student_id).json()[0].get('admin_id')   
                msg_json = {'sender_id': user_id, 'receiver_id': admin_id, 'sender_group': user_group,
                            'about_student': student_id, 'content': request.json['msg'], 
                            'time': int(datetime.datetime.now().timestamp()), 'been_read': False}
                requests.post(REST_API + '/msgBoard', json=msg_json)
        else:   # admin send
            if 'reply_msg_id' in request.json.keys():
                reply_msg_id_list = list(map(int, request.json.get('reply_msg_id').split(',')))
                for reply_msg_id in reply_msg_id_list:
                    requests.put(REST_API + '/msgBoard/%d' % reply_msg_id, json={'been_read': True})

                    reply_msg_json = requests.get(REST_API + '/msgBoard/%d' % reply_msg_id).json()

                    student_id = reply_msg_json.get('about_student')
                    guardian_id = reply_msg_json.get('sender_id')

                    msg_json = {'sender_id': user_id, 'receiver_id': guardian_id, 'sender_group': user_group,
                                'about_student': student_id, 'content': request.json['msg'], 
                                'time': int(datetime.datetime.now().timestamp()), 'been_read': True}
                    requests.post(REST_API + '/msgBoard', json=msg_json)
            else:   # TODO: sending to multiple students, should specify which student related to
                student_id_list = list(map(int, request.json.get('student_id').split(',')))
                for student_id in student_id_list:
                    family_json = requests.get(REST_API + '/family/student/%d' % student_id).json()
                    for family in family_json:
                        msg_json = {'sender_id': user_id, 'receiver_id': family['guardian_id'], 'sender_group': user_group,
                                    'about_student': student_id, 'content': request.json['msg'], 
                                    'time': int(datetime.datetime.now().timestamp()), 'been_read': True}
                        requests.post(REST_API + '/msgBoard', json=msg_json)

        t["msg"] = "Successfully post message!"

    return jsonify(t)


@app.route('/studentBriefInfo', methods=['GET'])
def studentBriefInfo():
    res = deepcopy(AMIS_RES_TEMPLATE)
    if request.cookies.get('user_group') == 'guardian':
        family_id = int(request.cookies.get('family_id'))
        family_json = requests.get(REST_API + '/family/%d' % family_id).json()
        # filter repeat to be unique
        student_id_set = set()
        # list of json objects
        student_info_list = []

        for family in family_json:
            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(REST_API + '/student/%d' % family['student_id']).json()
                student_info_list.append({
                    'id': student_json['id'],
                    'fname': student_json['fname'],
                    'lname': student_json['lname']
                })
                student_id_set.add(family['student_id'])
        res['data']['items'] = student_info_list
    else:   # admin
        classes_id = request.cookies.get('classes_id')
        classes_json = requests.get(REST_API + '/classes/%s' % classes_id).json()
        # filter repeat to be unique
        student_id_set = set()
        # list of json objects
        student_info_list = []

        for classes in classes_json:
            if classes['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(REST_API + '/student/%d' % classes['student_id']).json()
                student_info_list.append({
                    'id': student_json['id'],
                    'fname': student_json['fname'],
                    'lname': student_json['lname'],
                    'classes_id': student_json['classes_id'],
                })
                student_id_set.add(classes['student_id'])
        res['data']['items'] = student_info_list
    return jsonify(res)


@app.route('/barcode/<object>', methods=['GET'])
def barcode(object):
    res = deepcopy(AMIS_RES_TEMPLATE)
    if object == 'guardian':
        guardian_id = int(request.cookies.get('user_id'))
        guardian_json = requests.get(REST_API + '/guardian/%d' % guardian_id).json()
        res['data']['barcode'] = guardian_json.get('barcode')
    elif object == 'student':
        student_id = int(request.args.get('id'))
        student_json = requests.get(REST_API + '/student/%d' % student_id).json()
        res['data']['barcode'] = student_json.get('barcode')

    return jsonify(res)


@app.route('/logPage', methods=['GET'])
def logPage():
    return render_template('flask_templates/admin/log.html')


@app.route('/log', methods=['OPTIONS', 'POST', 'PUT', 'DELETE'])
def log():
    pass


@app.route('/guestEnrollPage', methods=['GET'])
def guestEnrollPage():
    return render_template('flask_templates/scanner/guest_form.html')


@app.route('/guestEnroll', methods=['POST'])
def guestEnroll():
    # TODO: replicate check
    res = deepcopy(AMIS_RES_TEMPLATE)

    if request.method == 'POST':
        # guardian
        guardian_list = []
        for i, guardian in enumerate(request.json['guardians']):
            guardian_res = requests.post(REST_API + '/guardian', json=guardian)
            guardian_list.append(guardian_res.json())

        # student
        student_list = []
        for student in request.json['children']:
            student_res = requests.post(
                REST_API + '/student', json=student)
            student_list.append(student_res.json())

        # familyInfo
        familyInfo_json = {'is_guest': True}
        familyInfo_res = requests.post(REST_API + '/familyInfo', json=familyInfo_json)
        familyInfo_json = familyInfo_res.json()

        # family
        family_json = {}
        family_json['id'] = familyInfo_json['id']
        for guardian in guardian_list:
            for student in student_list:
                family_json['guardian_id'] = guardian['id']
                family_json['student_id'] = student['id']
                family_json['is_guest'] = True

                family_res = requests.post(
                    REST_API + '/family', json=family_json)
                family_json = family_res.json()

    res['msg'] = 'Successfully enrolled guest family!'
    return jsonify(res)


def generate_random_str(randomLength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(randomLength):
        random_str += base_str[random.randint(0, length)]
    return random_str


if __name__ == '__main__':
    app.run(port=5000)
    
