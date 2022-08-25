from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import requests
import json
import config


app = Flask(__name__)
app.secret_key = '123456'

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

API_URL = "http://localhost:5001"

@app.route('/')
def index():
    return render_template('indexManage.html')


@app.route('/guardian')
def guardian():
    return render_template('indexManage.html')


@app.route('/student')
def student():
    json_data = json.loads(requests.get(API_URL + "/student").content)

    attrs = list(json_data[0].keys())
    attrs = ['id', 'fname', 'lname', 'checked_in', 'barcode', 'checked_out', 'school', 'birthdate',
             'allergies', 'allergies_medication', 'medication', 'emergency_name', 'emergency_phone', 'health_insurance']

    entries = []
    for entry in json_data:
        vals = []
        for attr in attrs:
            vals.append(entry[attr])
        entries.append(vals)

    insert_attrs = ('fname', 'lname', 'school', 'birthdate','allergies', 'allergies_medication', 
                    'medication', 'emergency_name', 'emergency_phone', 'health_insurance')

    return render_template('student.html', attrs=attrs, entries=entries, insert_attrs=insert_attrs, enumerate=enumerate)


@app.route('/student/insert', methods=['POST'])
def studentInsert():
    if request.method == "POST":
        form = dict(request.form)
        response = requests.post(API_URL + '/student', json=form)
        print(response.json)
        flash("Data Inserted Successfully")

        return redirect(url_for('student'))


@app.route('/student/update/<int:id>', methods=['POST', 'GET'])
def studentUpdate(id):
    if request.method == 'POST':
        form = dict(request.form)
        response = requests.put(API_URL + '/student/' + str(id), json=form)
        flash("Data Updated Successfully")
        return redirect(url_for('student'))


@app.route('/student/delete/<int:id>', methods=['GET'])
def studentDelete(id):
    response = requests.delete(API_URL + '/student/' + str(id))
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('student'))


if __name__ == "__main__":
    app.run(debug=True)
