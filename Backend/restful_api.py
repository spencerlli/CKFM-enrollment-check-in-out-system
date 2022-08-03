from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
import config


app = Flask(__name__)
app.secret_key = '654321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DB)

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


###### Family ######
class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    physician = db.Column(db.String(256))
    physician_phone = db.Column(db.String(256))
    insurance = db.Column(db.String(256))
    insurance_phone = db.Column(db.String(256))
    group_num = db.Column(db.Integer)
    sunday_school = db.Column(db.String(256))
    friday_night = db.Column(db.String(256))
    special_events = db.Column(db.String(256))

    def __repr__(self):
        return '<Family with guardian_id and student_id: %s, %s>' % (self.guardian_id, self.student_id)


class FamilySchema(ma.Schema):
    class Meta:
        fields = ('id', 'guardian_id', 'student_id')


family_schema = FamilySchema()
familys_schema = FamilySchema(many=True)


class FamilyListResource(Resource):
    def get(self):
        familys = Family.query.all()
        return familys_schema.dump(familys)

    def post(self):
        new_family = Family(
            guardian_id=request.json['guardian_id'],
            student_id=request.json['student_id'],
        )
        db.session.add(new_family)
        db.session.commit()
        return family_schema.dump(new_family)


class FamilyResource(Resource):
    def get(self, id):
        family_got = Family.query.filter_by(id=id).first_or_404()
        return family_schema.dump(family_got)

    def put(self, id):
        family_got = Family.query.filter_by(id=id).first_or_404()

        if 'guardian_id' in request.json:
            family_got.guardian_id = request.json['guardian_id']
        if 'guardian_id' in request.json:
            family_got.guardian_id = request.json['guardian_id']

        db.session.commit()
        return family_schema.dump(family_got)

    def delete(self, id):
        family_got = Family.query.filter_by(id=id).first_or_404()
        db.session.delete(family_got)
        db.session.commit()
        return '', 204
###### Family ######


###### Guardian ######
class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    phone_number = db.Column(db.String(256))
    password = db.Column(db.String(256))
    email = db.Column(db.String(256))
    relationship = db.Column(db.String(256))
    is_special = db.Column(db.String(256))
    street = db.Column(db.String(256))
    city = db.Column(db.String(256))
    state = db.Column(db.String(256))
    zip = db.Column(db.Integer)

    def __repr__(self):
        return '<Guardian with phone number: %s>' % self.phone_number


class GuardianSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'password',
                  'email', 'relationship', 'is_special', 'street', 'city', 'state', 'zip')


guardian_schema = GuardianSchema()
guardians_schema = GuardianSchema(many=True)


class GuardianListResource(Resource):
    def get(self):
        guardians = Guardian.query.all()
        return guardians_schema.dump(guardians)

    def post(self):
        new_guardian = Guardian(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            phone_number=request.json['phone_number'],
            password=request.json['password'],
            email=request.json['email'],
            relationship=request.json['relationship'],
            is_special=request.json['is_special'],
            street=request.json['street'],
            city=request.json['city'],
            state=request.json['state'],
            zip=request.json['zip']
        )
        db.session.add(new_guardian)
        db.session.commit()
        return guardian_schema.dump(new_guardian)


