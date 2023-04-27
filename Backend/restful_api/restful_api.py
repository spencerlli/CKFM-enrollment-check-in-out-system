from flask import request
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from tables import Guardian, GuardianSchema, Student, StudentSchema, \
    FamilyInfo, FamilyInfoSchema, MsgBoard, MsgBoardSchema, app, db, ma
from tables import Teacher, TeacherSchema, Log, LogSchema

api = Api(app)
bcrypt = Bcrypt(app)


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
        plain_pwd = request.json.get('password', '123456')
        new_guardian = Guardian(
            pwd=request.json.get('password', '123456'),
            pwd_hash=bcrypt.generate_password_hash(plain_pwd).decode('utf-8'),
            fname=request.json.get('fname'),
            lname=request.json.get('lname'),
            phone=request.json.get('phone'),
            email=request.json.get('email'),
            barcode=request.json.get('barcode'),
            relationship=request.json.get('relationship'),
            check_in_method=request.json.get('check_in_method'),
            is_guest=request.json.get('is_guest', 0)
        )
        db.session.add(new_guardian)
        db.session.flush()
        db.session.commit()
        return {
            'id': new_guardian.id,
            'lname': new_guardian.lname,
            'fname': new_guardian.fname,
            'barcode': new_guardian.barcode
        }


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
            plain_pwd = request.json['pwd']
            guardian.pwd_hash = bcrypt.generate_password_hash(
                plain_pwd).decode('utf-8')
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
        Guardian.query.filter_by(id=id).delete()
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
            fname=request.json.get('fname'),
            lname=request.json.get('lname'),
            birthdate=request.json.get('birthdate'),
            gender=request.json.get('gender'),
            grade=request.json.get('grade'),
            allergies=request.json.get('allergies'),
            check_in_method=request.json.get('check_in_method'),
            is_guest=request.json.get('is_guest'),

            programs=request.json.get('programs'),
            sunday_school=request.json.get('sunday_school'),
            cm_lounge=request.json.get('cm_lounge'),
            kid_choir=request.json.get('kid_choir'),
            u3_friday=request.json.get('u3_friday'),
            friday_lounge=request.json.get('friday_lounge'),
            friday_night=request.json.get('friday_night'),

            barcode=request.json.get('barcode'),
            # TODO: add classes_id when post student
            classes_id=request.json.get('classes_id')
        )
        db.session.add(new_student)
        db.session.flush()
        db.session.commit()
        return {
            'id': new_student.id,
            'fname': new_student.fname,
            'lname': new_student.lname,
            'grade': new_student.grade,
            'barcode': new_student.barcode
        }


class StudentResource(Resource):
    def get(self, id):
        # get one by id
        student = Student.query.filter_by(id=id).first_or_404()
        return student_schema.dump(student)

    def put(self, id):
        # update by id
        student = Student.query.filter_by(id=id).first_or_404()
        if 'status' in request.json:
            student.status = request.json['status']
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

        student.programs = request.json.get('programs')

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

        if 'classes_id' in request.json:
            student.classes_id = request.json['classes_id']

        db.session.commit()
        return student_schema.dump(student)

    def delete(self, id):
        # delete by id
        Student.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204


class StudentBarcodeResource(Resource):
    def get(self, barcode):
        student = Student.query.filter_by(barcode=barcode).first_or_404()
        return student_schema.dump(student)
###### Student ######


###### FamilyInfo ######
family_info_schema = FamilyInfoSchema()
families_info_schema = FamilyInfoSchema(many=True)


class FamilyInfoListResource(Resource):
    def get(self):
        # get all
        families_info = FamilyInfo.query.all()
        return families_info_schema.dump(families_info)

    def post(self):
        # create a new one
        new_family_info = FamilyInfo(
            street=request.json.get('street'),
            city=request.json.get('city'),
            state=request.json.get('state'),
            zip=request.json.get('zip'),

            physician=request.json.get('physician'),
            physician_phone=request.json.get('physician_phone'),
            insurance=request.json.get('insurance'),
            insurance_phone=request.json.get('insurance_phone'),
            insurance_policy=request.json.get('insurance_policy'),
            group=request.json.get('group'),

            sunday_school=request.json.get('sunday_school'),
            friday_night=request.json.get('friday_night'),
            special_events=request.json.get('special_events'),

            pay=request.json.get('pay'),
            checkbox=request.json.get('checkbox'),
            is_guest=request.json.get('is_guest', 0)
        )
        db.session.add(new_family_info)
        db.session.flush()
        db.session.commit()
        return family_info_schema.dump(new_family_info)


