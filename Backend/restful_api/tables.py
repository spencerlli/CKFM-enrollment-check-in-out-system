from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import restful_config
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = '654321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    restful_config.MYSQL_USER, restful_config.MYSQL_PASSWORD, restful_config.MYSQL_HOST, restful_config.MYSQL_PORT, restful_config.MYSQL_DB)
# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, resources=r'/*', supports_credentials=True)
ma = Marshmallow(app)


class GuardianSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pwd', 'pwd_hash', 'fname', 'lname', 'phone', 'email', 'relationship', 
                  'fellow_group', 'check_in_method', 'barcode', 'is_primary', 'is_guest')


class Guardian(db.Model):
    __tablename__ = "guardian"
    id = db.Column(db.Integer, primary_key=True)
    pwd = db.Column(db.String(255))
    pwd_hash = db.Column(db.String(255))
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    phone = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    relationship = db.Column(db.String(255))
    fellow_group = db.Column(db.String(255))
    check_in_method = db.Column(db.String(255))
    barcode = db.Column(db.String(255))

    is_primary = db.Column(db.Boolean, default=False)
    is_guest = db.Column(db.Boolean, default=False)


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'fname', 'lname', 'birthdate', 'gender', 'grade', 'allergies', 
                  'check_in_method','programs', 'sunday_school', 'cm_lounge', 'kid_choir', 'u3_friday',
                  'friday_lounge', 'friday_night', 'barcode', 'classes_id', 'is_guest')


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0)
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    birthdate = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    grade = db.Column(db.String(255))
    allergies = db.Column(db.String(255))
    check_in_method = db.Column(db.String(255))

    programs = db.Column(db.String(255))
    sunday_school = db.Column(db.Boolean)
    cm_lounge = db.Column(db.Boolean)
    kid_choir = db.Column(db.Boolean)
    u3_friday = db.Column(db.Boolean)
    friday_lounge = db.Column(db.Boolean)
    friday_night = db.Column(db.Boolean)

    barcode = db.Column(db.String(255))
    classes_id = db.Column(db.String(255))

    is_guest = db.Column(db.Boolean, default=False)


class FamilyInfoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street', 'city', 'state', 'zip', 'physician', 'physician_phone', 'insurance', 'insurance_phone',
                  'insurance_policy', 'group', 'sunday_school', 'friday_night', 'special_events', 'pay', 'checkbox', 'is_guest')


class FamilyInfo(db.Model):
    __tablename__ = "familyInfo"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip = db.Column(db.String(255))

    physician = db.Column(db.String(255))
    physician_phone = db.Column(db.String(255))
    insurance = db.Column(db.String(255))
    insurance_phone = db.Column(db.String(255))
    insurance_policy = db.Column(db.String(255))
    group = db.Column(db.String(255))

    sunday_school = db.Column(db.String(255))
    friday_night = db.Column(db.String(255))
    special_events = db.Column(db.String(255))

    pay = db.Column(db.Integer)
    checkbox = db.Column(db.Boolean, default=False)

    is_guest = db.Column(db.Boolean, default=False)


class MsgBoardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sender_id', 'receiver_id', 'content',
                  'time', 'about_student', 'sender_group', 'been_read')


class MsgBoard(db.Model):
    __tablename__ = "msgBoard"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    content = db.Column(db.String(255))
    time = db.Column(db.String(255))
    about_student = db.Column(db.Integer)
    sender_group = db.Column(db.String(255))
    been_read = db.Column(db.Boolean)


# family = db.Table('family',
#     db.Column('id', db.Integer, db.ForeignKey('familyInfo.id'), primary_key=True),
#     db.Column('guardian_id', db.Integer, db.ForeignKey('guardian.id'), primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
#     db.Column('is_guest', db.Boolean, default=False)
# )


class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pwd', 'pwd_hash', 'fname', 'lname', 'phone',
                  'email', 'classes_id', 'privilege')


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    pwd = db.Column(db.String(255))
    pwd_hash = db.Column(db.String(255))
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    phone = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    classes_id = db.Column(db.String(255))

    # for now there are only teacher and scanner, no normal teacher
    privilege = db.Column(db.Integer)   # 0: scanner, 1: teacher, 2: admin


# classes = db.Table('classes',
#     db.Column('id', db.String(255), primary_key=True),
#     db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
# )


class LogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'student_id', 'status', 'check_in_method', 'check_by', 'check_time', 'daily_progress')


class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)   # 0: check out, 1: pre check in, 2: check in
    check_in_method = db.Column(db.String(255))
    check_by = db.Column(db.Integer)
    check_time = db.Column(db.String(255))
    daily_progress = db.Column(db.String(255))


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
