import calendar
import boto3
from datetime import datetime

SKILL_NAME = "N.A.L.C.S."
NA_LCS_TEAMS = ['cloud9', 'team-solomid', 'counter-logic-gaming', 'team-liquid', 'echo-fox', 'flyquest',
                'golden-guardians', 'clutch-gaming', '100-thieves', 'optic-gaming']
DYNAMODB_TABLE_NAME="teams_na-lcs-id"
SCHEDULED_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


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
    print("Starting new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    speechOutput = "Welcome to the N.A.L.C.S. skill. " \
                   "You can ask me for a team's match date by saying, " \
                   "When does Cloud 9 play?"
    reprompt_text = "Please ask me about a team."
    should_end_session = False
    return response(SKILL_NAME, speechOutput, reprompt_text, should_end_session)

def on_intent(request, session):
    intent_name = request['intent']['name']

    if intent_name == "getMatchTime":
        team_id = request['intent']['slots']['myTeam']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        return get_match_response(team_id)

def get_match_response(team_id_str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    team_id = int(team_id_str)
    DBitemData = table.get_item(Key={"id": team_id})
    DBteamData = DBitemData['Item']
    DBdateTime = datetime.strptime(DBteamData['nextMatch'], SCHEDULED_TIME_FORMAT)
    if DBdateTime.hour < 12:
        timeHour = DBdateTime.hour
        dayTime = " A.M."
    else:
        dayTime = " P.M."
        if DBdateTime.hour > 12:
            timeHour = DBdateTime.hour - 12
        else:
            timeHour = 12
    speechOutput = DBteamData['slug'] + " play on " + calendar.day_name[DBdateTime.weekday()] + ", " + calendar.month_name[DBdateTime.month] + " " + str(DBdateTime.day) + " at " + str(timeHour) + dayTime + " Pacific Time."
    return response(SKILL_NAME, speechOutput, speechOutput, True)


def response(title, output, reprompt_text, endsession):
    return {
        'version': '1.0',
        'response': {
            'card': {
                'type': 'Simple',
                'title': title,
                'content': output
            },
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
