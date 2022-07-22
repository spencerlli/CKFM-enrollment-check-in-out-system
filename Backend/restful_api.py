from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api


app = Flask(__name__)
app.secret_key = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ubuntu:123456@34.221.217.34:3306/Users'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


''' Family '''
class Family(db.Table):
    id = db.Column(db.Integer, primary_key=True)
    guardian_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Family: %s>' % self.id


class FamilySchema(ma.Schema):
    class Meta:
        fields = ("id", "guardian_id", "student_id")


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
        family = Family.query.filter_by(id=id).first_or_404()
        return family_schema.dump(family)

    def patch(self, id):
        family = Family.query.filter_by(id=id).first_or_404()

        if 'guardian_id' in request.json:
            family.guardian_id = request.json['guardian_id']
        if 'guardian_id' in request.json:
            family.guardian_id = request.json['guardian_id']

        db.session.commit()
        return family_schema.dump(family)

    def delete(self, id):
        family = Family.query.filter_by(id=id).first_or_404()
        db.session.delete(family)
        db.session.commit()
        return '', 204
''' Family '''


''' Guardian '''
class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<Guardian with phone number: %s>' % self.phone_number


class GuardianSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "phone_number", 'password')


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
        )
        db.session.add(new_guardian)
        db.session.commit()
        return guardian_schema.dump(new_guardian)


class GuardianResource(Resource):
    def get(self, phone_number):
        guardian = Guardian.query.filter_by(phone_number=phone_number).first_or_404()
        return guardian_schema.dump(guardian)

    def patch(self, phone_number):
        guardian = Guardian.query.filter_by(phone_number=phone_number).first_or_404()

        if 'first_name' in request.json:
            guardian.first_name = request.json['first_name']
        if 'last_name' in request.json:
            guardian.last_name = request.json['last_name']
        if 'phone_number' in request.json:
            guardian.phone_number = request.json['phone_number']
        if 'password' in request.json:
            guardian.password = request.json['password']

        db.session.commit()
        return guardian_schema.dump(guardian)

    def delete(self, phone_number):
        guardian = Guardian.query.filter_by(phone_number=phone_number).first_or_404()
        db.session.delete(guardian)
        db.session.commit()
        return '', 204
''' Guardian '''


''' Student '''
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(255))
    checked_in = db.Column(db.Integer)
    barcode = db.Column(db.String(255))
    checked_out = db.Column(db.Integer)


    def __repr__(self):
        return '<Student: %s %s>' % (self.first_name, self.last_name)


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "checked_in", 'barcode', 'checked_out')


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
            checked_in=request.json['checked_in'],
            barcode=request.json['barcode'],
            password=request.json['password'],
        )
        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student)


class StudentResource(Resource):
    def get(self, id):
        student = Student.query.filter_by(id=id).first_or_404()
        return student_schema.dump(student)

    def patch(self, id):
        student = Student.query.filter_by(id=id).first_or_404()

        if 'first_name' in request.json:
            student.first_name = request.json['first_name']
        if 'last_name' in request.json:
            student.last_name = request.json['last_name']

        db.session.commit()
        return student_schema.dump(student)

    def delete(self, id):
        student = Student.query.filter_by(id=id).first_or_404()
        db.session.delete(student)
        db.session.commit()
        return '', 204
''' Student '''

api.add_resource(FamilyListResource, '/family')
api.add_resource(FamilyResource, '/family/<int:id>')
api.add_resource(GuardianListResource, '/guardian')
api.add_resource(GuardianResource, '/guardian/<int:phone_number>')
api.add_resource(StudentListResource, '/student')
api.add_resource(StudentResource, '/student/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
