import random
from ast import literal_eval as make_tuple
import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import os
import Backend.restful_api.config as config

# pymysql.install_as_MySQLdb()


template_dir = os.path.abspath('../AttendancePro')
static_dir = os.path.abspath('../AttendancePro/sdk')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.secret_key = '123456'

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if ('loggedin' in session.keys() and session['loggedin'] == True):
        return render_template('flask_templates/index.html')
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'phoneNumber' in request.form and 'password' in request.form:
        phoneNumber = request.form['phoneNumber']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM guardian WHERE phone_number = %s AND password = %s;', (phoneNumber, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['phoneNumber'] = account['phone_number']
            msg = 'Logged in successfully!'
            return render_template('flask_templates/index.html', msg=msg)
        else:
            msg = 'Incorrect phone number / password !'
    return render_template('flask_templates/login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form \
                                and 'phoneNumber' in request.form and 'password' in request.form:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phoneNumber = request.form['phoneNumber']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM guardian WHERE phone_number = %s AND password = %s;', (phoneNumber, password, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exist! Please login with your phone number.'
            return render_template('flask_templates/register.html', msg=msg)
        else:
            cursor.execute(
                'INSERT INTO guardian (first_name, last_name, phone_number) VALUES (%s, %s, %s);',
                (firstName, lastName, phoneNumber, ))
            msg = 'Successfully signed up! Please go back to homepage and login.'
    return render_template('flask_templates/register.html', msg=msg)


@app.route('/firstTimeEnroll', methods=['GET', 'POST'])
def firstTimeEnroll():
    '''
    Create a family for a guardian and a child.
    Required info:
                Guardian: First name, last name, phone number
                Child: First name, last name
    '''
    msg = ''
    if request.method == 'POST' and \
        'guardianFirstName' in request.form and 'guardianLastName' in request.form and 'phoneNumber' in request.form and \
            'studentFirstName' in request.form and 'studentLastName' in request.form:
        phoneNumber = request.form['phoneNumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM guardian WHERE phone_number = %s;', (phoneNumber, ))
        guardian = cursor.fetchone()
        if guardian:
            msg = 'Family already existed, please do additional enrollment.'
        # elif not (firstName and lastName):
        #   msg = 'Please fill out the form!'
        else:
            guardianFirstName = request.form['guardianFirstName']
            guardianLastName = request.form['guardianLastName']
            studentFirstName = request.form['studentFirstName']
            studentLastName = request.form['studentLastName']

            cursor.execute('SELECT MAX(id) FROM guardian;')
            guardianId = cursor.fetchone()['MAX(id)'] + 1
            cursor.execute('SELECT MAX(id) FROM student;')
            studentId = cursor.fetchone()['MAX(id)'] + 1
            cursor.execute('SELECT MAX(id) FROM family;')
            familyId = cursor.fetchone()['MAX(id)'] + 1

            cursor.execute(
                'INSERT INTO guardian (first_name, last_name, phone_number) VALUES (%s, %s, %s);',
                (guardianFirstName, guardianLastName, phoneNumber, ))
            cursor.execute(
                'INSERT INTO student (first_name, last_name) VALUES (%s, %s);', (studentFirstName, studentLastName, ))
            cursor.execute(
                'INSERT INTO family (id, guardian_id, student_id) VALUES (%s, %s, %s);', (familyId, guardianId, studentId, ))

            mysql.connection.commit()
            msg = 'Enroll successfully!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('flask_templates/firstTimeEnroll.html', msg=msg)


@app.route('/checkInOut', methods=['GET', 'POST'])
def checkInOut():
    return render_template('check_in_out/main.html')


@app.route('/checkIn', methods=['GET', 'POST'])
def checkIn():
    msg = 'Input guardian\'s phone number to identify the family:'
    if request.method == 'POST' and 'phoneNumber' in request.form:
        phoneNumber = request.form['phoneNumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM guardian WHERE phone_number = %s;', (phoneNumber, ))
        guardian = cursor.fetchone()
        if guardian:
            guardianId = guardian['id']
            cursor.execute(
                'SELECT * FROM family WHERE guardian_id = %s;', (guardianId, ))
            familyId = cursor.fetchone()['id']
            return redirect(url_for('checkInSelect', familyId=familyId))
        else:
            msg = 'Incorrect phone number!'
    elif request.method == 'POST':
        msg = 'Please input guardian\'s phone number!'
    return render_template('flask_templates/checkIn.html', msg=msg)


# @app.route('/checkIn', methods=['GET', 'POST'])
# def checkIn():
#     msg = 'Input guardian\'s phone number to identify the family:'
#     if request.method == 'POST' and 'phoneNumber' in request.form:
#         phoneNumber = request.form['phoneNumber']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             'SELECT * FROM guardian WHERE phone_number = %s;', (phoneNumber, ))
#         guardian = cursor.fetchone()
#         if guardian:
#             guardianId = guardian['id']
#             cursor.execute(
#                 'SELECT * FROM family WHERE guardian_id = %s;', (guardianId, ))
#             familyId = cursor.fetchone()['id']
#             return redirect(url_for('checkInSelect', familyId=familyId))
#         else:
#             msg = 'Incorrect phone number!'
#     elif request.method == 'POST':
#         msg = 'Please input guardian\'s phone number!'
#     return render_template('flask_templates/checkIn.html', msg=msg)


@app.route('/checkInSelect?<int:familyId>', methods=['GET', 'POST'])
def checkInSelect(familyId=0):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT family.id, family.guardian_id, guardian.first_name, guardian.last_name, \
            family.student_id, student.first_name, student.last_name \
            FROM family JOIN guardian ON family.guardian_id = guardian.id \
            JOIN student ON family.student_id = student.id \
            WHERE family.id = %s;', (familyId, ))
        data = cursor.fetchall()

        guardians, students = set(), set()
        for d in data:
            guardians.add((d['guardian_id'], d['first_name'], d['last_name']))
            students.add(
                (d['student_id'], d['student.first_name'], d['student.last_name']))

        return render_template('flask_templates/checkInSelect.html', guardians=guardians, students=students, familyId=familyId)
    else:
        guardian = request.form['guardian']
        student = request.form['student']
        return redirect(url_for('checkInSuccess', guardian=guardian, student=student))


@app.route('/checkInSuccess?<string:guardian>&<string:student>', methods=['GET'])
def checkInSuccess(guardian, student):
    guardian = make_tuple(guardian)
    student = make_tuple(student)
    guardianId = guardian[0]
    studentId = student[0]
    guardianName = guardian[1] + ' ' + guardian[2]
    studentName = student[1] + ' ' + student[2]
    barcode = generate_random_str(randomLength=8)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'UPDATE student SET checked_in = %s, barcode = %s WHERE id = %s;', (guardianId, barcode, studentId, ))
    mysql.connection.commit()

    return render_template('flask_templates/checkInSuccess.html', guardianName=guardianName, studentName=studentName, barcode=barcode)


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    msg = 'Input guardian\'s phone number to identify the family:'
    if request.method == 'POST' and 'phoneNumber' in request.form:
        phoneNumber = request.form['phoneNumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM guardian WHERE phone_number = %s;', (phoneNumber, ))
        guardian = cursor.fetchone()
        if guardian:
            guardianId = guardian['id']
            cursor.execute(
                'SELECT * FROM family WHERE guardian_id = %s;', (guardianId, ))
            familyId = cursor.fetchone()['id']
            return redirect(url_for('checkOutSelect', familyId=familyId))
        else:
            msg = 'Incorrect phone number!'
    elif request.method == 'POST':
        msg = 'Please input guardian\'s phone number!'
    return render_template('flask_templates/checkOut.html', msg=msg)


@app.route('/checkOutSelect?<int:familyId>', methods=['GET', 'POST'])
def checkOutSelect(familyId=0):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT family.id, family.guardian_id, guardian.first_name, guardian.last_name, \
            family.student_id, student.first_name, student.last_name \
            FROM family JOIN guardian ON family.guardian_id = guardian.id \
            JOIN student ON family.student_id = student.id \
            WHERE family.id = %s;', (familyId, ))
        data = cursor.fetchall()

        guardians, students = set(), set()
        for d in data:
            guardians.add((d['guardian_id'], d['first_name'], d['last_name']))
            students.add(
                (d['student_id'], d['student.first_name'], d['student.last_name']))

        return render_template('flask_templates/checkOutSelect.html', guardians=guardians, students=students, familyId=familyId)
    else:
        guardian = request.form['guardian']
        student = request.form['student']
        studentId = make_tuple(student)[0]
        barcode = request.form['barcode']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT id from student where barcode = %s;', (barcode, ))
        if cursor.fetchone()['id'] == studentId:
            return redirect(url_for('checkOutSuccess', msg=None, guardian=guardian, student=student))
        else:
            msg = 'Picking up wrong student, please verify.'
            return render_template('flask_templates/checkOutSelect.html', msg=msg, guardians=guardians, students=students, familyId=familyId)


@app.route('/checkOutSuccess?<string:guardian>&<string:student>', methods=['GET'])
def checkOutSuccess(guardian, student):
    guardian = make_tuple(guardian)
    student = make_tuple(student)
    guardianId = guardian[0]
    studentId = student[0]
    guardianName = guardian[1] + ' ' + guardian[2]
    studentName = student[1] + ' ' + student[2]

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'UPDATE student SET checked_in = 0, checked_out = %s, barcode = NULL WHERE id = %s;', (guardianId, studentId, ))
    mysql.connection.commit()

    return render_template('flask_templates/checkOutSuccess.html', guardianName=guardianName, studentName=studentName)


def generate_random_str(randomLength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(randomLength):
        random_str += base_str[random.randint(0, length)]
    return random_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
