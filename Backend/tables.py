from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = '654321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DB)

db = SQLAlchemy(app)
CORS(app, resources=r'/*', supports_credentials=True)


class Guardian(db.Model):
    __tablename__ = "guardian"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    phone_number = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    relationship = db.Column(db.String(256))
    check_in_method = db.Column(db.String(256))


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    birth_date = db.Column(db.String(256))
    gender = db.Column(db.String(256))
    grade = db.Column(db.String(256))
    allergies = db.Column(db.String(256))
    check_in_method = db.Column(db.String(256))

    sunday_school = db.Column(db.Boolean)
    CM_lounge = db.Column(db.Boolean)
    kid_choir = db.Column(db.Boolean)
    U3_friday = db.Column(db.Boolean)
    friday_lounge = db.Column(db.Boolean)
    friday_night = db.Column(db.Boolean)


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


# family = db.Table('family',
#     db.Column('id', db.Integer, db.ForeignKey('familyInfo.id'), primary_key=True),
#     db.Column('guardian_id', db.Integer, db.ForeignKey('guardian.id'), primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
# )


if __name__ == '__main__':
    db.create_all()
