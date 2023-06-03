import random
# import MySQLdb.cursors
# from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, abort
# import pymysql
import os
from flask_cors import CORS
import requests
from routing_config import REST_API, DEFAULT_PWD
from copy import deepcopy
from flask_bcrypt import Bcrypt
import datetime

# pymysql.install_as_MySQLdb()

template_dir = os.path.abspath('../../AttendancePro')
static_dir = os.path.abspath('../../AttendancePro/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = '123456'

CORS(app, resources=r'/*', supports_credentials=True)

bcrypt = Bcrypt(app)

AMIS_RES_TEMPLATE = {
    'status': 0,
    'msg': None,
    'data': {}
}

COOKIE_EXPIRE_TIME = int(
    (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp())

'''
COOKIES: {
    'login': ('1', '0'),
    'user_group': ('guardian','scanner','teacher','admin'),
    'user_id': user_id,
    'family_id': family_id,
    'classes_id': classes_id,
    'fname': first_name,
    'lname': last_name
} (all str)
'''


@app.route('/guardianSignUp', methods=['POST'])
def guardianSignUp():
    res = deepcopy(AMIS_RES_TEMPLATE)

    guardian_json = {
        'phone': request.json['phone'], 'pwd': request.json['password']}
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
            return render_template('flask_templates/guardian/index.html')
        elif request.cookies.get('user_group') == 'scanner':
            return render_template('flask_templates/scanner/index.html')
        elif request.cookies.get('user_group') == 'teacher':
            return render_template('flask_templates/teacher/index.html')
        elif request.cookies.get('user_group') == 'admin':
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

            guardian_query = requests.get(
                REST_API + '/guardian/phone/' + phone)
            teacher_query = requests.get(REST_API + '/teacher/phone/' + phone)

            if guardian_query.status_code == 200:
                guardian_json = guardian_query.json()
                # if hash password is set, check it; otherwise check the plain text password
                if 'phone' in guardian_json.keys() and guardian_json['pwd'] == pwd and (not guardian_json['pwd_hash'] \
                        or (guardian_json['pwd_hash'] and bcrypt.check_password_hash(guardian_json['pwd_hash'], pwd))):
                    res_json['msg'] = 'Logged in successfully!'

                    if guardian_json['pwd'] == DEFAULT_PWD:
                        res_json['data'] = {'default_pwd': True}
                    res = jsonify(res_json)

                    res.set_cookie(key='login', value="1",
                                   expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='user_id', value=str(
                        guardian_json['id']), expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(
                        key='user_group', value='guardian', expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(key='phone', value=phone,
                                   expires=COOKIE_EXPIRE_TIME)

                    # first time register not input name yet
                    if guardian_json.get('fname'):
                        res.set_cookie(
                            key='fname', value=guardian_json['fname'], expires=COOKIE_EXPIRE_TIME)
                        res.set_cookie(
                            key='lname', value=guardian_json['lname'], expires=COOKIE_EXPIRE_TIME)
                    else:
                        res.set_cookie(key='fname', value='New',
                                       expires=COOKIE_EXPIRE_TIME)
                        res.set_cookie(key='lname', value='Guardian',
                                       expires=COOKIE_EXPIRE_TIME)

                    family_json = requests.get(
                        REST_API + '/family/guardian/%d' % guardian_json['id']).json()
                    if len(family_json) != 0:
                        family_id = family_json[0]['id']
                        res.set_cookie(key='family_id', value=str(
                            family_id), expires=COOKIE_EXPIRE_TIME)

                    return res
                else:
                    res_json['status'] = 1
                    res_json['msg'] = 'Incorrect phone number or password!'
            elif teacher_query.status_code == 200:
                teacher_json = teacher_query.json()
                # if hash password is set, check it; otherwise check the plain text password
                if 'phone' in teacher_json.keys() and (not teacher_json['pwd_hash'] \
                        or (teacher_json['pwd_hash'] and bcrypt.check_password_hash(teacher_json['pwd_hash'], pwd))):
                    res_json['msg'] = 'Logged in successfully!'
                    res = jsonify(res_json)
                    res.set_cookie(key='login', value="1",
                                   expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(
                        key='fname', value=teacher_json['fname'], expires=COOKIE_EXPIRE_TIME)
                    res.set_cookie(
                        key='lname', value=teacher_json['lname'], expires=COOKIE_EXPIRE_TIME)

                    # logged in as a scanner account
                    if teacher_json['privilege'] == 0:
                        res.set_cookie(
                            key='user_group', value='scanner', expires=COOKIE_EXPIRE_TIME)
                    else:
                        # logged in as a normal teacher
                        if teacher_json['privilege'] == 1:
                            res.set_cookie(
                                key='user_group', value='teacher', expires=COOKIE_EXPIRE_TIME)
                        elif teacher_json['privilege'] == 2:    # logged in as an admin
                            res.set_cookie(
                                key='user_group', value='admin', expires=COOKIE_EXPIRE_TIME)

                        classes_json = requests.get(
                            REST_API + '/classes/teacher/%d' % teacher_json['id']).json()
                        # teacher/admin has asscoiated classes
                        if classes_json and len(classes_json) > 0:
                            classes_id = classes_json[0]['id']
                            res.set_cookie(key='classes_id', value=str(
                                classes_id), expires=COOKIE_EXPIRE_TIME)
                        res.set_cookie(key='user_id', value=str(
                            teacher_json['id']), expires=COOKIE_EXPIRE_TIME)

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
    res.delete_cookie('fname')
    res.delete_cookie('lname')
    return res


@app.route('/enrollFamily', methods=['POST'])
def enrollFamily():
    res = deepcopy(AMIS_RES_TEMPLATE)

    # TODO: fault tolerant: what if user exit during enrollment process
    # guardian
    guardian_list = []
    for guardian in request.json['guardians']:
        guardian_res = requests.post(REST_API + '/guardian', json=guardian)
        guardian_list.append(guardian_res.json())

    # student
    student_list = []
    for student in request.json['students']:
        student['barcode'] = student['fname'][0].upper(
        ) + student['lname'][0].upper() + generate_random_str(5)

        student_res = requests.post(
            REST_API + '/student', json=student)
        student_list.append(student_res.json())

    # familyInfo
    familyInfo_res = requests.post(
        REST_API + '/familyInfo', json=request.json)
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
    # add id cookie for later checkings
    res.set_cookie(key='family_id', value=str(family_json['id']))
    return res


@app.route('/adminManagePage', methods=['GET'])
def adminManagePage():
    if request.cookies.get('user_group') != 'admin':
        abort(403)
    return render_template('flask_templates/admin/management.html')


@app.route('/adminManage/<object>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def adminManage(object):
    res = deepcopy(AMIS_RES_TEMPLATE)
    if object != 'classes':
        if request.method == 'GET':     # guardian / student / familyInfo / family / teacher
            object_json = requests.get(REST_API + '/' + object).json()

            if object == 'family':
                guardians_json = requests.get(REST_API + '/guardian').json()
                students_json = requests.get(REST_API + '/student').json()
                guardian_id_to_json = {guardian['id']: guardian for guardian in guardians_json}
                student_id_to_json = {student['id']: student for student in students_json}

                for i, family in enumerate(object_json):
                    guardian_json = guardian_id_to_json[family['guardian_id']]
                    student_json = student_id_to_json[family['student_id']]
                    object_json[i]['guardian_name'] = guardian_json['fname'] + \
                        ' ' + guardian_json['lname']
                    object_json[i]['guardian_phone'] = guardian_json['phone']
                    object_json[i]['guardian_email'] = guardian_json['email']
                    object_json[i]['guardian_relationship'] = guardian_json['relationship']
                    object_json[i]['student_name'] = student_json['fname'] + \
                        ' ' + student_json['lname']
                    
            if object == 'familyInfo':
                guardians_json = requests.get(REST_API + '/guardian').json()
                students_json = requests.get(REST_API + '/student').json()
                family_json = requests.get(REST_API + '/family').json()
                guardian_id_to_json = {guardian['id']: guardian for guardian in guardians_json}
                student_id_to_json = {student['id']: student for student in students_json}
            
                for i, _ in enumerate(object_json):
                    object_json[i]['guardian_names'], object_json[i]['student_names'] = set(), set()

                id_familyInfo = {familyInfo['id']: familyInfo for familyInfo in object_json}
                
                for family in family_json:
                    family_id = family['id']
                    guardian_json = guardian_id_to_json[family['guardian_id']]
                    student_json = student_id_to_json[family['student_id']]
                    guardian_name = guardian_json['fname'] + ' ' + guardian_json['lname']
                    student_name = student_json['fname'] + ' ' + student_json['lname']
                    id_familyInfo[family_id]['guardian_names'].add(guardian_name)
                    id_familyInfo[family_id]['student_names'].add(student_name)

                for id, _ in id_familyInfo.items():
                    id_familyInfo[id]['guardian_names'] = ', '.join(list(id_familyInfo[id]['guardian_names']))
                    id_familyInfo[id]['student_names'] = ', '.join(list(id_familyInfo[id]['student_names']))
                
                object_json = list(id_familyInfo.values())
            
            if object == 'student':
                teachers_json = requests.get(REST_API + '/teacher').json()
                classes_teacher_name = {}
                for teacher in teachers_json:
                    if teacher['classes_id'] not in classes_teacher_name:
                        classes_teacher_name[teacher['classes_id']] = []
                    classes_teacher_name[teacher['classes_id']].append(teacher['fname'] + ' ' + teacher['lname'])

                for i, student in enumerate(object_json):
                    if student['classes_id']:
                        object_json[i]['teacher_name'] = classes_teacher_name[student['classes_id']]
                
                object_json = sorted(object_json, key=lambda x: x['id'])
                object_json.pop(0)

            res['data']['items'] = object_json
            res['msg'] = 'Successfully get data!'
        elif request.method == 'PUT' or request.method == 'POST':
            if request.method == 'PUT':
                if object == 'student':
                    status = int(request.json.get('status'))
                    log_json = {
                        'student_id': int(request.args.get('id')),
                        'status': status,
                        'check_in_method': request.json.get('check_in_method'),
                        'check_by': 0,
                        'check_time': int(datetime.datetime.now().timestamp())
                    }
                    requests.post(REST_API + '/log', json=log_json)

                requests.put(REST_API + '/' + object + '/' +
                             request.args.get('id'), json=request.json)
                res['msg'] = 'Successfully update!'

            elif request.method == 'POST':
                # TODO: when add guardian, required to input 'is_primary'
                requests.post(REST_API + '/' + object, json=request.json)
                res['msg'] = 'Successfully add new %s!' % object
        elif request.method == 'DELETE':
            if object == 'guardian' or object == 'student':
                requests.delete(REST_API + '/family/' +
                                object + '/' + request.args.get('id'))
                requests.delete(REST_API + '/log/' + object +
                                '/' + request.args.get('id'))
            if object == 'teacher' or object == 'student':
                requests.delete(REST_API + '/classes/' +
                                object + '/' + request.args.get('id'))
            if object == 'familyInfo':
                family_json = requests.get(
                    REST_API + '/family/' + request.args.get('id')).json()

                guardian_id_set = {family['guardian_id']
                                   for family in family_json}
                student_id_set = {family['student_id']
                                  for family in family_json}

                if family_json:
                    requests.delete(REST_API + '/family/%d' %
                                    family_json[0].get('id'))

                    for guardian_id in guardian_id_set:
                        requests.delete(REST_API + '/guardian/%d' % guardian_id)
                        requests.delete(
                            REST_API + '/log/guardian/%d' % guardian_id)
                    for student_id in student_id_set:
                        requests.delete(REST_API + '/student/%d' % student_id)
                        requests.delete(REST_API + '/log/student/%d' % student_id)

            requests.delete(REST_API + '/' + object +
                            '/' + request.args.get('id'))
            res['msg'] = 'Successfully delete!'

    elif object == "classes":
        if request.method == 'GET':
            classes_json = requests.get(REST_API + '/' + object).json()
            classes_id_set = sorted({classes['id']
                                    for classes in classes_json})
            res['data']['options'] = [
                {"label": classes_id, "value": classes_id} for classes_id in classes_id_set]
            res['msg'] = 'Successfully get data!'
        elif request.method == 'PUT' or request.method == 'POST':
            if request.method == 'PUT':
                if request.json['operation'] == 'add':
                    # check if selected students already belong any class
                    for selected_student_classes in request.json['classes_id_list']:
                        if selected_student_classes:
                            res['status'] = 1
                            res['msg'] = 'To add student to new class, must drop them from the current class. \
                                          Please make sure selected students not belong to any class.'
                            return jsonify(res)
                    classes_id = request.json['classes_id']
                    teacher_id = requests.get(
                        REST_API + '/teacher/classes/%s' % classes_id).json()['id']
                    for student_id in request.json['student_id_list']:
                        requests.put(REST_API + '/student/%d' %
                                     student_id, json={'classes_id': classes_id})
                        requests.post(REST_API + '/classes', json={'id': classes_id, 'teacher_id': teacher_id,
                                                                   'student_id': student_id})
                elif request.json['operation'] == 'drop':
                    for student in request.json['students']:
                        # check if selected students belong to any class
                        if student['classes_id']:
                            student_id = student['id']
                            classes_id = student['classes_id']
                            teacher_id = requests.get(
                                REST_API + '/teacher/classes/%s' % classes_id).json()['id']
                            requests.put(REST_API + '/student/%s' %
                                         student_id, json={'classes_id': None})
                            requests.delete(REST_API + '/classes/%s/%s/%s' %
                                            (classes_id, teacher_id, student_id))

                res['msg'] = 'Successfully update!'

            elif request.method == 'POST':
                classes_json = dict(request.json)

                # TODO: classes page should display corresponding teacher
                classes_json['id'] = classes_json.pop('classes_id')
                classes_json['student_id'] = -1

                teacher_name = classes_json.pop('name').split(' ')
                if len(teacher_name) != 2:
                    res['status'] = 1
                    res['msg'] = "Please correctly input teacher's first and last name, splited by one space."
                    return jsonify(res)
                teacher_query = requests.get(
                    REST_API + '/teacher/name/%s/%s' % tuple(teacher_name))
                if teacher_query.status_code == 200:  # create new classes
                    teacher_id = int(teacher_query.json()['id'])
                    # TODO: filter repeated classes
                    classes_json['teacher_id'] = teacher_id
                    requests.put(REST_API + '/teacher/%d' % teacher_id,
                                 json={'classes_id': classes_json['id']})
                    requests.post(REST_API + '/classes', json=classes_json)
                    res['msg'] = 'Successfully add new class!'
                else:
                    res['status'] = 1
                    res['msg'] = 'No matched teacher found. Please check teacher name.'
                    return jsonify(res)
        elif request.method == 'DELETE':
            classes_json = requests.get(
                REST_API + '/classes/%s' % request.args.get('id')).json()
            if len(classes_json) > 1 or int(classes_json[0]['student_id']) != -1:
                res['status'] = 1
                res['msg'] = 'Please drop all students from the class before delete!'
            else:
                requests.delete(REST_API + '/classes/%s' %
                                request.args.get('id'))
                res['msg'] = 'Successfully delete!'

    if not res['msg']:
        res['msg'] = 'Error happened.'
        res['status'] = 400

    return jsonify(res)


@app.route('/userManagePage', methods=['GET'])
def userManagePage():
    if request.cookies.get('user_group') != 'guardian':
        abort(403)
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

        familyInfo_json = requests.get(
            REST_API + '/familyInfo/%d' % family_id).json()
        familyInfo_json['object'] = 'familyInfo'
        res['data']['items'].append(familyInfo_json)
        for guardian_id in guardian_ids:
            guardian_json = requests.get(
                REST_API + '/guardian/%d' % guardian_id).json()
            guardian_json['object'] = 'guardian'
            res['data']['items'].append(guardian_json)
        for student_id in student_ids:
            student_json = requests.get(
                REST_API + '/student/%d' % student_id).json()
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
                if object == 'student':
                    object_json['barcode'] = object_json['fname'][0].upper(
                    ) + object_json['lname'][0].upper() + generate_random_str(5)

                object_id = requests.post(
                    REST_API + '/%s' % object, json=object_json).json()['id']

                family_id = int(request.cookies.get('family_id'))
                family_json = requests.get(
                    REST_API + '/family/%d' % family_id).json()

                guardian_ids, student_ids = set(), set()
                for family in family_json:
                    guardian_ids.add(family['guardian_id'])
                    student_ids.add(family['student_id'])

                if object == 'guardian':
                    for student_id in student_ids:
                        new_family_json = {
                            'id': family_id, 'guardian_id': object_id, 'student_id': student_id}
                        requests.post(REST_API + '/family',
                                      json=new_family_json)
                else:   # object == student
                    for guardian_id in guardian_ids:
                        new_family_json = {
                            'id': family_id, 'guardian_id': guardian_id, 'student_id': object_id}
                        requests.post(REST_API + '/family',
                                      json=new_family_json)

                res['msg'] = 'Successfully add new %s!' % object

        elif request.method == 'PUT':
            object_id = request.args.get('id')
            object_json = request.json

            if object == 'student':
                # TODO: notice, when edit student, a new barcode will be generated and need to reprint.
                object_json['barcode'] = object_json['fname'][0].upper(
                ) + object_json['lname'][0].upper() + generate_random_str(5)

            # change password
            elif 'new_pwd' in object_json:
                if object == 'admin' or object == 'scanner':
                    object = 'teacher'
                query_res = requests.get(
                    REST_API + '/%s/%s' % (object, object_id)).json()

                if query_res['pwd'] != object_json['current_pwd']:
                    res['status'] = 1
                    res['msg'] = 'Current password is incorrect!'
                    return jsonify(res)

                object_json['pwd'] = object_json['new_pwd']
                requests.put(REST_API + '/%s/%s' %
                             (object, object_id), json=object_json)

                res['msg'] = 'Successfully change password! Please login with new password next time.'
                return jsonify(res)

            requests.put(REST_API + '/' + object + '/' +
                         object_id, json=request.json)

            res['msg'] = 'Successfully update %s!' % object

        else:   # DELETE
            object_id = request.args.get('id')
            requests.delete(REST_API + '/family/%s/%s' % (object, object_id))
            if object == 'student' and requests.get(REST_API + '/classes/%s/%s' % (object, object_id)).status_code == 200:
                requests.delete(REST_API + '/classes/%s/%s' %
                                (object, object_id))
            requests.delete(REST_API + '/%s/%s' % (object, object_id))
            res['msg'] = 'Successfully delete %s!' % object

    return jsonify(res)


@app.route('/preCheckInPage', methods=['GET'])
def preCheckInPage():
    if request.cookies.get('user_group') != 'guardian':
        abort(403)
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
        family_list = []
          
        for family in family_json:
            if family['guardian_id'] not in guardian_id_set:    # filter repeat
                guardian_json = requests.get(
                    REST_API + '/guardian/%d' % family['guardian_id']).json()
                family_list.append({
                    'object': 'guardian',
                    'id': guardian_json['id'],
                    'fname': guardian_json['fname'],
                    'lname': guardian_json['lname']
                })
                guardian_id_set.add(family['guardian_id'])

            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(
                    REST_API + '/student/%d' % family['student_id']).json()

                if int(student_json['status']) == 0:
                    family_list.append({
                        'object': 'student',
                        'id': student_json['id'],
                        'fname': student_json['fname'],
                        'lname': student_json['lname']
                    })
                    student_id_set.add(family['student_id'])

        family_list = sorted(family_list, key=lambda d: d['object'])
        res['data']['items'] = family_list
        res['msg'] = 'Successfully get guardians and students!'
    elif request.method == 'POST':
        guardian_id = 0
        student_list = []
        for object_json in request.json.get('items'):
            if object_json['object'] == 'guardian':  # selected guardian
                guardian_id = object_json['id']
            else:
                student_id = object_json['id']
                student_json = requests.get(
                    REST_API + '/student/%d' % student_id).json()
                student_list.append(student_json)

        for student_json in student_list:
            log_json = {
                'student_id': student_json['id'],
                'status': 1,
                'check_in_method': student_json['check_in_method'],
                'check_by': guardian_id,
                'check_time': int(datetime.datetime.now().timestamp())
            }
            student_json['status'] = 1
            requests.post(REST_API + '/log', json=log_json)
            requests.put(REST_API + '/student/%s' % student_json['id'], json=student_json)

        # generate barcode for all guardians
        barcode = request.cookies.get('fname')[0].upper() + \
                  request.cookies.get('lname')[0].upper() + \
                  generate_random_str(5)
        family_id = int(request.cookies.get('family_id'))
        family_json = requests.get(REST_API + '/family/%d' % family_id).json()
        for family in family_json:
            requests.put(REST_API + '/guardian/%d' % family['guardian_id'],
                         json={'barcode': barcode})

        res['msg'] = 'Successfully pre-check in student!'

    return jsonify(res)


@app.route('/checkInPage', methods=['GET'])
def checkInPage():
    if request.cookies.get('user_group') not in {'admin', 'teacher'}:
        abort(403)
    return render_template('flask_templates/teacher/check_in_barcode.html')


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
            if int(student_json['status']) != 1:
                res['status'] = 1
                res['msg'] = "Student is not on pre-checked in status!"
            else:
                last_log_json = requests.get(
                    REST_API + '/log/student/%s' % student_json['id']).json()
                last_log_json = sorted(last_log_json, key=lambda d: d['id'])[-1]
                check_by = int(last_log_json['check_by'])

                new_log_json = {
                    'student_id': student_json['id'],
                    'status': 2,
                    'check_in_method': student_json['check_in_method'],
                    'check_by': check_by,
                    'check_time': int(datetime.datetime.now().timestamp()),
                }

                student_json['status'] = 2                
                res['msg'] = "Successfully check in!"

                requests.post(REST_API + '/log', json=new_log_json)
                requests.put(REST_API + '/student/%s' % student_json['id'], json=student_json)
        return jsonify(res)

    return render_template('flask_templates/teacher/check_in.html')


@app.route('/checkOutPage', methods=['GET'])
def checkOutPage():
    if request.cookies.get('user_group') not in {'admin', 'teacher'}:
        abort(403)
    return render_template('flask_templates/teacher/check_out_barcode.html')


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    res = deepcopy(AMIS_RES_TEMPLATE)
    if request.method == 'POST':
        if not request.json.get('student_barcode'):  # scanned guardian barcode
            guardian_barcode = request.json.get('guardian_barcode')
            guardian_query = requests.get(
                REST_API + '/guardian/barcode/' + guardian_barcode)
            if guardian_query.status_code == 404:
                res['status'] = 1
                res['msg'] = "Barcode doesn't match!"
            else:
                guardian_id = guardian_query.json().get('id')
                family_id = requests.get(
                    REST_API + '/family/guardian/%d' % guardian_id).json()[0].get('id')
                res['msg'] = 'Verified guardian barcode!'
                res = jsonify(res)
                res.set_cookie(key='guardian_id', value=str(
                    guardian_id), expires=COOKIE_EXPIRE_TIME)
                res.set_cookie(key='family_id', value=str(
                    family_id), expires=COOKIE_EXPIRE_TIME)
                return res
        else:
            student_barcode = request.json['student_barcode']
            student_query = requests.get(
                REST_API + '/student/barcode/' + student_barcode)
            if student_query.status_code == 404:
                res['status'] = 1
                res['msg'] = "Barcode doesn't match!"
            else:
                student_json = student_query.json()
                # once checked out, set student status to 0
                student_json['status'] = 0

                log_json = {
                    'student_id': student_json['id'],
                    'status': 0,
                    'check_in_method': student_json['check_in_method'],
                    'check_by': int(request.cookies.get('guardian_id')),
                    'check_time': int(datetime.datetime.now().timestamp())
                }
                res['msg'] = "Successfully check out!"                    
                requests.put(REST_API + '/student/%d' %
                             student_json['id'], json=student_json)
                requests.post(REST_API + '/log', json=log_json)
    elif request.method == 'GET':
        family_id = int(request.cookies.get('family_id'))
        family_json = requests.get(REST_API + '/family/%d' % family_id).json()
        # filter repeat to be unique
        student_id_set = set()
        # list of json objects
        student_info_list = []

        for family in family_json:
            if family['student_id'] not in student_id_set:  # filter repeat
                student_json = requests.get(
                    REST_API + '/student/%d' % family['student_id']).json()
                if int(student_json['status']) == 2:
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
            res['msg'] = "No checked in student!"

    return jsonify(res)


@app.route('/msgBoardPage', methods=['GET'])
def msgBoardPage():
    user_group = request.cookies.get('user_group')
    if user_group == 'guardian':
        return render_template('flask_templates/guardian/communication.html')
    else:
        return render_template('flask_templates/teacher/teacher_communication.html')


@app.route('/msgBoard', methods=['GET', 'POST'])
def msgBoard():
    res = deepcopy(AMIS_RES_TEMPLATE)
    user_group = request.cookies.get('user_group')
    user_id = int(request.cookies.get('user_id'))

    if request.method == 'GET':
        if user_group == 'guardian':
            guardian_json = requests.get(
                REST_API + '/guardian/%d' % user_id).json()
            fname, lname = guardian_json['fname'], guardian_json['lname']

            msg_show = []
            msgBoard_json = requests.get(
                REST_API + '/msgBoard/guardian/%d' % user_id).json()
            for msg in msgBoard_json:
                if msg['sender_group'] == 'teacher':
                    teacher_json = requests.get(
                        REST_API + '/teacher/%d' % int(msg['sender_id'])).json()
                    msg_show.append({'id': msg['id'], 'fname': 'Teacher - ' + teacher_json['fname'], 'lname': teacher_json['lname'],
                                    'msg': msg['content'], 'timestamp': msg['time']})
                else:
                    msg_show.append({'id': msg['id'], 'fname': fname, 'lname': lname,
                                    'msg': msg['content'], 'timestamp': msg['time']})

            res['data'] = {'items': msg_show[::-1]}
            res["msg"] = "Successfully get historical messages!"
        else:   # teacher
            teacher_json = requests.get(
                REST_API + '/teacher/%d' % user_id).json()
            fname, lname = teacher_json['fname'], teacher_json['lname']

            msg_show = []
            msgBoard_json = requests.get(
                REST_API + '/msgBoard/teacher/%d' % user_id).json()
            for msg in msgBoard_json:
                if msg['sender_group'] == 'guardian':
                    guardian_json = requests.get(
                        REST_API + '/guardian/%d' % int(msg['sender_id'])).json()
                    msg_show.append({'id': msg['id'], 'fname': 'Guardian - ' + guardian_json['fname'], 'lname': guardian_json['lname'],
                                    'msg': msg['content'], 'timestamp': msg['time'], 'read': 'Yes' if msg['been_read'] else 'No'})
                else:
                    msg_show.append({'id': msg['id'], 'fname': fname, 'lname': lname,
                                    'msg': msg['content'], 'timestamp': msg['time'], 'read': 'Yes' if msg['been_read'] else 'No'})

            res['data'] = {'items': msg_show[::-1]}
            res["msg"] = "Successfully get historical messages!"
    else:   # POST
        if user_group == 'guardian':
            student_id_list = list(
                map(int, request.json.get('student_id').split(',')))
            
            error_student_id_list = []
            for student_id in student_id_list:
                # query teacher corresponding to student
                classes_json = requests.get(
                    REST_API + '/classes/student/%d' % student_id).json()
                if classes_json is None or len(classes_json) == 0:
                    error_student_id_list.append(student_id)
                    continue
                
                teacher_id = classes_json[0].get('teacher_id')
                msg_json = {'sender_id': user_id, 'receiver_id': teacher_id, 'sender_group': user_group,
                            'about_student': student_id, 'content': request.json['msg'],
                            'time': int(datetime.datetime.now().timestamp()), 'been_read': False}
                requests.post(REST_API + '/msgBoard', json=msg_json)

            if len(error_student_id_list) > 0:
                res['status'] = 1
                res['msg'] = "Student ID: " + \
                    ', '.join(map(str, error_student_id_list)) + " not assigned to any class!"
                return jsonify(res)
        else:   # teacher send
            if 'reply_msg_id' in request.json.keys():
                reply_msg_id_list = list(
                    map(int, request.json.get('reply_msg_id').split(',')))
                for reply_msg_id in reply_msg_id_list:
                    requests.put(REST_API + '/msgBoard/%d' %
                                 reply_msg_id, json={'been_read': True})

                    reply_msg_json = requests.get(
                        REST_API + '/msgBoard/%d' % reply_msg_id).json()

                    student_id = reply_msg_json.get('about_student')
                    guardian_id = reply_msg_json.get('sender_id')

                    msg_json = {'sender_id': user_id, 'receiver_id': guardian_id, 'sender_group': user_group,
                                'about_student': student_id, 'content': request.json['msg'],
                                'time': int(datetime.datetime.now().timestamp()), 'been_read': True}
                    requests.post(REST_API + '/msgBoard', json=msg_json)
            else:   # TODO: sending to multiple students, should specify which student related to
                student_id_list = list(
                    map(int, request.json.get('student_id').split(',')))
                for student_id in student_id_list:
                    family_json = requests.get(
                        REST_API + '/family/student/%d' % student_id).json()
                    for family in family_json:
                        msg_json = {'sender_id': user_id, 'receiver_id': family['guardian_id'], 'sender_group': user_group,
                                    'about_student': student_id, 'content': request.json['msg'],
                                    'time': int(datetime.datetime.now().timestamp()), 'been_read': True}
                        requests.post(REST_API + '/msgBoard', json=msg_json)

        res["msg"] = "Successfully post message!"

    return jsonify(res)


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
                student_json = requests.get(
                    REST_API + '/student/%d' % family['student_id']).json()
                student_info_list.append({
                    'id': student_json['id'],
                    'fname': student_json['fname'],
                    'lname': student_json['lname']
                })
                student_id_set.add(family['student_id'])
        res['data']['items'] = student_info_list
    else:   # admin or teacher
        if request.cookies.get('user_group') == 'teacher':
            classes_id = request.cookies.get('classes_id')
            classes_json = requests.get(
                REST_API + '/classes/%s' % classes_id).json()
        else:
            classes_json = requests.get(REST_API + '/classes').json()
        # filter repeat to be unique
        student_id_set = set()
        # list of json objects
        student_info_list = []

        for classes in classes_json:
            if classes['student_id'] not in student_id_set:  # filter repeat
                if classes['student_id'] == -1:
                    continue
                student_json = requests.get(
                    REST_API + '/student/%d' % classes['student_id']).json()
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
        guardian_json = requests.get(
            REST_API + '/guardian/%d' % guardian_id).json()
        res['data']['barcode'] = guardian_json.get('barcode')
    elif object == 'student':
        student_id = int(request.args.get('id'))
        student_json = requests.get(
            REST_API + '/student/%d' % student_id).json()
        res['data']['barcode'] = student_json.get('barcode')

    return jsonify(res)


@app.route('/logPage', methods=['GET'])
def logPage():
    if request.cookies.get('user_group') not in {'admin', 'teacher'}:
        abort(403)
    return render_template('flask_templates/teacher/log.html')


@app.route('/log', methods=['GET', 'PUT', 'DELETE'])
def log():
    res = deepcopy(AMIS_RES_TEMPLATE)
    if request.method == 'GET':
        if request.cookies.get('user_group') == 'teacher':
            classes_json = requests.get(REST_API + '/classes/%s' %
                                        request.cookies.get('classes_id')).json()
            student_id_set = set([classes['student_id']
                                 for classes in classes_json])

        logs_json = requests.get(REST_API + '/log').json()
        logs = []

        guardians_json = requests.get(REST_API + '/guardian').json()
        guardian_id_to_json = {0: {'name': 'Admin'}}
        for guardian_json in guardians_json:
            if guardian_json['fname'] and guardian_json['lname']:
                guardian_json['name'] = guardian_json['fname'] + \
                    ' ' + guardian_json['lname']
                guardian_id_to_json[guardian_json['id']] = guardian_json
        students_json = requests.get(REST_API + '/student').json()
        student_id_to_json = {}
        for student_json in students_json:
            if student_json['fname'] and student_json['lname']:
                student_json['name'] = student_json['fname'] + \
                    ' ' + student_json['lname']
                student_id_to_json[student_json['id']] = student_json

        for log in logs_json:
            student_id = log.pop('student_id')

            if request.cookies.get('user_group') == 'teacher' and student_id not in student_id_set:
                continue    # filter student not in the teacher's class

            log['student_name'] = student_id_to_json[student_id]['name']
            log['check_by'] = guardian_id_to_json[log['check_by']]['name']

            if log['daily_progress']:
                log['daily_progress'] = log['daily_progress'].split(',')
            logs.append(log)
        res['data']['items'] = logs[::-1]
        res['msg'] = 'Successfully get logs!'

    elif request.method == 'PUT':   # only for update daily progress
        log_id = int(request.args.get('id'))
        requests.put(REST_API + '/log/%d' % log_id, json=request.json)
        res['msg'] = 'Successfully update daily progress!'

    elif request.method == 'DELETE':
        for log in request.json['log']:
            log_id = int(log['id'])
            requests.delete(REST_API + '/log/%d' % log_id)
            res['msg'] = 'Successfully delete log!'

    return jsonify(res)


@app.route('/guestEnrollPage', methods=['GET'])
def guestEnrollPage():
    if request.cookies.get('user_group') not in {'admin', 'teacher'}:
        abort(403)
    return render_template('flask_templates/general/guest_form.html')


@app.route('/guestEnroll', methods=['POST'])
def guestEnroll():
    # TODO: replicate check
    res = deepcopy(AMIS_RES_TEMPLATE)

    if request.method == 'POST':
        # guardian
        guardian_list = []
        for guardian in request.json['guardians']:
            guardian['barcode'] = guardian['fname'][0].upper(
            ) + guardian['lname'][0].upper() + generate_random_str(5)
            guardian_res = requests.post(REST_API + '/guardian', json=guardian)
            guardian_list.append(guardian_res.json())

        # student
        student_list = []
        for student in request.json['students']:
            student['barcode'] = student['fname'][0].upper(
            ) + student['lname'][0].upper() + generate_random_str(5)
            student['status'] = 1
            student_res = requests.post(
                REST_API + '/student', json=student)
            student_list.append(student_res.json())

            log_json = {
                'student_id': student_res.json()['id'],
                'status': 1,
                'check_in_method': request.json.get('check_in_method'),
                'check_by': int(guardian_list[0]['id']),
                'check_time': int(datetime.datetime.now().timestamp())
            }
            requests.post(REST_API + '/log', json=log_json)

        # familyInfo
        familyInfo_json = {'is_guest': True}
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
                family_json['is_guest'] = True

                family_res = requests.post(
                    REST_API + '/family', json=family_json)
                family_json = family_res.json()

        res['data'] = {'guardians': guardian_list, 'students': student_list}
        res['msg'] = 'Successfully enrolled guest family!'
        return jsonify(res)


@app.route('/printBagePage', methods=['GET'])
def printBagePage():
    if request.cookies.get('user_group') not in {'admin', 'teacher'}:
        abort(403)
    return render_template('static/lib/print_badge.html')


@app.route('/upload', methods=['POST'])
def upload():
    import pandas as pd

    res = deepcopy(AMIS_RES_TEMPLATE)
    f = request.files['file']

    if f.filename.endswith('.xlsx'):
        data = pd.read_excel(f)     # pip install openpyxl
    else:
        data = pd.read_csv(f)

    print(data)
    res['msg'] = f'Upload {f.filename} successfully!'

    return jsonify(res)


def generate_random_str(randomLength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(randomLength):
        random_str += base_str[random.randint(0, length)]
    return random_str


if __name__ == '__main__':
    app.run(port=5000, debug=True)
