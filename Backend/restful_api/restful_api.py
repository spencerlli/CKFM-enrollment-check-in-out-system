from flask import request
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from tables import Guardian, GuardianSchema, Student, StudentSchema, \
    FamilyInfo, FamilyInfoSchema, MsgBoard, MsgBoardSchema, app, db, ma
from tables import Teacher, TeacherSchema, Log, LogSchema
from sqlalchemy.exc import IntegrityError

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
        try:
            db.session.begin()
            guardians_data = request.json if isinstance(request.json, list) else [request.json]
            new_guardians = []
            for guardian_data in guardians_data:
                plain_pwd = str(guardian_data.get('pwd', '123456'))
                new_guardian = Guardian(
                    pwd=guardian_data.get('pwd', '123456'),
                    pwd_hash=bcrypt.generate_password_hash(plain_pwd).decode('utf-8'),
                    fname=guardian_data.get('fname'),
                    lname=guardian_data.get('lname'),
                    phone=guardian_data.get('phone'),
                    email=guardian_data.get('email'),
                    barcode=guardian_data.get('barcode'),
                    relationship=guardian_data.get('relationship'),
                    fellow_group=guardian_data.get('fellow_group', ''),
                    check_in_method=guardian_data.get('check_in_method'),
                    is_guest=guardian_data.get('is_guest', 0)
                )
                db.session.add(new_guardian)
                db.session.flush()
                new_guardians.append(new_guardian)

            db.session.commit()

            return {
                'guardians': [
                    {
                        'id': guardian.id,
                        'lname': guardian.lname,
                        'fname': guardian.fname,
                        'barcode': guardian.barcode
                    }
                    for guardian in new_guardians
                ]
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
        # delete by id
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
        try:
            db.session.begin()
            new_students = []

            for student_data in request.json:
                new_student = Student(
                    status=student_data.get('status'),
                    fname=student_data.get('fname'),
                    lname=student_data.get('lname'),
                    birthdate=student_data.get('birthdate'),
                    gender=student_data.get('gender'),
                    grade=student_data.get('grade'),
                    allergies=student_data.get('allergies'),
                    check_in_method=student_data.get('check_in_method'),
                    is_guest=student_data.get('is_guest'),
                    programs=student_data.get('programs'),
                    sunday_school=student_data.get('sunday_school'),
                    cm_lounge=student_data.get('cm_lounge'),
                    kid_choir=student_data.get('kid_choir'),
                    u3_friday=student_data.get('u3_friday'),
                    friday_lounge=student_data.get('friday_lounge'),
                    friday_night=student_data.get('friday_night'),
                    barcode=student_data.get('barcode'),
                    classes_id=student_data.get('classes_id')
                )
                db.session.add(new_student)
                db.session.flush()
                new_students.append(new_student)

            db.session.commit()

            return {
                'students': [
                    {
                        'id': student.id,
                        'fname': student.fname,
                        'lname': student.lname,
                        'grade': student.grade,
                        'barcode': student.barcode
                    }
                    for student in new_students
                ]
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
        try:
            db.session.begin()
            family_info_data = request.json
            if isinstance(family_info_data, dict):
                family_info_data = [family_info_data]

            new_family_infos = []
            for info_data in family_info_data:
                new_family_info = FamilyInfo(
                    street=info_data.get('street'),
                    city=info_data.get('city'),
                    state=info_data.get('state'),
                    zip=info_data.get('zip'),
                    physician=info_data.get('physician'),
                    physician_phone=info_data.get('physician_phone'),
                    insurance=info_data.get('insurance'),
                    insurance_phone=info_data.get('insurance_phone'),
                    insurance_policy=info_data.get('insurance_policy'),
                    group=info_data.get('group'),
                    sunday_school=info_data.get('sunday_school'),
                    friday_night=info_data.get('friday_night'),
                    special_events=info_data.get('special_events'),
                    pay=info_data.get('pay'),
                    checkbox=info_data.get('checkbox'),
                    is_guest=info_data.get('is_guest', 0)
                )
                db.session.add(new_family_info)
                db.session.flush()
                new_family_infos.append(new_family_info)

            db.session.commit()

            return {
                'familyInfos': [
                    {
                        'id': family_info.id,
                        'street': family_info.street,
                        'city': family_info.city,
                        'state': family_info.state,
                        'zip': family_info.zip,
                        'physician': family_info.physician,
                        'physician_phone': family_info.physician_phone,
                        'insurance': family_info.insurance,
                        'insurance_phone': family_info.insurance_phone,
                        'insurance_policy': family_info.insurance_policy,
                        'group': family_info.group,
                        'sunday_school': family_info.sunday_school,
                        'friday_night': family_info.friday_night,
                        'special_events': family_info.special_events,
                        'pay': family_info.pay,
                        'checkbox': family_info.checkbox
                    } for family_info in new_family_infos
                ]
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
        # delete by id
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
        try:
            db.session.begin()
            family_data = request.json
            if isinstance(family_data, dict):
                family_data = [family_data]

            new_families = []
            for data in family_data:
                new_family = Family(
                    id=data['id'],
                    guardian_id=data['guardian_id'],
                    student_id=data['student_id'],
                    is_guest=data.get('is_guest')
                )
                db.session.add(new_family)
                db.session.flush()
                new_families.append(new_family)
            db.session.commit()
            return { 
                'families': [
                    {
                        'id': family.id,
                        'guardian_id': family.guardian_id,
                        'student_id': family.student_id,
                        'is_guest': family.is_guest
                    } for family in new_families
                ] 
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
        Family.query.filter_by(guardian_id=guardian_id).delete()
        db.session.commit()
        return '', 204


class FamilyStudentResource(Resource):
    def get(self, student_id):
        # get one by id
        families_got = Family.query.filter_by(student_id=student_id).all()
        return families_schema.dump(families_got)

    def delete(self, student_id):
        # delete by id
        Family.query.filter_by(student_id=student_id).delete()
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
        try:
            db.session.begin()
            msg_data = request.json
            if isinstance(msg_data, dict):
                msg_data = [msg_data]

            new_msgs = []
            for data in msg_data:
                new_msg = MsgBoard(
                    sender_id=data['sender_id'],
                    receiver_id=data['receiver_id'],
                    content=data['content'],
                    time=data['time'],
                    about_student=data['about_student'],
                    sender_group=data['sender_group'],
                    been_read=data['been_read'],
                )

                db.session.add(new_msg)
                db.session.flush()
                new_msgs.append(new_msg)

            db.session.commit()
            return { 
                'msg_records': [
                    {
                        'id': msg_record.id,
                        'sender_id': msg_record.sender_id,
                        'receiver_id': msg_record.receiver_id,
                        'content': msg_record.content,
                        'time': msg_record.time,
                        'about_student': msg_record.about_student,
                        'sender_group': msg_record.sender_group,
                        'been_read': msg_record.been_read
                    } for msg_record in new_msgs
                ] 
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
        # delete by id
        msg_got = MsgBoard.query.filter_by(id=id).first_or_404()
        db.session.delete(msg_got)
        db.session.commit()
        return '', 204


class MsgBoardGuardianResource(Resource):
    def get(self, guardian_id):
        # get one by id
        msg_record = MsgBoard.query.filter(
            ((MsgBoard.sender_group == 'teacher' or MsgBoard.sender_group == 'admin') & 
             (MsgBoard.receiver_id == guardian_id)) |
            ((MsgBoard.sender_id == guardian_id) &
             (MsgBoard.sender_group == 'guardian'))
        ).all()
        return msg_records_schema.dump(msg_record)


class MsgBoardTeacherResource(Resource):
    def get(self, teacher_id):
        # get one by id
        msg_record = MsgBoard.query.filter(
            ((MsgBoard.sender_group == 'guardian') & 
             (MsgBoard.receiver_id == teacher_id)) |
            ((MsgBoard.sender_id == teacher_id) &
             (MsgBoard.sender_group == 'teacher' or MsgBoard.sender_group == 'admin'))
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
        try:
            db.session.begin()
            teacher_data = request.json
            if isinstance(teacher_data, dict):
                teacher_data = [teacher_data]

            new_teachers = []
            for data in teacher_data:
                plain_pwd = data['pwd']
                new_teacher = Teacher(
                    pwd=data['pwd'],
                    pwd_hash=bcrypt.generate_password_hash(plain_pwd).decode('utf-8'),
                    fname=data['fname'],
                    lname=data['lname'],
                    phone=data['phone'],
                    email=data['email'],
                    classes_id=data['classes_id'],
                    privilege=data['privilege']
                )
                db.session.add(new_teacher)
                db.session.flush()
                new_teachers.append(new_teacher)

            db.session.commit()
            return { 
                'teachers': [
                    {
                        'id': teacher.id,
                        'fname': teacher.fname,
                        'lname': teacher.lname,
                        'phone': teacher.phone,
                        'email': teacher.email,
                        'classes_id': teacher.classes_id,
                        'privilege': teacher.privilege
                    } for teacher in new_teachers
                ]
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


class TeacherResource(Resource):
    def get(self, id):
        # get one by id
        teacher = Teacher.query.filter_by(id=id).first_or_404()
        return teacher_schema.dump(teacher)

    def put(self, id):
        # update one by id
        teacher = Teacher.query.filter_by(id=id).first_or_404()

        # Avoid duplicate entries
        if teacher.phone == request.json.get('phone'):
            del request.json['phone']
        if teacher.email == request.json.get('email'):
            del request.json['email']

        try:
            for key, value in request.json.items():
                setattr(teacher, key, value)

            teacher.pwd_hash = bcrypt.generate_password_hash(
                request.json['pwd']).decode('utf-8')

            db.session.commit()
            return {"msg": "Teacher updated successfully.", "status": 0}

        except IntegrityError as e:
            db.session.rollback()
            return {"msg": "An error occurred: {}".format(e), "status": -1}


    def delete(self, id):
        # delete by id
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
        try:
            db.session.begin()
            classes_data = request.json
            if isinstance(classes_data, dict):
                classes_data = [classes_data]

            new_classes_list = []
            for data in classes_data:
                new_classes = Classes(
                    id=data['id'],
                    teacher_id=data['teacher_id'],
                    student_id=data['student_id'],
                )
                db.session.add(new_classes)
                db.session.flush()
                new_classes_list.append(new_classes)

            db.session.commit()
            return { 
                'classess': [
                    {
                        'id': classes.id,
                        'teacher_id': classes.teacher_id,
                        'student_id': classes.student_id
                    } for classes in new_classes_list
                ]
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
        Classes.query.filter_by(teacher_id=teacher_id).delete()
        db.session.commit()
        return '', 204

class ClassesStudentResource(Resource):
    def get(self, student_id):
        classess_got = Classes.query.filter_by(student_id=student_id).all()
        return classess_schema.dump(classess_got)

    def delete(self, student_id):
        Classes.query.filter_by(student_id=student_id).delete()
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
        try:
            db.session.begin()
            log_data = request.json
            if isinstance(log_data, dict):
                log_data = [log_data]

            new_logs_list = []
            for data in log_data:
                new_log = Log(
                    student_id=data['student_id'],
                    status=data['status'],
                    check_in_method=data['check_in_method'],
                    check_by=data['check_by'],
                    check_time=data['check_time'],
                    daily_progress=data.get('daily_progress')
                )
                db.session.add(new_log)
                db.session.flush()
                new_logs_list.append(new_log)

            db.session.commit()
            return {
                'logs': [
                    {
                        'id': log.id,
                        'student_id': log.student_id,
                        'status': log.status,
                        'check_in_method': log.check_in_method,
                        'check_by': log.check_by,
                        'check_time': log.check_time,
                        'daily_progress': log.daily_progress
                    } for log in new_logs_list
                ]
            }

        except Exception as e:
            db.session.rollback()
            return 'Transaction failed, error: {}'.format(str(e)), 400


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
            log.check_by = request.json['check_by']
        if 'check_time' in request.json:
            log.check_time = request.json['check_time']
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
        logs = Log.query.filter_by(check_by=guardian_id).all()
        return logs_schema.dump(logs)

    def delete(self, guardian_id):
        Log.query.filter_by(check_by=guardian_id).delete()  # delete all
        db.session.commit()
        return '', 204


class LogStudentResource(Resource):
    def get(self, student_id):
        logs = Log.query.filter_by(student_id=student_id).all()
        return logs_schema.dump(logs)

    def delete(self, student_id):
        Log.query.filter_by(student_id=student_id).delete()
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
