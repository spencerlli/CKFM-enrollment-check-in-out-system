from flask import request
from flask_restful import Resource, Api
from tables import Guardian, GuardianSchema, Student, StudentSchema, \
    FamilyInfo, FamilyInfoSchema, MsgBoard, MsgBoardSchema, app, db, ma
from tables import Admin, AdminSchema, Log, LogSchema

api = Api(app)


###### Guardian ######
guardian_schema = GuardianSchema()
guardians_schema = GuardianSchema(many=True)


class GuardianListResource(Resource):
    def get(self):
        # get all
        guardians = Guardian.query.all()
        return guardians_schema.dump(guardians)

    def post(self):
        # create a new one
        new_guardian = Guardian(
            pwd='123456',
            fname=request.json['fname'],
            lname=request.json['lname'],
            phone=request.json['phone'],
            email=request.json['email'],
            relationship=request.json['relationship'],
            check_in_method=request.json['check_in_method'],
        )
        db.session.add(new_guardian)
        db.session.flush()
        db.session.commit()
        return guardian_schema.dump(new_guardian)


class GuardianResource(Resource):
    def get(self, id):
        # get one by id
        guardian = Guardian.query.filter_by(id=id).first_or_404()
        return guardian_schema.dump(guardian)

    def put(self, id):
        # update one by id
        guardian = Guardian.query.filter_by(id=id).first_or_404()
        if 'pwd' in request.json:
            guardian.pwd = request.json['pwd']
        if 'fname' in request.json:
            guardian.fname = request.json['fname']
        if 'lname' in request.json:
            guardian.lname = request.json['lname']
        if 'phone' in request.json:
            guardian.phone = request.json['phone']
        if 'email' in request.json:
            guardian.email = request.json['email']
        if 'relationship' in request.json:
            guardian.relationship = request.json['relationship']
        if 'check_in_method' in request.json:
            guardian.check_in_method = request.json['check_in_method']
        if 'barcode' in request.json:
            guardian.barcode = request.json['barcode']
        db.session.commit()
        return guardian_schema.dump(guardian)

    def delete(self, id):
        # delete one by id
        guardian = Guardian.query.filter_by(id=id).first_or_404()
        db.session.delete(guardian)
        db.session.commit()
        return '', 204


class GuardianPhoneResource(Resource):
    def get(self, phone):
        guardian = Guardian.query.filter_by(phone=phone).first_or_404()
        return guardian_schema.dump(guardian)


class GuardianBarcodeResource(Resource):
    def get(self, barcode):
        guardian = Guardian.query.filter_by(barcode=barcode).first_or_404()
        return guardian_schema.dump(guardian)
###### Guardian ######


###### Student ######
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class StudentListResource(Resource):
    def get(self):
        # get all
        students = Student.query.all()
        return students_schema.dump(students)

    def post(self):
        # create a new one
        new_student = Student(
            fname=request.json['fname'],
            lname=request.json['lname'],
            birthdate=request.json['birthdate'],
            gender=request.json['gender'],
            grade=request.json['grade'],
            allergies=request.json['allergies'],
            check_in_method=request.json['check_in_method'],

            sunday_school=request.json['sunday_school'],
            cm_lounge=request.json['cm_lounge'],
            kid_choir=request.json['kid_choir'],
            u3_friday=request.json['u3_friday'],
            friday_lounge=request.json['friday_lounge'],
            friday_night=request.json['friday_night'],

            # TODO: add classes_id when post student
            classes_id=request.json['classes_id']
        )
        db.session.add(new_student)
        db.session.flush()
        db.session.commit()
        return student_schema.dump(new_student)


