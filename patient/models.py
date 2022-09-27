import uuid, re
from flask import jsonify, request, session, redirect, render_template
from markupsafe import functools
from passlib.hash import pbkdf2_sha256
from app import patients_db, providers_db, appointments_db, patient_notes_db

class Patient:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def create_patient(self):
        patient = {
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
        patient['password'] = pbkdf2_sha256.encrypt(patient['password'])

        patients_db.details.insert_one(patient)

        return render_template('signup_success.html')
    
    def login(self):
        data = request.get_json()
        user = patients_db.details.find_one({"email": data['email']})
        print(user)

        if user and pbkdf2_sha256.verify(data['password'], user['password']):
            return self.start_session(user)
        
        return jsonify({"error": "Invalid login credentials"}), 401
    
    def logout(self):
        session.clear()
        print("clearing seesion")
        print(session)
        return redirect('/login')

    def schedule(self):
        data = request.get_json()
        print(data)
        return render_template('patient-portal-schedule.html')

    def appointments(self):
        # data = appointments_db.appointments.find()
        allAppointments =[]
        cursor_allAppointments = appointments_db.appointments.find({'patientId': session['user']['_id']})
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
                  
    def get_all_patients(self):
        allPatients =[]
        cursor_allPatients = patients_db.details.find()
        for patients in cursor_allPatients:
            allPatients.append(patients)
        return jsonify(allPatients)

    def add_patient_notes(self, patient):
        data = request.get_json()

        patient_entry = patient_notes_db.details.find_one({"patient": patient})

        # Error Check for patient's that don't exist
        
        if patient_entry is None:
            patient_notes = {
                "patient": patient,
                "notes": data['notes']
            }
            patient_notes_db.details.insert_one(patient_notes)
        else:
            new_note = patient_entry['notes'] + data['notes']
            patient_notes_db.details.update_one({'patient': patient}, {'$set': {'notes': new_note}})

        return jsonify({"success": 'Submitted Notes Successfully!'}), 200
