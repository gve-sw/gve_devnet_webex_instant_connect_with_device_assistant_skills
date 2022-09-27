""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

# Import Section
import os, requests, time, random, json, uuid, re
from markupsafe import functools
from flask import Flask, render_template, request, redirect, session, redirect
from dotenv import load_dotenv
from webexteamssdk import WebexTeamsAPI
from pymongo import MongoClient
from bson.json_util import dumps
from functools import wraps
from passlib.hash import pbkdf2_sha256

# load all environment variables
load_dotenv()

# Global variables
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
  
    return wrap

# connect to MongoDb
client = MongoClient(os.environ.get("MONGO_DB_URL"))
appointments_db = client.appointments
admin_db = client.admin
providers_db = client.providers
patients_db = client.patients
patient_notes_db = client.patient_notes

## Routes
from admin import routes
from provider import routes
from patient import routes

@app.route('/teleconsultCreate',methods = ['POST', 'GET'])
def teleconsultCreate():
    data = json.loads(request.data)

    print(request.data)
    # Patient is scheduling meeting
    if (data['type'] == 'patient'):
        patientName = session['user']['first_name'] + ' ' + session['user']['last_name']
        patientId = session['user']['_id']
        providerFirstName = providers_db.details.find_one({'_id': data['provider']})['first_name']
        providerLastName = providers_db.details.find_one({'_id': data['provider']})['last_name']
        providerName = providerFirstName + ' ' + providerLastName
        providerId = data['provider']
        patient = patients_db.details.find_one({'_id': patientId})
        provider = providers_db.details.find_one({'_id': providerId})

    # Provider is scheduling meeting
    elif (data['type'] == 'provider'):
        providerName = session['user']['first_name'] + ' ' + session['user']['last_name']
        providerId = session['user']['_id']
        patientFirstName = patients_db.details.find_one({'_id': data['patient']})['first_name']
        patientLastName = patients_db.details.find_one({'_id': data['patient']})['last_name']
        patientName = patientFirstName + ' ' + patientLastName
        patientId = data['patient']
        patient = patients_db.details.find_one({'_id': patientId})
        provider = providers_db.details.find_one({'_id': providerId})

    #Skill is scheduling meeting 
    elif (data['type'] == 'skill'):
        providerName = 'gerardo chaves'
        providerId = '12341234'
        patientFirstName = data['first_name']
        patientLastName = data['last_name']
        patientName = patientFirstName + ' ' + patientLastName
        patientId = '20222022'
        patient = {
            "schedule": {}
        }
        provider = {
            "schedule": {}
        }
         

    date = data['date']
    if data['type'] == 'skill':
        appointmentTime = data['appointment_time'][0]
    else:
        appointmentTime = data['appointment_time']

    # add to patient and provider schedule

    schedule = scheduler(patient['schedule'], date, appointmentTime)

    # TODO: patient already has appointment in slot!.... some kind of block
    # if schedule is None:
    #     return jsonify(None), 400

    patients_db.details.update_one({'_id': patientId}, {'$set': {'schedule': schedule}})
    
    schedule = scheduler(provider['schedule'], date, appointmentTime)

    providers_db.details.update_one({'_id': providerId}, {'$set': {'schedule': schedule}})

    if request.method == 'POST':
        IC_API_URL = os.environ.get("IC_API_URL")
        IC_SPACE_API_URL = os.environ.get("IC_SPACE_API_URL")
        IC_AUDIENCE = os.environ.get("IC_AUDIENCE")
        IC_ACCESS_TOKEN = os.environ.get("IC_ACCESS_TOKEN")
        IC_URL_DURATION = os.environ.get("IC_URL_DURATION")
        IC_AGENT_BASEURL = os.environ.get("IC_AGENT_BASEURL")
        IC_CLIENT_BASEURL = os.environ.get("IC_CLIENT_BASEURL")
        IC_HOST_BASEURL = os.environ.get("IC_HOST_BASEURL")

        result = request.form
        resultDict=dict(request.form)

        print(result)
        print(resultDict)

        theWebexID=""
        confirmedBaseSubject="Virtual Appointment " + str(random.randint(1,25555))

        url = IC_API_URL

        payload = json.dumps({
            "aud": IC_AUDIENCE,
            "jwt": {
                "sub": confirmedBaseSubject, #using same subject will return same consultation always!,
                "exp": int(time.time())  + int(IC_URL_DURATION)
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ IC_ACCESS_TOKEN
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        print(response.text)
        theHost=response_dict['host'][0]
        theGuest=  response_dict['guest'][0]
        print(theHost)
        print(theGuest)

        # now obtain the spaceID and token
        url = IC_SPACE_API_URL+"?int=jose&data="+theHost
        response = requests.request("GET", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        print(response.text)
        theToken=response_dict['token']
        theSpaceID=response_dict['spaceId']
        print(f'access token: {theToken}')

        #obtain the space meeting URI
        api = WebexTeamsAPI(access_token=theToken)
        theResult = api.rooms.get_meeting_info(theSpaceID)
        add_to_database(theResult, theHost, theGuest, confirmedBaseSubject, patientName, patientId, providerName, providerId, appointmentTime, date)
        print(f'Meetings info for the space: {theResult}')
        theSpaceSIP=theResult.sipAddress
        theMeetingNumber=theResult.meetingNumber

        #if webex ID to add was provided, add them to the space
        if theWebexID!='':
            theResult=api.memberships.create(theSpaceID,personEmail=theWebexID)
            print("Added to space: ",theResult)
        
        return redirect('patient/success', 302)

        # return render_template("result.html",
        #                        basehost=IC_HOST_BASEURL,
        #                        baseagent=IC_AGENT_BASEURL,
        #                        baseguest=IC_CLIENT_BASEURL,
        #                        host=theHost,
        #                        guest=theGuest,
        #                        spaceid=theSpaceID,
        #                        spaceURI=theSpaceSIP,
        #                        participant=theWebexID,
        #                        token=theToken)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/consult')
def consult():
    IC_BASE_SUBJECT = os.environ.get("IC_BASE_SUBJECT")
    return render_template('consult.html',theBase=IC_BASE_SUBJECT)

@app.route('/')
def index():
    return redirect('/login')


# Supporting methods

def add_to_database(theResult, host, guest, subject, patientName, patientId, providerName, providerId, appointmentTime, date):
    data = {
        '_id': uuid.uuid4().hex,
        "baseSubject": subject,
        "patientName": patientName,
        "patientId": patientId,
        "providerName": providerName,
        "providerId": providerId,
        "hostUrl": os.environ.get("IC_HOST_BASEURL") + host,
        "agentUrl": os.environ.get("IC_AGENT_BASEURL") + host,
        "guestUrl": os.environ.get("IC_CLIENT_BASEURL") + guest,
        "spaceUri": theResult.sipAddress,
        "appointmentTime": appointmentTime,
        "date": date
    }
    appointments_db.appointments.insert_one(data)

def getAppointmentsForPatient(patient):
    return json.loads(dumps(appointments_db.appointments.find({'patientName': patient})))

def scheduler(schedule, date, appointmentTime):
    # Check if day exists in calander (if not add it)
    if date not in schedule:
        schedule[date] = []

    print(schedule)

    print(appointmentTime)

    # Generate Appointment time in proper format
    timeSlot = []
    timeSlot.append(appointmentTime + ':' + '00')
    timeSlot.append(str(int(appointmentTime) + 1) + ':' + '00')

    # TODO: if timeslot already present, return None
    # if timeSlot in schedule[date]:
    #     return None

    # insert into schedule
    schedule[date].append(timeSlot)

    if len(schedule[date]) > 1:
        schedule[date] = sorted(schedule[date], key=functools.cmp_to_key(slot_compare))

    print(schedule)
    return schedule

# order slots
def slot_compare(item1, item2):
    item1_list = re.split(r':', item1[0])
    item2_list = re.split(r':', item2[0])

    item1_list[0] = int(item1_list[0])
    item1_list[1] = int(item1_list[1])

    item2_list[0] = int(item2_list[0])
    item2_list[1] = int(item2_list[1])

    # if hour is the same, check minutes
    if item1_list[0] == item2_list[0]:
        return item1_list[1] - item2_list[1]
    else:
        return item1_list[0] - item2_list[0]



if __name__ == "__main__":
    # Check if admin account exists in DB and if not, create one
    if admin_db.users.find_one({}) is None:
        admin = {
            "_id": uuid.uuid4().hex,
            "name": "Admin",
            "email": "admin@cisco.com",
            "password": "admin"
        }

        # Encrypt the password
        admin['password'] = pbkdf2_sha256.encrypt(admin['password'])

        admin_db.users.insert_one(admin)
    else:
        pass

    app.run(port=5000,debug=True)