class StudentResource(Resource):
    def get(self, id):
        # get one by id
        student = Student.query.filter_by(id=id).first_or_404()
        return student_schema.dump(student)

    def put(self, id):
        # update by id
        student = Student.query.filter_by(id=id).first_or_404()
        if 'fname' in request.json:
            student.fname = request.json['fname']
        if 'lname' in request.json:
            student.lname = request.json['lname']
        if 'birthdate' in request.json:
            student.birthdate = request.json['birthdate']
        if 'gender' in request.json:
            student.gender = request.json['gender']
        if 'grade' in request.json:
            student.grade = request.json['grade']
        if 'allergies' in request.json:
            student.allergies = request.json['allergies']
        if 'check_in_method' in request.json:
            student.check_in_method = request.json['check_in_method']

        if 'sunday_school' in request.json:
            student.sunday_school = request.json['sunday_school']
        if 'cm_lounge' in request.json:
            student.cm_lounge = request.json['cm_lounge']
        if 'kid_choir' in request.json:
            student.kid_choir = request.json['kid_choir']
        if 'u3_friday' in request.json:
            student.u3_friday = request.json['u3_friday']
        if 'friday_lounge' in request.json:
            student.friday_lounge = request.json['friday_lounge']
        if 'friday_night' in request.json:
            student.friday_night = request.json['friday_night']

        if 'check_in' in request.json:
            student.check_in = request.json['check_in']
        if 'check_in_time' in request.json:
            student.check_in_time = request.json['check_in_time']
        if 'check_out' in request.json:
            student.check_out = request.json['check_out']
        if 'check_out_time' in request.json:
            student.check_out_time = request.json['check_out_time']

        if 'classes_id' in request.json:
            student.classes_id = request.json['classes_id']

        db.session.commit()
        return student_schema.dump(student)

    def delete(self, id):
        # delete by id
        student = Student.query.filter_by(id=id).first_or_404()
        db.session.delete(student)
        db.session.commit()
        return '', 204


class StudentBarcodeResource(Resource):
    def get(self, barcode):
        student = Student.query.filter_by(barcode=barcode).first_or_404()
        return student_schema.dump(student)
###### Student ######


###### FamilyInfo ######
family_info_schema = FamilyInfoSchema()
familys_info_schema = FamilyInfoSchema(many=True)


class FamilyInfoListResource(Resource):
    def get(self):
        # get all
        familys_info = FamilyInfo.query.all()
        return familys_info_schema.dump(familys_info)

    def post(self):
        # create a new one
        new_family_info = FamilyInfo(
            street=request.json['street'],
            city=request.json['city'],
            state=request.json['state'],
            zip=request.json['zip'],

            physician=request.json['physician'],
            physician_phone=request.json['physician_phone'],
            insurance=request.json['insurance'],
            insurance_phone=request.json['insurance_phone'],
            insurance_policy=request.json['insurance_policy'],
            group=request.json['group'],

            sunday_school=request.json['sunday_school'],
            friday_night=request.json['friday_night'],
            special_events=request.json['special_events'],

            pay=request.json['pay'],
            checkbox=request.json['checkbox']
        )
        db.session.add(new_family_info)
        db.session.flush()
        db.session.commit()
        return family_info_schema.dump(new_family_info)


class FamilyInfoResource(Resource):
    def get(self, id):
        # get one by id
        familys_info = FamilyInfo.query.filter_by(id=id).first_or_404()
        return family_info_schema.dump(familys_info)

    def put(self, id):
        # update one by id
        familys_info = FamilyInfo.query.filter_by(id=id).first_or_404()

        if 'street' in request.json:
            familys_info.street = request.json['street']
        if 'city' in request.json:
            familys_info.city = request.json['city']
        if 'state' in request.json:
            familys_info.state = request.json['state']
        if 'zip' in request.json:
            familys_info.zip = request.json['zip']

        if 'physician' in request.json:
            familys_info.physician = request.json['physician']
        if 'physician_phone' in request.json:
            familys_info.physician_phone = request.json['physician_phone']
        if 'insurance' in request.json:
            familys_info.insurance = request.json['insurance']
        if 'insurance_phone' in request.json:
            familys_info.insurance_phone = request.json['insurance_phone']
        if 'insurance_policy' in request.json:
            familys_info.insurance = request.json['insurance_policy']
        if 'group' in request.json:
            familys_info.group_num = request.json['group']

        if 'sunday_school' in request.json:
            familys_info.sunday_school = request.json['sunday_school']
        if 'friday_night' in request.json:
            familys_info.friday_night = request.json['friday_night']
        if 'special_events' in request.json:
            familys_info.special_events = request.json['special_events']

        if 'pay' in request.json:
            familys_info.pay = request.json['pay']
        if 'checkbox' in request.json:
            familys_info.checkbox = request.json['checkbox']

        db.session.commit()
        return family_info_schema.dump(familys_info)

    def delete(self, id):
        # delete one by id
        family_got = FamilyInfo.query.filter_by(id=id).first_or_404()
        db.session.delete(family_got)
        db.session.commit()
        return '', 204