class FamilyInfoResource(Resource):
    def get(self, id):
        # get one by id
        family_info = FamilyInfo.query.filter_by(id=id).first_or_404()
        return family_info_schema.dump(family_info)

    def put(self, id):
        # update one by id
        family_info = FamilyInfo.query.filter_by(id=id).first_or_404()

        if 'street' in request.json:
            family_info.street = request.json['street']
        if 'city' in request.json:
            family_info.city = request.json['city']
        if 'state' in request.json:
            family_info.state = request.json['state']
        if 'zip' in request.json:
            family_info.zip = request.json['zip']

        if 'physician' in request.json:
            family_info.physician = request.json['physician']
        if 'physician_phone' in request.json:
            family_info.physician_phone = request.json['physician_phone']
        if 'insurance' in request.json:
            family_info.insurance = request.json['insurance']
        if 'insurance_phone' in request.json:
            family_info.insurance_phone = request.json['insurance_phone']
        if 'insurance_policy' in request.json:
            family_info.insurance = request.json['insurance_policy']
        if 'group' in request.json:
            family_info.group_num = request.json['group']

        if 'sunday_school' in request.json:
            family_info.sunday_school = request.json['sunday_school']
        if 'friday_night' in request.json:
            family_info.friday_night = request.json['friday_night']
        if 'special_events' in request.json:
            family_info.special_events = request.json['special_events']

        if 'pay' in request.json:
            family_info.pay = request.json['pay']
        if 'checkbox' in request.json:
            family_info.checkbox = request.json['checkbox']

        db.session.commit()
        return family_info_schema.dump(family_info)

    def delete(self, id):
        # delete one by id
        FamilyInfo.query.filter_by(id=id).delete()
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
    is_guest = db.Column(db.Boolean, default=False)


class FamilySchema(ma.Schema):
    class Meta:
        fields = ('id', 'guardian_id', 'student_id', 'is_guest')


family_schema = FamilySchema()
families_schema = FamilySchema(many=True)


class FamilyListResource(Resource):
    def get(self):
        # get all
        families_got = Family.query.all()
        return families_schema.dump(families_got)

    def post(self):
        # create a new family
        new_family = Family(
            id=request.json['id'],
            guardian_id=request.json['guardian_id'],
            student_id=request.json['student_id'],
            is_guest=request.json.get('is_guest')
        )
        db.session.add(new_family)
        db.session.commit()
        return family_schema.dump(new_family)


class FamilyResource(Resource):
    def get(self, id):
        # get one by id
        families_got = Family.query.filter_by(id=id).all()
        return families_schema.dump(families_got)

    def delete(self, id):
        # delete all records with matched id
        Family.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204


class FamilySingleResource(Resource):
    def get(self, id, guardian_id, student_id):
        # get one by id
        family_got = Family.query.filter_by(
            id=id, guardian_id=guardian_id, student_id=student_id).first_or_404()
        return family_schema.dump(family_got)

    def put(self, id, guardian_id, student_id):
        family_got = Family.query.filter_by(
            id=id, guardian_id=guardian_id, student_id=student_id).first_or_404()

        if 'guardian_id' in request.json:
            family_got.guardian_id = request.json['guardian_id']
        if 'student_id' in request.json:
            family_got.student_id = request.json['student_id']

        db.session.commit()
        return family_schema.dump(family_got)

    def delete(self, id, guardian_id, student_id):
        family_got = Family.query.filter_by(
            id=id, guardian_id=guardian_id, student_id=student_id).first_or_404()
        db.session.delete(family_got)
        db.session.commit()
        return '', 204


class FamilyGuardianResource(Resource):
    def get(self, guardian_id):
        families_got = Family.query.filter_by(guardian_id=guardian_id).all()
        return families_schema.dump(families_got)

    def delete(self, guardian_id):
        families_got = Family.query.filter_by(guardian_id=guardian_id).all()
        for family_got in families_got:
            db.session.delete(family_got)
        db.session.commit()
        return '', 204


class FamilyStudentResource(Resource):
    def get(self, student_id):
        # get one by id
        families_got = Family.query.filter_by(student_id=student_id).all()
        return families_schema.dump(families_got)

    def delete(self, student_id):
        # delete one by id
        families_got = Family.query.filter_by(student_id=student_id).all()
        for family_got in families_got:
            db.session.delete(family_got)
        db.session.commit()
        return '', 204
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
            ((MsgBoard.sender_group == 'teacher') & (MsgBoard.receiver_id == guardian_id)) |
            ((MsgBoard.sender_id == guardian_id) &
             (MsgBoard.sender_group == 'guardian'))
        ).all()
        return msg_records_schema.dump(msg_record)


