import pymysql
pymysql.install_as_MySQLdb()


from email.mime import application
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ubuntu'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'Users'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():
    msg = ''
    if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'password' in request.form:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE first_name = "%s" and last_name = "%s"', (firstName, lastName, ))
        # account = cursor.fetchone()
        account = None
        if account:
            msg = 'Account already exists!'
        elif not (firstName and lastName):
            msg = 'Please fill out the form!'
        else:
            # cursor.execute(
            #     'INSERT INTO students (first_name, last_name, password) VALUES (%s, %s, %s)', (firstName, lastName, password, ))
            # mysql.connection.commit()
            msg = 'You have successfully enrolled!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('enrollment.html', msg=msg)


@app.route('/checkIn', methods=['GET', 'POST'])
def checkIn():
    msg = ''
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM students WHERE password = %s', (password, ))
        account = cursor.fetchone()
        print(account)
        if account:
            cursor.execute(
                'UPDATE students SET checked_in = true WHERE password = "%s";', (password, ))
            msg = 'Check in successfully!'
            mysql.connection.commit()
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
        print(account)
        if account:
            cursor.execute(
                'UPDATE students SET checked_in = false WHERE password = "%s";', (password, ))
            msg = 'Check Out successfully!'
            mysql.connection.commit()
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
