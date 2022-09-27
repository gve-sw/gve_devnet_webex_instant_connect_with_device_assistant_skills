from flask import render_template, request
from __main__ import app
import json
from provider.models import Provider

from app import login_required

@app.route('/provider/login')
def providerLogin():
    return render_template('provider-login.html')

@app.route('/provider/login', methods=['POST'])
def login_provider():
    return Provider().login()

@app.route('/provider/home')
@login_required
def providerHome():
    return render_template('provider-portal-home.html')

@app.route('/provider/appointments')
@login_required
def providerAppointments():
    return render_template('provider-portal-appointments.html')

@app.route('/provider/logout')
def logout():
    return Provider().logout()

@app.route('/provider/all', methods=['GET'])
def get_all_providers():
    return Provider().get_all_providers()

@app.route('/provider/my-appointments', methods=['GET'])
def provider_appointments():
    return Provider().appointments()

@app.route('/provider/free-time', methods=['POST'])
def free_time():
    data = json.loads(request.data)
    return Provider().free_time(data['date'], data['provider'])

@app.route('/provider/schedule', methods=['GET'])
def provider_schedule():
    return render_template('provider-portal-schedule.html') 

