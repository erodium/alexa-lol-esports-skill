from datetime import datetime
import calendar
from botocore.vendored import requests

SKILL_NAME = "eSports"
NA_LCS_TEAMS = ['cloud9', 'team-solomid', 'counter-logic-gaming', 'team-liquid', 'echo-fox', 'flyquest',
                'golden-guardians', 'clutch-gaming', '100-thieves', 'optic-gaming']
EU_LCS_TEAMS = ['fnatic', 'gambit-gaming', 'sk-gaming', 'roccat', 'millenium', 'h2k', 'unicorns-of-love',
                'copenhagen-wolves', 'giants-gaming', 'fc-schalke-04', 'origen', 'splyce', 'g2-esports', 'vitality',
                'huma', 'misfits', 'mysterious-monkeys', 'ninjas-in-pyjamas']


def lambda_handler(event, context):
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


def on_session_started(session_started_request, session):
    print ("Starting new session.")


def on_launch(launch_request, session):
    return get_welcome_response()


def get_welcome_response():
    speechOutput = "Welcome to the eSports skill. " \
                   "You can ask me for a team's match date by saying, " \
                   "When does Cloud 9 play next?"
    reprompt_text = "Please ask me when a team plays next."
    should_end_session = False
    return response(SKILL_NAME, speechOutput, reprompt_text, should_end_session)


def on_intent(request, session):
    intent_name = request['intent']['name']

    if intent_name == "getMatchTime":
        team_name = \
        request['intent']['slots']['myTeam']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        return get_match_response(team_name)


def get_match_response(team_name):
    date_time_string = get_match_datetime_api(team_name)
    datetime_obj = convert_date_time(date_time_string)
    match_day = calendar.day_name[calendar.weekday(datetime_obj.year, datetime_obj.month, datetime_obj.day)]
    match_month = calendar.month_name[datetime_obj.month]
    match_date = str(datetime_obj.day)
    speechOutput = team_name + " play on " + match_day + " " + match_month + " " + match_date + "."
    return response(SKILL_NAME, speechOutput, speechOutput, True)


def get_match_datetime_api(slug):
    if slug in NA_LCS_TEAMS:
        tourn_id = "8531db79-ade3-4294-ae4a-ef639967c393"
    elif slug in EU_LCS_TEAMS:
        tourn_id = "e1e96873-55a3-4a91-8def-e4fe9d461538"
    api_url = "http://api.lolesports.com/api/v1/teams?slug=" + slug + "&tournament=" + tourn_id
    api_resp = requests.get(api_url)
    next_match = api_resp.json()['scheduleItems'][0]['scheduledTime']
    return (next_match)


    format1 = "%Y-%m-%dT%H:%M:%S.%f%z"
    new_date = datetime.strptime(date_time_string, format1)
    return (new_date)


def response(title, output, reprompt_text, endsession):
    return {
        'version': '1.0',
        'response': {
            'card': {
                'type': 'Simple',
                'title': title,
                'content': output
            },
def convert_date_time(date_time_string):
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'reprompt': {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": reprompt_text
                }
            },
            'shouldEndSession': endsession
        }
    }