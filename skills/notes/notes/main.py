from webex_skills.api import MindmeldAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState, ProcessedQuery

api = MindmeldAPI()

# Set this Portal URL to be the URL of the portal
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


@api.handle(intent='note')
async def patient_notes(current_state: DialogueState, processed_query: ProcessedQuery) -> DialogueState:
    new_state = current_state.copy()

    # Response
    if(len(processed_query.entities) > 0):
        entity = processed_query.entities[0]
        if entity['type'] == 'patients':
            text = f'Ok, please enter notes for {entity["text"]} now. When you are done, say "tell notes to close notes"'
    
    # TODO: else: some kind of error here?

    url = PORTAL_URL + f'/patient/notes/{entity["text"]}'

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.DisplayWebView(url, title="Patient Notes"),
        responses.Sleep(10)
    ]

    return new_state


@api.handle(intent='close_note')
async def patient_notes(current_state: DialogueState, processed_query: ProcessedQuery) -> DialogueState:
    new_state = current_state.copy()

    # Response
    text = 'Okay, closing notes.'
    
    # TODO: else: some kind of error here?

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.ClearWebView(),
        responses.Sleep(10)
    ]

    return new_state