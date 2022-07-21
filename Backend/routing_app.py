import random
from ast import literal_eval as make_tuple
import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import os

# pymysql.install_as_MySQLdb()

template_dir = os.path.abspath('../AttendancePro')
static_dir = os.path.abspath('../AttendancePro/sdk')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = '123456'


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


@app.route('/firstTimeEnroll', methods=['GET', 'POST'])
def firstTimeEnroll():
    msg = ''
    if request.method == 'GET':
        return render_template('enrollment/GuardianEnrollment.html', msg=msg)
    else:
        return render_template('enrollment/StudentEnrollment.html', msg=msg)


@app.route('/studentEnrollment', methods=['GET', 'POST'])
def studentEnrollment():
    return render_template('enrollment/StudentEnrollment.html')


@app.route('/enrollmentCheck', methods=['GET', 'POST'])
def enrollmentCheck():
    return render_template('enrollment/CompleteEnrollmentCheck.html')


@app.route('/checkInOut', methods=['GET', 'POST'])
def checkInOut():
    return render_template('check_in_out/main.html')


@app.route('/checkIn', methods=['GET', 'POST'])
def checkIn():
    return render_template('check_in_out/check_in.html')


@app.route('/checkIn2', methods=['GET', 'POST'])
def checkIn2():
    return render_template('check_in_out/check_in2.html')


@app.route('/checkInSuccess', methods=['GET', 'POST'])
def checkInSuccess():
    return render_template('check_in_out/s_check_in.html')


@app.route('/checkOut', methods=['GET', 'POST'])
def checkOut():
    return render_template('check_in_out/check_out.html')


@app.route('/checkOut2', methods=['GET', 'POST'])
def checkOut2():
    return render_template('check_in_out/check_out2.html')


@app.route('/checkOutSuccess', methods=['GET', 'POST'])
def checkOutSuccess():
    return render_template('check_in_out/s_check_out.html')


def generate_random_str(randomLength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(randomLength):
        random_str += base_str[random.randint(0, length)]
    return random_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
