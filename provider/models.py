import uuid
from datetime import datetime
from flask import jsonify, request, session, redirect, render_template
from markupsafe import functools, re
from passlib.hash import pbkdf2_sha256
import json
import uuid

from app import providers_db, appointments_db

class Provider:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def create_provider(self):
        provider = {
            "_id": uuid.uuid4().hex,
            "first_name": request.form['first_name'],
		    "last_name": request.form['last_name'],
		    "webex_person_id": request.form['webex_person_id'],
		    "email": request.form['email'],
		    "hours_of_operation": request.form['hours_of_operation'],
		    "timezone": request.form['timezone'],
            "password": request.form['password'],
            "schedule": {}
        }

        # Encrypt the password
        provider['password'] = pbkdf2_sha256.encrypt(provider['password'])

        providers_db.details.insert_one(provider)

        return render_template('signup_success.html')
    
    def login(self):
        data = request.get_json()
        user = providers_db.details.find_one({"email": data['email']})
        print(user)

        if user and pbkdf2_sha256.verify(data['password'], user['password']):
            return self.start_session(user)
        
        return jsonify({"error": "Invalid login credentials"}), 401
    
    def logout(self):
        session.clear()
        print("clearing seesion")
        print(session)
        return redirect('/login')

    def get_all_providers(self):
        allProviders =[]
        cursor_allProviders = providers_db.details.find()
        for providers in cursor_allProviders:
            allProviders.append(providers)
        return jsonify(allProviders)

    def appointments(self):
        data = appointments_db.appointments.find()
        allAppointments =[]
        cursor_allAppointments = appointments_db.appointments.find({'providerId': session['user']['_id']})
        for appointments in cursor_allAppointments:
            allAppointments.append(appointments)
                
        if len(allAppointments) > 1:
            allAppointments = sorted(allAppointments, key=functools.cmp_to_key(self.appointment_compare))

        return jsonify(allAppointments), 200

    # order appointments by day and start time
    def appointment_compare(self, item1, item2):
        # if date is the same, compare by time
        if item1['date'] == item2['date']:
            return int(item1['appointmentTime']) - int(item2['appointmentTime'])
        else:
            temp1 = re.split(r'-', item1['date'])
            temp2 = re.split(r'-', item2['date'])

            # compare by year, then month, then day
            for i in range(0,3):
                if int(temp1[i]) != int(temp2[i]):
                    return int(temp1[i]) - int(temp2[i])

    def free_time(self, date, providerId):
        provider = providers_db.details.find_one({'_id': providerId})

        working_hours = provider['hours_of_operation']

        meeting_length = 60

        # if no entry, return entire working range
        if date not in provider['schedule']:
            return jsonify([working_hours]), 200
        else:
            provider_schedule = provider['schedule'][date]

        new = []

        working_start=datetime.strptime(working_hours[0],"%H:%M")
        working_end=datetime.strptime(working_hours[1],"%H:%M")

        schedule_start=datetime.strptime(provider_schedule[0][0],"%H:%M")
        schedule_end=datetime.strptime(provider_schedule[len(provider_schedule)-1][1],"%H:%M")

        min_start=(working_start-schedule_start).seconds/60
        min_end=(working_end-schedule_end).seconds/60

        if min_start >= float(meeting_length):
            new.append([working_hours[0],provider_schedule[0][0]])

        for i in range(len(provider_schedule)-1):
            if ((datetime.strptime(provider_schedule[i+1][0],"%H:%M")-datetime.strptime(provider_schedule[i][1],"%H:%M")).seconds/60) >=float(meeting_length):
                new.append([provider_schedule[i][1],provider_schedule[i+1][0]])
        if min_end >= float(meeting_length):
            new.append([provider_schedule[len(provider_schedule)-1][1],working_hours[1]])

        return jsonify(new), 200