class MsgBoardTeacherResource(Resource):
    def get(self, teacher_id):
        # get one by id
        msg_record = MsgBoard.query.filter(
            ((MsgBoard.sender_group == 'guardian') & (MsgBoard.receiver_id == teacher_id)) |
            ((MsgBoard.sender_id == teacher_id) &
             (MsgBoard.sender_group == 'teacher'))
        ).all()
        return msg_records_schema.dump(msg_record)
###### MsgBoard ######


###### Teacher ######
teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)


class TeacherListResource(Resource):
    def get(self):
        # get all
        teachers = Teacher.query.all()
        return teachers_schema.dump(teachers)

    def post(self):
        # create a new one
        plain_pwd = request.json['pwd']
        new_teacher = Teacher(
            pwd=request.json['pwd'],
            pwd_hash=bcrypt.generate_password_hash(plain_pwd).decode('utf-8'),
            fname=request.json['fname'],
            lname=request.json['lname'],
            phone=request.json['phone'],
            email=request.json['email'],
            classes_id=request.json['classes_id'],
            privilege=request.json['privilege']
        )
        db.session.add(new_teacher)
        db.session.flush()
        db.session.commit()
        return teacher_schema.dump(new_teacher)


class TeacherResource(Resource):
    def get(self, id):
        # get one by id
        teacher = Teacher.query.filter_by(id=id).first_or_404()
        return teacher_schema.dump(teacher)

    def put(self, id):
        # update one by id
        teacher = Teacher.query.filter_by(id=id).first_or_404()
        if 'pwd' in request.json:
            pwd = request.json['pwd']
            plain_pwd = request.json['pwd']
            teacher.pwd_hash = bcrypt.generate_password_hash(
                plain_pwd).decode('utf-8')
        if 'fname' in request.json:
            teacher.fname = request.json['fname']
        if 'lname' in request.json:
            teacher.lname = request.json['lname']
        if 'phone' in request.json:
            teacher.phone = request.json['phone']
        if 'email' in request.json:
            teacher.email = request.json['email']
        if 'classes_id' in request.json:
            teacher.classes_id = request.json['classes_id']
        db.session.commit()
        return teacher_schema.dump(teacher)

    def delete(self, id):
        # delete one by id
        teacher = Teacher.query.filter_by(id=id).first_or_404()
        db.session.delete(teacher)
        db.session.commit()
        return '', 204


class TeacherPhoneResource(Resource):
    def get(self, phone):
        teacher = Teacher.query.filter_by(phone=phone).first_or_404()
        return teacher_schema.dump(teacher)


class TeacherNameResource(Resource):
    def get(self, fname, lname):
        teacher = Teacher.query.filter_by(
            fname=fname, lname=lname).first_or_404()
        return teacher_schema.dump(teacher)


class TeacherClassesResource(Resource):
    def get(self, classes_id):
        teacher = Teacher.query.filter_by(classes_id=classes_id).first_or_404()
        return teacher_schema.dump(teacher)
###### Teacher ######


###### Classes ######
class Classes(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.String(255), primary_key=True)
    teacher_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, primary_key=True)


class ClassesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'teacher_id', 'student_id')


# named classes in case of confliction with preserve keyword 'class'
classes_schema = ClassesSchema()
classess_schema = ClassesSchema(many=True)  # one more 's' for multiple records


class ClassesListResource(Resource):
    def get(self):
        # get all
        classess = Classes.query.all()
        return classess_schema.dump(classess)

    def post(self):
        # create a new classes
        new_classes = Classes(
            id=request.json['id'],
            teacher_id=request.json['teacher_id'],
            student_id=request.json['student_id'],
        )
        db.session.add(new_classes)
        db.session.commit()
        return classes_schema.dump(new_classes)


class ClassesResource(Resource):
    def get(self, id):
        # get one by id
        classess_got = Classes.query.filter_by(id=id).all()
        return classess_schema.dump(classess_got)

    def delete(self, id):
        # delete one by id
        classes_got = Classes.query.filter_by(id=id).first_or_404()
        db.session.delete(classes_got)
        db.session.commit()
        return '', 204


