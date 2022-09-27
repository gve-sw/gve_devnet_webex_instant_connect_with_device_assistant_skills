from webex_skills.api import MindmeldAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
from webex_skills.models.mindmeld import ProcessedQuery
import requests, json, datetime, ast

api = MindmeldAPI()

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

@api.handle(domain='generation', intent='generate', entities=['date','name'])
async def schedule_meeting(current_state: DialogueState, processed_query: ProcessedQuery) -> DialogueState:
    new_state = current_state.copy()
    #create dictionary to add information to
    meetings_info = {}

    # dictionaries for date, year, and time to convert between the word and the number 
    date_dict = {"1st":"1", "2nd":"2", "3rd":"3", "4th":"4", "5th":"5", "6th":"6", "7th":"7", "8th":"8", "9th":"9", "10th":"10", "11th":"11", "12th":"12", "13th":"13", "14th":"14", "15th":"15", "16th":"16", "17th":"17", "18th":"18", "19th":"19", "20th":"20", "21st":"21", "22nd":"22", "23rd":"23", "24th":"24", "25th":"25", "26th":"26", "27th":"27", "28th":"28", "29th":"29", "30th":"30", "31st":"31"}
    date_dict = dict(date_dict)

    #pull the two entities from the processed query (name and date)
    entity_name = processed_query.entities[0]['text']
    entity_date = processed_query.entities[1]['text']

    #convert date entities from text to numbers 
    entity_date = entity_date.split()
    entity_month = f"{entity_date[0]}"
    date_unformatted = f"{entity_date[1]}"
    entity_day = date_dict.get(date_unformatted)
    entity_year = f"{entity_date[2]}"
    entity_time = f"{entity_date[4]}"

    #recompile now that they are properly formatted 
    updated_entity_date = ""
    updated_entity_date = entity_month + " " + entity_day + " " + entity_year + " " + entity_time

    #format the date entity using datetime then separate the date from the time 
    formattedDate = datetime.datetime.strptime(updated_entity_date, '%B %d %Y %I')

    meetings_info["appointment_time"] = f"{formattedDate.time()}"
    meetings_info["date"] = f"{formattedDate.date()}"

    #type must be skill to schedule the meeting 
    meetings_info["type"] = "skill"

    #separate entity name into first name and last name 
    entity_name = entity_name.split()
    meetings_info["first_name"] = f"{entity_name[0]}"
    meetings_info["last_name"] = f"{entity_name[1]}"
    
    #call the scheduler api to schedule the meeting 
    PORTAL_URL = 'http://127.0.0.1:5000'
    url = PORTAL_URL + '/teleconsultCreate'
    meetings_info = json.dumps(meetings_info)
    meetings_info = str(meetings_info)
    r = requests.post(url, data=meetings_info)
    response_code = r.status_code
    #speak to the user depending on if scheduling the meeting was successful or not 
    if response_code == 200:
        response_text = f"I have scheduled your meeting. Goodbye!"
    else:
        response_text = f"I was unable to schedule a meeting. Please try again."
    new_state.directives = [
        responses.Reply(response_text),
        responses.Speak(response_text),
    ]
    return new_state