from flask import render_template, request, jsonify, redirect
from __main__ import app

from markupsafe import re
from admin.models import Admin
from bson.json_util import dumps
from passlib.hash import pbkdf2_sha256
import uuid, json

from app import appointments_db, providers_db, patients_db, login_required

@app.route('/admin/signup', methods=['POST'])
def signup():
    return Admin().signup()

@app.route('/admin/login', methods=['POST'])
def admin_login():
    return Admin().login()

@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    return Admin().logout()

@app.route('/admin/home', methods=['GET'])
@login_required
def admin_home():
    return render_template('index.html')

@app.route('/admin/patients', methods=['GET'])
@login_required
def admin_patients():
    return render_template('patients.html')

@app.route('/admin/providers', methods=['GET'])
@login_required
def admin_providers():
    return render_template('providers.html')

@app.route('/admin/appointments', methods=['GET'])
@login_required
def admin_appointments():
    return render_template('appointments.html')

@app.route('/admin/login', methods=['GET'])
def admin_login_page():
    return render_template('admin-login.html')

@app.route('/getAppointments',methods = ['GET'])
def getAppointments():
    data = json.loads(dumps(appointments_db.appointments.find({})))
    return jsonify(data)

@app.route('/admin/sign_up_provider', methods=['POST'])
def signUpProvider():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    webex_person_id = request.form['webex_person_id']
    email = request.form['email']
    hours_of_operation = request.form['hours_of_operation']
    timezone = request.form['timezone']
    password = request.form['password']


    # Get hours of operation in right format (24h, converted)
    working_hours_provider = []
    temp = re.split(r'-', hours_of_operation)

    #TODO: assumption made here (9-10 is 9 am to 10 am, but a 9-8 is 9 am to 8 pm) -> could enforce people specifying?
    if int(temp[1]) <= int(temp[0]):
        temp[1] = str(int(temp[1]) + 12)

    working_hours_provider.append(temp[0] + ':00')
    working_hours_provider.append(temp[1] + ':00')


    data = {
        "_id": uuid.uuid4().hex,
        "first_name": first_name,
		"last_name": last_name,
		"webex_person_id":webex_person_id,
		"email": email,
		"hours_of_operation": working_hours_provider,
		"timezone": timezone,
        "password": password,
        "schedule": {}
    }

    # Encrypt the password
    data['password'] = pbkdf2_sha256.encrypt(data['password'])

    providers_db.details.insert_one(data)
    return render_template('signup_success.html')

@app.route("/admin/allProviders", methods=['POST'])
def all():
    allProviders =[]
    cursor_allProviders = providers_db.details.find()
    for providers in cursor_allProviders:
        allProviders.append(providers)
    return render_template('allProviders.html', allProviders = allProviders)

@app.route("/admin/allPatients", methods=['GET'])
def allPatients():
    data = json.loads(dumps(patients_db.details.find({})))
    return jsonify(data)

@app.route("/admin/patients/all", methods=['GET'])
def allPatientsView():
    return render_template('allPatients.html')

@app.route("/admin/sign_up_patient", methods=['POST'])
def signUpPatient():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    record_number = request.form['record_number']
    password = request.form['password']

    data = {
        "_id": uuid.uuid4().hex,
        "first_name": first_name,
		"last_name": last_name,
		"email": email,
        "password": password,
		"phone_number": phone_number,
		"record_number": record_number,
        "password": password,
        "schedule": {}
    }

    # Encrypt the password
    data['password'] = pbkdf2_sha256.encrypt(data['password'])

    patients_db.details.insert_one(data)
    return redirect('/admin/patients/all')