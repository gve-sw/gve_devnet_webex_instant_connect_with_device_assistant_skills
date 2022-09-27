from flask import render_template
from __main__ import app
from patient.models import Patient
from app import login_required

@app.route('/patient/home')
@login_required
def patientHome():
    return render_template('patient-portal-home.html')

@app.route('/patient/appointments')
@login_required
def myAppointments():
    return render_template('patient-portal-appointments.html')

@app.route('/patient/login')
def patientLogin():
    return render_template('patient-login.html')

@app.route('/patient/login', methods=['POST'])
def login_patient():
    return Patient().login()

@app.route('/patient/logout')
def logout_patient():
    return Patient().logout()

@app.route('/patient/schedule', methods=['GET'])
def schedule():
    return render_template('patient-portal-schedule.html')

@app.route('/patient/schedule', methods=['POST'])
def scheduleApt():
    return Patient().schedule()

@app.route('/patient/notes/<patient>', methods=['GET'])
def notes(patient):
    return render_template('patient-portal-notes.html', patient = patient)

@app.route('/patient/notes/<patient>', methods=['POST'])
def enterNotes(patient):
    return Patient().add_patient_notes(patient)

@app.route('/patient/success')
def success():
    return render_template('patient-schedule-success.html')

@app.route('/patient/my-appointments', methods=['GET'])
def patient_appointments():
    return Patient().appointments()

@app.route('/patient/all', methods=['GET'])
def all_patients():
    return Patient().get_all_patients()