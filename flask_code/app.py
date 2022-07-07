import pymysql
pymysql.install_as_MySQLdb()


from email.mime import application
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.config['MYSQL_HOST'] = '34.221.217.34'
app.config['MYSQL_USER'] = 'ubuntu'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'Users'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


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
            'studentFirstName' in request.form and 'studentLastName' in request.form :
        phoneNumber = request.form['phoneNumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM guardian WHERE phone_number = %s;', (phoneNumber, ))
        account = cursor.fetchone()
        if account:
            msg = 'Family already existed, please do additional enrollment.'
        # elif not (firstName and lastName):
        #     msg = 'Please fill out the form!'
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
    return render_template('firstTimeEnroll.html', msg=msg)


@app.route('/checkIn', methods=['GET', 'POST'])
def checkIn():
    msg = ''
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM students WHERE password = %s', (password, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                "UPDATE students SET checked_in = true WHERE password = %s;", (password, ))
            mysql.connection.commit()
            msg = 'Check in successfully!'
            return render_template('checkIn.html', msg=msg)
        else:
            msg = 'Incorrect password !'
    return render_template('checkIn.html', msg=msg)


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    msg = ''
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM students WHERE password = %s', (password, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                "UPDATE students SET checked_in = false WHERE password = %s;", (password, ))
            mysql.connection.commit()
            msg = 'Check Out successfully!'
            return render_template('checkOut.html', msg=msg)
        else:
            msg = 'Incorrect password!'
    return render_template('checkOut.html', msg=msg)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             'SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
#         account = cursor.fetchone()
#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             msg = 'Logged in successfully !'
#             return render_template('index.html', msg=msg)
#         else:
#             msg = 'Incorrect username / password !'
#     return render_template('login.html', msg=msg)


# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