###### FamilyInfo ######


###### Family ######
class Family(db.Model):
    __tablename__ = "family"
    id = db.Column(db.Integer, db.ForeignKey(
        'familyInfo.id'), primary_key=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey(
        'guardian.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), primary_key=True)


class FamilySchema(ma.Schema):
    class Meta:
        fields = ('id', 'guardian_id', 'student_id')


family_schema = FamilySchema(many=True)
familys_schema = FamilySchema(many=True)


class FamilyListResource(Resource):
    def get(self):
        # get all
        familys = Family.query.all()
        return familys_schema.dump(familys)

    def post(self):
        # create a new family
        new_family = Family(
            id=request.json['id'],
            guardian_id=request.json['guardian_id'],
            student_id=request.json['student_id'],
        )
        db.session.add(new_family)
        db.session.commit()
        return family_schema.dump(new_family)


class FamilyResource(Resource):
    def get(self, id):
        # get one by id
        family_got = Family.query.filter_by(id=id).all()
        return family_schema.dump(family_got)

    def put(self, id):
        # update one by id
        family_got = Family.query.filter_by(id=id).first_or_404()

        if 'guardian_id' in request.json:
            family_got.guardian_id = request.json['guardian_id']
        if 'student_id' in request.json:
            family_got.student_id = request.json['student_id']

        db.session.commit()
        return family_schema.dump(family_got)

    def delete(self, id):
        # delete one by id
        family_got = Family.query.filter_by(id=id).first_or_404()
        db.session.delete(family_got)
        db.session.commit()
        return '', 204


class FamilyGuardianResource(Resource):
    def get(self, guardian_id):
        # get one by id
        family_got = Family.query.filter_by(guardian_id=guardian_id).all()
        return family_schema.dump(family_got)


class FamilyStudentResource(Resource):
    def get(self, student_id):
        # get one by id
        family_got = Family.query.filter_by(student_id=student_id).all()
        return family_schema.dump(family_got)
###### Family ######


###### MsgBoard ######
msg_record_schema = MsgBoardSchema()
msg_records_schema = MsgBoardSchema(many=True)


class MsgBoardListResource(Resource):
    def get(self):
        # get all
        msg_records = MsgBoard.query.all()
        return msg_records_schema.dump(msg_records)

    def post(self):
        # create a new msg record
        print(request.json)
        new_msg = MsgBoard(
            sender_id=request.json['sender_id'],
            receiver_id=request.json['receiver_id'],
            content=request.json['content'],
            time=request.json['time'],
            about_student=request.json['about_student'],
            sender_group=request.json['sender_group'],
            been_read=request.json['been_read'],
        )
        db.session.add(new_msg)
        db.session.commit()
        return msg_record_schema.dump(new_msg)


class MsgBoardResource(Resource):
    def get(self, id):
        # get one by id
        msg_record = MsgBoard.query.filter_by(id=id).first_or_404()
        return msg_record_schema.dump(msg_record)

    def put(self, id):
        msg_record = MsgBoard.query.filter_by(id=id).first_or_404()
        if 'been_read' in request.json:
            msg_record.been_read = request.json['been_read']
        db.session.commit()
        return msg_record_schema.dump(msg_record)

    def delete(self, id):
        # delete one by id
        msg_got = MsgBoard.query.filter_by(id=id).first_or_404()
        db.session.delete(msg_got)
        db.session.commit()
        return '', 204


class MsgBoardGuardianResource(Resource):
    def get(self, guardian_id):
        # get one by id
        msg_record = MsgBoard.query.filter(
            ((MsgBoard.sender_group == 'admin') & (MsgBoard.receiver_id == guardian_id)) |
            ((MsgBoard.sender_id == guardian_id) & (MsgBoard.sender_group == 'guardian'))
        ).all()
        return msg_records_schema.dump(msg_record)


class MsgBoardAdminResource(Resource):
    def get(self, admin_id):
        # get one by id
        msg_record = MsgBoard.query.filter(
            ((MsgBoard.sender_group == 'guardian') & (MsgBoard.receiver_id == admin_id)) |
            ((MsgBoard.sender_id == admin_id) & (MsgBoard.sender_group == 'admin'))
        ).all()
        return msg_records_schema.dump(msg_record)
###### MsgBoard ######


###### Admin ######
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


class AdminListResource(Resource):
    def get(self):
        # get all
        admins = Admin.query.all()
        return admins_schema.dump(admins)

    def post(self):
        # create a new one
        new_admin = Admin(
            pwd='123456',
            fname=request.json['fname'],
            lname=request.json['lname'],
            phone=request.json['phone'],
            email=request.json['email'],
            classes=request.json['classes']
        )
        db.session.add(new_admin)
        db.session.flush()
        db.session.commit()
        return admin_schema.dump(new_admin)


class AdminResource(Resource):
    def get(self, id):
        # get one by id
        admin = Admin.query.filter_by(id=id).first_or_404()
        return admin_schema.dump(admin)

    def put(self, id):
        # update one by id
        admin = Admin.query.filter_by(id=id).first_or_404()
        if 'pwd' in request.json:
            admin.pwd = request.json['pwd']
        if 'fname' in request.json:
            admin.fname = request.json['fname']
        if 'lname' in request.json:
            admin.lname = request.json['lname']
        if 'phone' in request.json:
            admin.phone = request.json['phone']
        if 'email' in request.json:
            admin.email = request.json['email']
        if 'classes' in request.json:
            admin.classes = request.json['classes']
        db.session.commit()
        return admin_schema.dump(admin)

    def delete(self, id):
        # delete one by id
        admin = Admin.query.filter_by(id=id).first_or_404()
        db.session.delete(admin)
        db.session.commit()
        return '', 204


class AdminPhoneResource(Resource):
    def get(self, phone):
        admin = Admin.query.filter_by(phone=phone).first_or_404()
        return admin_schema.dump(admin)
###### Admin ######


###### Classes ######
class Classes(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.String(256), primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admin.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), primary_key=True)


class ClassesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'admin_id', 'student_id')