class GuardianResource(Resource):
    def get(self, phone_number):
        guardian = Guardian.query.filter_by(
            phone_number=phone_number).first_or_404()
        return guardian_schema.dump(guardian)

    def put(self, phone_number):
        guardian = Guardian.query.filter_by(
            phone_number=phone_number).first_or_404()
        if 'first_name' in request.json:
            guardian.first_name = request.json['first_name']
        if 'last_name' in request.json:
            guardian.last_name = request.json['last_name']
        if 'phone_number' in request.json:
            guardian.phone_number = request.json['phone_number']
        if 'password' in request.json:
            guardian.password = request.json['password']
        if 'email' in request.json:
            guardian.email = request.json['email']
        if 'relationship' in request.json:
            guardian.relationship = request.json['relationship']
        if 'is_special' in request.json:
            guardian.is_special = request.json['is_special']
        if 'street' in request.json:
            guardian.street = request.json['street']
        if 'city' in request.json:
            guardian.city = request.json['city']
        if 'state' in request.json:
            guardian.state = request.json['state']
        if 'zip' in request.json:
            guardian.zip = request.json['zip']
        db.session.commit()
        return guardian_schema.dump(guardian)

    def delete(self, phone_number):
        guardian = Guardian.query.filter_by(
            phone_number=phone_number).first_or_404()
        db.session.delete(guardian)
        db.session.commit()
        return '', 204
###### Guardian ######


###### Student ######
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    checked_in = db.Column(db.Integer)
    barcode = db.Column(db.String(256))
    checked_out = db.Column(db.Integer)
    school = db.Column(db.String(256))
    birth_date = db.Column(db.String(256))
    allergies = db.Column(db.String(256))
    allergies_medication = db.Column(db.String(256))
    medication = db.Column(db.String(256))
    emergency_name = db.Column(db.String(256))
    emergency_phone = db.Column(db.String(256))
    health_insurance = db.Column(db.String(256))

    def __repr__(self):
        return '<Student: %s %s>' % (self.first_name, self.last_name)


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'checked_in', 'barcode', 'checked_out', 'school', 'birth_date',
                  'allergies', 'allergies_medication', 'medication', 'emergency_name', 'emergency_phone', 'health_insurance')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return students_schema.dump(students)

    def post(self):
        new_student = Student(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            checked_in=0,
            barcode=None,
            checked_out=0,
            school=request.json['school'],
            birth_date=request.json['birth_date'],
            allergies=request.json['allergies'],
            allergies_medication=request.json['allergies_medication'],
            medication=request.json['medication'],
            emergency_name=request.json['emergency_name'],
            emergency_phone=request.json['emergency_phone'],
            health_insurance=request.json['health_insurance'],
        )
        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student)


class StudentResource(Resource):
    def get(self, id):
        student = Student.query.filter_by(id=id).first_or_404()
        return student_schema.dump(student)

    def put(self, id):
        student = Student.query.filter_by(id=id).first_or_404()
        if 'first_name' in request.json:
            student.first_name = request.json['first_name']
        if 'last_name' in request.json:
            student.last_name = request.json['last_name']
        if 'checked_in' in request.json:
            student.checked_in = request.json['checked_in']
        if 'barcode' in request.json:
            student.barcode = request.json['barcode']
        if 'checked_out' in request.json:
            student.checked_out = request.json['checked_out']
        if 'school' in request.json:
            student.school = request.json['school']
        if 'birth_date' in request.json:
            student.birth_date = request.json['birth_date']
        if 'allergies' in request.json:
            student.allergies = request.json['allergies']
        if 'allergies_medication' in request.json:
            student.allergies_medication = request.json['allergies_medication']
        if 'medication' in request.json:
            student.medication = request.json['medication']
        if 'emergency_name' in request.json:
            student.emergency_name = request.json['emergency_name']
        if 'emergency_phone' in request.json:
            student.emergency_phone = request.json['emergency_phone']
        if 'health_insurance' in request.json:
            student.health_insurance = request.json['health_insurance']

        db.session.commit()
        return student_schema.dump(student)

    def delete(self, id):
        student = Student.query.filter_by(id=id).first_or_404()
        db.session.delete(student)
        db.session.commit()
        return '', 204
###### Student ######


api.add_resource(FamilyListResource, '/family')
api.add_resource(FamilyResource, '/family/<int:id>')
api.add_resource(GuardianListResource, '/guardian')
api.add_resource(GuardianResource, '/guardian/<int:phone_number>')
api.add_resource(StudentListResource, '/student')
api.add_resource(StudentResource, '/student/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
