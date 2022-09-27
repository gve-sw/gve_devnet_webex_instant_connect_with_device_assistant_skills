from webex_skills.api import MindmeldAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
import requests, json, datetime
from datetime import date

api = MindmeldAPI()


PORTAL_URL = 'http://127.0.0.1:5000'
#PORTAL_URL = 'https://0b58-209-188-53-160.ngrok.io'

@api.handle(intent = 'show', default=True)
async def show(current_state: DialogueState) -> DialogueState:
    text = 'show skill'

    new_state = current_state.copy()

    url = PORTAL_URL + '/getAppointments'
    r = requests.get(url, False)
    data = json.loads(r.text)

    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    now = datetime.datetime.now()

    today_apt = []

    # Find all the apts for today
    #TODO: Get all appointments for specific provider
    for appointment in data:
        if (appointment ['date'] == today_date):
            today_apt.append(appointment)

    #Sort appointments in ascending order
    today_apt.sort(key=lambda x: x['appointmentTime'],reverse=False)

    num_meetings = len(today_apt)

    meetingsPlural = "meetings"

    if (num_meetings == 1):
        meetingsPlural = "meeting"
    

    response_text = "You have {num_meetings} {meetingsPlural} today.".format(num_meetings=num_meetings, meetingsPlural = meetingsPlural)
    print(today_apt[0]["patientName"])
    
    #print(today_apt[0][10])

    for i in range(len(today_apt)):
        time = today_apt[i]["appointmentTime"]
        timeInt = int(time)
        if (timeInt > 12):
            timeInt = timeInt - 12
        
        response_text += " You have a meeting with {name} at {time}.".format(name=today_apt[i]["patientName"], time=timeInt)


    new_state.directives = [
        responses.Reply(response_text),
        responses.Speak(response_text),
        responses.Sleep(10),
    ]

    return new_state




@api.handle(intent='greet')
async def greet(current_state: DialogueState) -> DialogueState:
    text = 'Hello I am a super simple skill using NLP'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state


@api.handle(intent='exit')
async def goodbye(current_state: DialogueState) -> DialogueState:
    text = 'Have a nice day!'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state