class ClassesSingleResource(Resource):
    def get(self, id, teacher_id, student_id):
        classes_got = Classes.query.filter_by(
            id=id, teacher_id=teacher_id, student_id=student_id).first_or_404()
        return classes_schema.dump(classes_got)

    def put(self, id, teacher_id, student_id):
        # update one by id
        classes_got = Classes.query.filter_by(
            id=id, teacher_id=teacher_id, student_id=student_id).first_or_404()

        if 'teacher_id' in request.json:
            classes_got.teacher_id = request.json['teacher_id']
        if 'student_id' in request.json:
            classes_got.student_id = request.json['student_id']

        db.session.commit()
        return classes_schema.dump(classes_got)

    def delete(self, id, teacher_id, student_id):
        # delete one by id
        classes_got = Classes.query.filter_by(
            id=id, teacher_id=teacher_id, student_id=student_id).first_or_404()
        db.session.delete(classes_got)
        db.session.commit()
        return '', 204


class ClassesTeacherResource(Resource):
    def get(self, teacher_id):
        classess_got = Classes.query.filter_by(teacher_id=teacher_id).all()
        return classess_schema.dump(classess_got)

    def delete(self, teacher_id):
        classess_got = Classes.query.filter_by(teacher_id=teacher_id).all()
        for class_got in classess_got:
            db.session.delete(class_got)
        db.session.commit()
        return '', 204

class ClassesStudentResource(Resource):
    def get(self, student_id):
        classess_got = Classes.query.filter_by(student_id=student_id).all()
        return classess_schema.dump(classess_got)

    def delete(self, student_id):
        classess_got = Classes.query.filter_by(student_id=student_id).all()
        for class_got in classess_got:
            db.session.delete(class_got)
        db.session.commit()
        return '', 204
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
            status=request.json['status'],
            check_in_method=request.json['check_in_method'],
            check_by=request.json['check_by'],
            check_time=request.json['check_time'],
            daily_progress=request.json['daily_progress'] if 
                'daily_progress' in request.json else None,
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
        if 'status' in request.json:
            log.status = request.json['status']
        if 'check_in_method' in request.json:
            log.check_in_method = request.json['check_in_method']
        if 'check_by' in request.json:
            log.check_in = request.json['check_by']
        if 'check_time' in request.json:
            log.check_in_time = request.json['check_time']
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


class LogGuardianResource(Resource):
    def get(self, guardian_id):
        check_in_logs = Log.query.filter_by(check_in=guardian_id).all()
        check_out_logs = Log.query.filter_by(check_out=guardian_id).all()
        logs = check_in_logs + check_out_logs
        return logs_schema.dump(logs)

    def delete(self, guardian_id):
        check_in_logs = Log.query.filter_by(check_in=guardian_id).all()
        check_out_logs = Log.query.filter_by(check_out=guardian_id).all()
        logs = check_in_logs + check_out_logs
        for log in logs:
            db.session.delete(log)
        db.session.commit()
        return '', 204


class LogStudentResource(Resource):
    def get(self, student_id):
        logs = Log.query.filter_by(student_id=student_id).all()
        return logs_schema.dump(logs)

    def delete(self, student_id):
        logs = Log.query.filter_by(student_id=student_id).all()
        for log in logs:
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
api.add_resource(FamilySingleResource,
                 '/family/single/<int:id>/<int:guardian_id>/<int:student_id>')

api.add_resource(MsgBoardListResource, '/msgBoard')
api.add_resource(MsgBoardResource, '/msgBoard/<int:id>')
api.add_resource(MsgBoardGuardianResource,
                 '/msgBoard/guardian/<int:guardian_id>')
api.add_resource(MsgBoardTeacherResource,
                 '/msgBoard/teacher/<int:teacher_id>')

api.add_resource(TeacherListResource, '/teacher')
api.add_resource(TeacherResource, '/teacher/<int:id>')
api.add_resource(TeacherPhoneResource, '/teacher/phone/<phone>')
api.add_resource(TeacherNameResource, '/teacher/name/<fname>/<lname>')
api.add_resource(TeacherClassesResource, '/teacher/classes/<classes_id>')

api.add_resource(ClassesListResource, '/classes')
api.add_resource(ClassesResource, '/classes/<id>')
api.add_resource(ClassesTeacherResource, '/classes/teacher/<int:teacher_id>')
api.add_resource(ClassesStudentResource, '/classes/student/<int:student_id>')
api.add_resource(ClassesSingleResource,
                 '/classes/<id>/<int:teacher_id>/<int:student_id>')

api.add_resource(LogListResource, '/log')
api.add_resource(LogResource, '/log/<int:id>')
api.add_resource(LogGuardianResource, '/log/guardian/<int:guardian_id>')
api.add_resource(LogStudentResource, '/log/student/<int:student_id>')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
