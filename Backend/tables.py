from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import config
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = '654321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DB)

db = SQLAlchemy(app)
CORS(app, resources=r'/*', supports_credentials=True)
ma = Marshmallow(app)


class GuardianSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pwd', 'fname', 'lname', 'phone',
                  'email', 'relationship', 'check_in_method', 'barcode')


class Guardian(db.Model):
    __tablename__ = "guardian"
    id = db.Column(db.Integer, primary_key=True)
    pwd = db.Column(db.String(256))
    fname = db.Column(db.String(256))
    lname = db.Column(db.String(256))
    phone = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    relationship = db.Column(db.String(256))
    check_in_method = db.Column(db.String(256))
    barcode = db.Column(db.String(256))


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fname', 'lname', 'birthdate', 'gender', 'grade', 'allergies', 'check_in_method',
                  'sunday_school', 'cm_lounge', 'kid_choir', 'u3_friday', 'friday_lounge', 'friday_night',
                  'check_in', 'check_in_time', 'check_out', 'check_out_time', 'barcode', 'classes_id')


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(256))
    lname = db.Column(db.String(256))
    birthdate = db.Column(db.String(256))
    gender = db.Column(db.String(256))
    grade = db.Column(db.String(256))
    allergies = db.Column(db.String(256))
    check_in_method = db.Column(db.String(256))

    sunday_school = db.Column(db.Boolean)
    cm_lounge = db.Column(db.Boolean)
    kid_choir = db.Column(db.Boolean)
    u3_friday = db.Column(db.Boolean)
    friday_lounge = db.Column(db.Boolean)
    friday_night = db.Column(db.Boolean)

    check_in = db.Column(db.Integer)
    check_in_time = db.Column(db.String(256))
    check_out = db.Column(db.Integer)
    check_out_time = db.Column(db.String(256))

    barcode = db.Column(db.String(256))
    classes_id = db.Column(db.String(256))


class FamilyInfoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street', 'city', 'state', 'zip', 'physician', 'physician_phone', 'insurance', 'insurance_phone',
                  'insurance_policy', 'group', 'sunday_school', 'friday_night', 'special_events', 'pay', 'checkbox')


class FamilyInfo(db.Model):
    __tablename__ = "familyInfo"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(256))
    city = db.Column(db.String(256))
    state = db.Column(db.String(256))
    zip = db.Column(db.String(256))

    physician = db.Column(db.String(256))
    physician_phone = db.Column(db.String(256))
    insurance = db.Column(db.String(256))
    insurance_phone = db.Column(db.String(256))
    insurance_policy = db.Column(db.String(256))
    group = db.Column(db.Integer)

    sunday_school = db.Column(db.String(256))
    friday_night = db.Column(db.String(256))
    special_events = db.Column(db.String(256))

    pay = db.Column(db.Integer)
    checkbox = db.Column(db.Boolean)


class MsgBoardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'send_id', 'receive_id', 'content', 'time', 'about_student', 'sender', 'refer_msg', 'been_read')


class MsgBoard(db.Model):
    __tablename__ = "msgBoard"
    id = db.Column(db.Integer, primary_key=True)
    send_id = db.Column(db.Integer)
    receive_id = db.Column(db.Integer)
    content = db.Column(db.String(256))
    time = db.Column(db.String(256))
    about_student = db.Column(db.Integer)
    sender = db.Column(db.String(256))
    refer_msg = db.Column(db.Integer)
    been_read = db.Column(db.Boolean)


# family = db.Table('family',
#     db.Column('id', db.Integer, db.ForeignKey('familyInfo.id'), primary_key=True),
#     db.Column('guardian_id', db.Integer, db.ForeignKey('guardian.id'), primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
# )


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pwd', 'fname', 'lname', 'phone', 'email', 'classes')


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    pwd = db.Column(db.String(256))
    fname = db.Column(db.String(256))
    lname = db.Column(db.String(256))
    phone = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    classes = db.Column(db.String(256))


# classes = db.Table('classes',
#     db.Column('id', db.String(256), primary_key=True),
#     db.Column('admin_id', db.Integer, db.ForeignKey('admin.id'), primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
# )


if __name__ == '__main__':
    db.create_all()
