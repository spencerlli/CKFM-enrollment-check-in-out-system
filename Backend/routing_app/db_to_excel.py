import requests
from routing_config import REST_API
import pandas as pd


def get_guardian_df():
    guardian_json = requests.get(REST_API + "/guardian").json()
    guardian_df = pd.DataFrame(guardian_json)
    keys_to_keep = [
        "id",
        "phone",
        "pwd",
        "fname",
        "lname",
        "email",
        "fellow_group",
        "relationship",
    ]
    guardian_df = guardian_df[keys_to_keep]
    guardian_df["class"] = None
    guardian_df = guardian_df[
        [
            "id",
            "phone",
            "pwd",
            "fname",
            "lname",
            "email",
            "class",
            "fellow_group",
            "relationship",
        ]
    ]
    guardian_df.columns = [
        "id",
        "phone_number",
        "password",
        "first_name",
        "last_name",
        "email",
        "class",
        "fellow_group",
        "relationship",
    ]
    return guardian_df


def get_student_df():
    student_json = requests.get(REST_API + "/student").json()
    student_df = pd.DataFrame(student_json)
    student_df["class"] = None
    keys_to_keep = [
        "id",
        "fname",
        "lname",
        "birthdate",
        "gender",
        "class",
        "grade",
        "allergies",
        "check_in_method",
        "sunday_school",
        "cm_lounge",
        "kid_choir",
        "u3_friday",
        "friday_lounge",
        "friday_night",
    ]
    student_df = student_df[keys_to_keep]
    student_df.columns = [
        "id",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "class",
        "grade",
        "allergies",
        "check_in_method",
        "Sunday_school",
        "cm_lounge",
        "kid_choir",
        "u3_Friday",
        "Friday_lounge",
        "Friday_night",
    ]
    return student_df


def get_familyInfo_df():
    familyInfo_json = requests.get(REST_API + "/familyInfo").json()
    familyInfo_df = pd.DataFrame(familyInfo_json)
    keys_to_keep = [
        "id",
        "street",
        "city",
        "state",
        "zip",
        "physician",
        "physician_phone",
        "insurance",
        "insurance_phone",
        "insurance_policy",
        "group",
        "sunday_school",
        "friday_night",
        "special_events",
        "amount_paid",
        "checkbox",
    ]
    familyInfo_df = familyInfo_df[keys_to_keep]
    guardian_df = get_guardian_df()
    student_df = get_student_df()
    family_json = requests.get(REST_API + "/family").json()

    family_names_dict = {}
    for _, row in familyInfo_df.iterrows():
        family_names_dict[row["id"]] = {"guardian_names": [], "student_names": []}

    for family in family_json:
        guardian_id = family["guardian_id"]
        guardian_fname = guardian_df[guardian_df["id"] == guardian_id]["first_name"].values[0]
        guardian_lname = guardian_df[guardian_df["id"] == guardian_id]["last_name"].values[0]
        family_names_dict[family["id"]]["guardian_names"].append(
            guardian_fname + " " + guardian_lname
        )

        student_id = family["student_id"]
        student_fname = student_df[student_df["id"] == student_id]["first_name"].values[0]
        student_lname = student_df[student_df["id"] == student_id]["last_name"].values[0]
        family_names_dict[family["id"]]["student_names"].append(
            student_fname + " " + student_lname
        )

        familyInfo_df["guardian_names"] = familyInfo_df["id"].apply(
            lambda x: ";".join(family_names_dict[x]["guardian_names"])
        )
        familyInfo_df["student_names"] = familyInfo_df["id"].apply(
            lambda x: ";".join(family_names_dict[x]["student_names"])
        )

    return familyInfo_df


def get_teacher_df():
    teacher_json = requests.get(REST_API + "/teacher").json()
    teacher_df = pd.DataFrame(teacher_json)
    keys_to_keep = [
        "fname",
        "lname",
        "pwd",
        "email",
        "phone",
        "classes_id",
        "privilege",
    ]
    teacher_df = teacher_df[keys_to_keep]
    teacher_df.columns = [
        "first_name",
        "last_name",
        "password",
        "email",
        "phone",
        "class",
        "privilege",
    ]
    return teacher_df


if __name__ == "__main__":
    guardian_df = get_guardian_df()
    student_df = get_student_df()
    familyInfo_df = get_familyInfo_df()
    teacher_df = get_teacher_df()

    print(guardian_df)
    print(student_df)
    print(familyInfo_df)
    print(teacher_df)