classes_schema = ClassesSchema(many=True)
classess_schema = ClassesSchema(many=True)


class ClassesListResource(Resource):
    def get(self):
        # get all
        classess = Classes.query.all()
        return classess_schema.dump(classess)

    def post(self):
        # create a new classes
        new_classes = Classes(
            id=request.json['id'],
            admin_id=request.json['admin_id'],
            student_id=request.json['student_id'],
        )
        db.session.add(new_classes)
        db.session.commit()
        return classes_schema.dump(new_classes)


class ClassesResource(Resource):
    def get(self, id):
        # get one by id
        classes_got = Classes.query.filter_by(id=id).all()
        return classes_schema.dump(classes_got)

    def put(self, id):
        # update one by id
        classes_got = Classes.query.filter_by(id=id).first_or_404()

        if 'admin_id' in request.json:
            classes_got.admin_id = request.json['admin_id']
        if 'student_id' in request.json:
            classes_got.student_id = request.json['student_id']

        db.session.commit()
        return classes_schema.dump(classes_got)

    def delete(self, id):
        # delete one by id
        classes_got = Classes.query.filter_by(id=id).first_or_404()
        db.session.delete(classes_got)
        db.session.commit()
        return '', 204


class ClassesAdminResource(Resource):
    def get(self, admin_id):
        # get one by id
        classes_got = Classes.query.filter_by(admin_id=admin_id).all()
        return classes_schema.dump(classes_got)


