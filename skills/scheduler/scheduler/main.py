from webex_skills.api import MindmeldAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
import requests, json, datetime
from datetime import date

api = MindmeldAPI()

PORTAL_URL = 'http://127.0.0.1:5000'

@api.handle(intent='greet', default=True)
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

@api.handle(intent='join')
async def join(current_state: DialogueState) -> DialogueState:
    
    # GET all appointments
    url = PORTAL_URL + '/getAppointments'
    r = requests.get(url, False)
    data = json.loads(r.text)

    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    now = datetime.datetime.now()
    
    today_apt = []
    
    # Find all the appointments for today
    # TODO: Get all appointments for specific provider
    for appointment in data:
        if (appointment['date'] == today_date):
            today_apt.append(appointment)
    
    is_apt = True

    if len(today_apt) == 0:
        is_apt = False
    # Sort the appointments in ascending order
    if (is_apt):
        text = 'Joining current meeting.'
        today_apt.sort(key=lambda x: x['appointmentTime'], reverse=False)

        appointment_to_join = {}

        # Set the upcoming appointment
        for i in today_apt:
            if int(i['appointmentTime']) >= now.hour:
                appointment_to_join = i
                break
        
        # Create the assistant-event payload
        assistant_event_payload = {
            'name': 'join',
            'payload': {
                'sip_uri': appointment_to_join['spaceUri']
            }
        }
        
        new_state = current_state.copy()

        new_state.directives = [
            responses.Reply(text),
            responses.Speak(text),
            responses.AssistantEvent(payload=assistant_event_payload),
            responses.Sleep(10),
        ]
    
    else:
        text = 'Cannot join meeting - You have no meetings scheduled for today.'
        new_state = current_state.copy()
        new_state.directives = [
            responses.Reply(text),
            responses.Speak(text),
            responses.Sleep(10),
        ]


    return new_state
