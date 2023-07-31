import pandas as pd
import random
import re
import requests


ERRORS = {
    'read_error': 'Spreadsheet or worksheet not found\n',
    'header_error': 'Spreadsheet header are wrong\n',
    'familyInfo_error': "Guardian's familyInfo are incomplete\n",
    'guardian_error': 'Guardian info are incomplete\n',
    'student_error': 'Student info are incomplete\n',
    'name_error': 'These names are incorrect in format\n',
}


def generate_random_str(randomLength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(randomLength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def read_spreadsheet(spreadsheet_path):
    try:
        guardian_df = pd.read_excel(spreadsheet_path, 'Guardian')
        student_df = pd.read_excel(spreadsheet_path, 'Student')
        familyInfo_df = pd.read_excel(
            spreadsheet_path, 'FamilyInfo')
        # teacher_df = pd.read_excel(spreadsheet_path, 'Teacher')
    except ValueError as _:
        return {'status': 1, 'error_msg': ERRORS['read_error']}
    return {'status': 0, 'data': (guardian_df, student_df, familyInfo_df)}


def create_familyInfo(familyInfo_df):
    # FamilyInfo table
    try:
        family_df = familyInfo_df[['guardian_Names', 'student_Names']]
    except KeyError as _:
        return {'status': 1, 'error_msg': ERRORS['header_error']}

    family_df.columns = ['guardian_names', 'student_names']

    try:
        familyInfo_df = familyInfo_df[['street', 'city', 'state', 'zip', 'physician', 'physician_phone',
                                       'insurance', 'insurance_phone', 'insurance_policy#', 'group',
                                       'Sunday_school', 'Friday_night', 'special_events', 'paid', 'checkbox']]
    except KeyError as _:
        return {'status': 1, 'error_msg': ERRORS['header_error']}

    familyInfo_df.columns = ['street', 'city', 'state', 'zip', 'physician', 'physician_phone',
                             'insurance', 'insurance_phone', 'insurance_policy#', 'group',
                             'sunday_school', 'friday_night', 'special_events', 'paid', 'checkbox']

    error_family_guardians = family_df[familyInfo_df.isna().sum(
        axis=1) > 0]['guardian_names']
    if len(error_family_guardians) > 0:
        return {'status': 1, 'error_msg': ERRORS['familyInfo_error'] + str(error_family_guardians)}
    return {'status': 0, 'data': (family_df, familyInfo_df)}


def create_guardian(family_df, guardian_df):
    # Guardian table
    primary_guardians = []
    for _, family in family_df.iterrows():
        primary_guardians.append(family['guardian_names'].split(';')[0])

    key_order = ['phone_number', 'password', 'first_name',
                 'last_name', 'email', 'class', 'fellow_group', 'relationship']
    try:
        guardian_df = guardian_df[key_order]
    except KeyError as _:
        return {'status': 1, 'error_msg': ERRORS['header_error']}

    guardian_df.columns = ['phone', 'pwd', 'fname', 'lname',
                           'email', 'classes_id', 'fellow_group', 'relationship']

    guardian_df['check_in_method'] = 'barcode'

    guardian_df['is_primary'] = False

    for i, guardian in guardian_df.iterrows():
        if guardian['fname'] + ' ' + guardian['lname'] in primary_guardians:
            guardian_df.loc[i, 'is_primary'] = True

    guardian_df = guardian_df[['pwd', 'fname', 'lname', 'phone', 'email',
                               'relationship', 'check_in_method', 'is_primary']]

    error_guardians = guardian_df[guardian_df.isna().sum(axis=1) > 0]
    if len(error_guardians) > 0:
        return {'status': 1, 'error_msg': ERRORS['guardian_error'] + str(error_guardians[['fname', 'lname']])}
    return {'status': 0, 'data': guardian_df}


def create_student(student_df):
    # Student table
    key_order = ['first_name', 'last_name', 'date_of_birth', 'gender', 'class', 'grade',
                 'allergies', 'check_in_method', 'Sunday_school', 'cm_lounge',
                 'kid_choir', 'u3_Friday', 'Friday_lounge', 'Friday_night']
    try:
        student_df = student_df[key_order]
    except KeyError as _:
        return {'status': 1, 'error_msg': ERRORS['header_error']}

    student_df.columns = ['fname', 'lname', 'birthdate', 'gender', 'classes_id', 'grade',
                          'allergies', 'check_in_method', 'sunday_school', 'cm_lounge',
                          'kid_choir', 'u3_friday', 'friday_lounge', 'friday_night']
    student_df['status'] = 0

    error_students = student_df[student_df.isna().sum(axis=1) > 0]
    if len(error_students) > 0:
        return {'status': 1, 'error_msg': ERRORS['student_error'] + str(error_students[['fname', 'lname']])}
    return {'status': 0, 'data': student_df}


def create_guardian_student_dict(guardian_df, student_df):
    # Construct guardian_dict {'fname lname': id} and student_dict
    guardian_dict = {}
    for i, guardian in guardian_df.iterrows():
        guardian_name = guardian['fname'] + ' ' + guardian['lname']
        try:
            guardian_name = re.sub(' +', ' ', guardian_name)
        except TypeError as _:
            return {'status': 1, 'error_msg': ERRORS['name_error'] + guardian_name}

        if guardian_name in guardian_dict.keys():
            guardian_dict[guardian_name].append(i+1)
        else:
            guardian_dict[guardian_name] = [i+1]

    student_dict = {}
    for i, student in student_df.iterrows():
        student_name = student['fname'] + ' ' + student['lname']
        try:
            student_name = re.sub(' +', ' ', student_name)
        except TypeError as _:
            return {'status': 1, 'error_msg': ERRORS['name_error'] + student_name}

        if student_name in student_dict:
            student_dict[student_name].append(i+1)
        else:
            student_dict[student_name] = [i+1]
    return {'status': 0, 'data': (guardian_dict, student_dict)}


def create_family_list(family_df, guardian_dict, student_dict):
    # Family table
    family_list = []
    for i, row in family_df.iterrows():
        guardian_names, student_names = None, None
        if not pd.isna(row[0]):
            guardian_names = row[0].split(';')
        if not pd.isna(row[1]):
            student_names = row[1].split(';')
        guardian_ids, student_ids = [], []
        if guardian_names:
            for guardian_name in guardian_names:
                try:
                    guardian_name = re.sub(' +', ' ', guardian_name)
                except TypeError as _:
                    return {'status': 1, 'error_msg': ERRORS['name_error'] + guardian_name}

                if guardian_name in guardian_dict.keys():
                    guardian_ids.append(guardian_dict[guardian_name].pop(0))
        else:
            return {'status': 1, 'error_msg': ERRORS['familyInfo_error'] + str(guardian_names)}

        if student_names:
            for student_name in student_names:
                try:
                    student_name = re.sub(' +', ' ', student_name)
                except TypeError as _:
                    return {'status': 1, 'error_msg': ERRORS['name_error'] + student_name}

                student_ids.append(student_dict[student_name].pop(0))
        else:
            return {'status': 1, 'error_msg': ERRORS['familyInfo_error'] + str(guardian_names)}

        for guardian_id in guardian_ids:
            for student_id in student_ids:
                family_list.append([i+1, guardian_id, student_id])
    return {'status': 0, 'data': family_list}


def load_data(spreadsheet_path):
    res_dict = read_spreadsheet(spreadsheet_path)
    if (res_dict['status'] != 0): return res_dict
    guardian_df, student_df, familyInfo_df = res_dict['data']
    res_dict = create_familyInfo(familyInfo_df)
    if (res_dict['status'] != 0): return res_dict
    family_df, familyInfo_df = res_dict['data']
    res_dict = create_guardian(family_df, guardian_df)
    if (res_dict['status'] != 0): return res_dict
    guardian_df = res_dict['data']
    res_dict = create_student(student_df)
    if (res_dict['status'] != 0): return res_dict
    student_df = res_dict['data']
    res_dict = create_guardian_student_dict(guardian_df, student_df)
    if (res_dict['status'] != 0): return res_dict
    return {'status': 0, 'data': (guardian_df, student_df, familyInfo_df)}


# def create_teacher():
#     # Teacher
#     key_order = ['password', 'first_name', 'last_name',
#                  'email', 'phone', 'class', 'admin']
#     teacher_df = teacher_df[key_order]
#     teacher_df.columns = ['pwd', 'fname', 'lname', 'email', 'phone',
#                           'classes', 'admin']

#     teacher_df['privilege'] = 1
#     teacher_df.loc[teacher_df['admin'] == 'Yes', 'privilege'] = 2
#     teacher_df.loc[teacher_df['admin'] == 'No', 'privilege'] = 1

#     teacher_df = teacher_df.drop('admin', axis=1)
#     teacher_df['phone'] = teacher_df['phone'].apply(lambda x: 't' + str(x))

#     teacher_df['classes'] = teacher_df['classes'].fillna('0')

#     teacher_df.loc[len(teacher_df.index)-1] = ['123456', 'Chang',
#                                                'Liu', 'changliu020@gmail.com', 't8583196032', '0', 2]
#     return {'status': 0, 'data': teacher_df}


# def create_classes(student_df, teacher_df):
#     # Create classes
#     teacher_df.loc[13, 'classes'] = 'Preschool;k&1'

#     classes_teacher, student_classes = {}, {}
#     for i, teacher in teacher_df.iterrows():
#         teacher_id = i + 1
#         for classes_id in teacher['classes'].split(';'):
#             if classes_id not in classes_teacher.keys():
#                 classes_teacher[classes_id] = []
#             classes_teacher[classes_id].append(teacher_id)
#     for i, student in student_df.iterrows():
#         student_id = i + 1
#         student_classes[student_id] = student['classes_id']

#     classes_list = []

#     for i, student in student_df.iterrows():
#         student_id = i + 1
#         classes_id = student_classes[student_id]
#         for teacher_id in classes_teacher[classes_id]:
#             classes_list.append(
#                 {'id': classes_id, 'teacher_id': teacher_id, 'student_id': student_id})

#     return {'status': 0, 'data': classes_list}


# Post to database
# for i, guardian in guardian_df.iterrows():
#     requests.post('http://127.0.0.1:5001/guardian', json=json.loads(guardian.to_json()))

# student_df = student_df.replace('Yes', True)
# student_df = student_df.replace('No', False)

# for i, student in student_df.iterrows():
#     requests.post('http://127.0.0.1:5001/student', json=json.loads(student.to_json()))

# familyInfo_df = familyInfo_df.replace('Yes', True)
# familyInfo_df = familyInfo_df.replace('No', False)

# for i, familyInfo in familyInfo_df.iterrows():
#     requests.post('http://127.0.0.1:5001/familyInfo', json=json.loads(familyInfo.to_json()))

# for family in family_list:
#     family_json = {'id': family[0], 'guardian_id': family[1], 'student_id': family[2], 'is_guest': False}
#     requests.post('http://127.0.0.1:5001/family', json=family_json)

# teacher_df = teacher_df.replace('No', 2)
# teacher_df = teacher_df.replace('Yes', 2)

# teacher_df = teacher_df.rename(columns={'classes': 'classes_id'})

# teacher_df['pwd'] = teacher_df['pwd'].astype(str)

# for i, teacher in teacher_df.iterrows():
#     requests.post('http://127.0.0.1:5001/teacher', json=json.loads(teacher.to_json()))

# for classes in classes_list:
#     requests.post('http://127.0.0.1:5001/classes', json=classes)