class ClassesStudentResource(Resource):
    def get(self, student_id):
        # get one by id
        classes_got = Classes.query.filter_by(student_id=student_id).all()
        return classes_schema.dump(classes_got)
###### Classes ######


###### Logs ######
log_schema = LogSchema()
logs_schema = LogSchema(many=True)


class LogListResource(Resource):
    def get(self):
        # get all
        logs = Log.query.all()
        return logs_schema.dump(logs)

    def post(self):
        # create a new one
        new_log = Log(
            student_id=request.json['student_id'],
            current_status=request.json['current_status'],
            check_method=request.json['check_method'],
            check_in_by=request.json['check_in_by'],
            check_in_time=request.json['check_in_time'],
            check_out_by=request.json['check_out_by'],
            check_out_time=request.json['check_out_time'],
            daily_progress=request.json['daily_progress']
        )
        db.session.add(new_log)
        db.session.flush()
        db.session.commit()
        return log_schema.dump(new_log)


class LogResource(Resource):
    def get(self, id):
        # get one by id
        log = Log.query.filter_by(id=id).first_or_404()
        return log_schema.dump(log)

    def put(self, id):
        # update one by id
        log = Log.query.filter_by(id=id).first_or_404()
        if 'student_id' in request.json:
            log.student_id = request.json['student_id']
        if 'current_status' in request.json:
            log.current_status = request.json['current_status']
        if 'check_method' in request.json:
            log.check_method = request.json['check_method']
        if 'check_in_by' in request.json:
            log.check_in_by = request.json['check_in_by']
        if 'check_in_time' in request.json:
            log.check_in_time = request.json['check_in_time']
        if 'check_out_by' in request.json:
            log.check_out_by = request.json['check_out_by']
        if 'check_out_time' in request.json:
            log.check_out_time = request.json['check_out_time']
        if 'daily_progress' in request.json:
            log.daily_progress = request.json['daily_progress']

        db.session.commit()
        return log_schema.dump(log)

    def delete(self, id):
        # delete one by id
        log = Log.query.filter_by(id=id).first_or_404()
        db.session.delete(log)
        db.session.commit()
        return '', 204
###### Logs ######


api.add_resource(GuardianListResource, '/guardian')
api.add_resource(GuardianResource, '/guardian/<int:id>')
api.add_resource(GuardianPhoneResource, '/guardian/phone/<phone>')
api.add_resource(GuardianBarcodeResource, '/guardian/barcode/<barcode>')

api.add_resource(StudentListResource, '/student')
api.add_resource(StudentResource, '/student/<int:id>')
api.add_resource(StudentBarcodeResource, '/student/barcode/<barcode>')

api.add_resource(FamilyInfoListResource, '/familyInfo')
api.add_resource(FamilyInfoResource, '/familyInfo/<int:id>')
api.add_resource(FamilyListResource, '/family')
api.add_resource(FamilyResource, '/family/<int:id>')
api.add_resource(FamilyGuardianResource, '/family/guardian/<int:guardian_id>')
api.add_resource(FamilyStudentResource, '/family/student/<int:student_id>')

api.add_resource(MsgBoardListResource, '/msgBoard')
api.add_resource(MsgBoardResource, '/msgBoard/<int:id>')
api.add_resource(MsgBoardGuardianResource,
                 '/msgBoard/guardian/<int:guardian_id>')
api.add_resource(MsgBoardAdminResource,
                 '/msgBoard/admin/<int:admin_id>')

api.add_resource(AdminListResource, '/admin')
api.add_resource(AdminResource, '/admin/<int:id>')
api.add_resource(AdminPhoneResource, '/admin/phone/<phone>')

api.add_resource(ClassesListResource, '/classes')
api.add_resource(ClassesResource, '/classes/<int:id>')
api.add_resource(ClassesAdminResource, '/classes/admin/<int:admin_id>')
api.add_resource(ClassesStudentResource, '/classes/student/<int:student_id>')

api.add_resource(LogListResource, '/log')
api.add_resource(LogResource, '/log/<int:id>')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
