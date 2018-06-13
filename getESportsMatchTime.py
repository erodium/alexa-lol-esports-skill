import calendar
import boto3
import json

SKILL_NAME = "eSports"
NA_LCS_TEAMS = ['cloud9', 'team-solomid', 'counter-logic-gaming', 'team-liquid', 'echo-fox', 'flyquest',
                'golden-guardians', 'clutch-gaming', '100-thieves', 'optic-gaming']
EU_LCS_TEAMS = ['fnatic', 'gambit-gaming', 'sk-gaming', 'roccat', 'millenium', 'h2k', 'unicorns-of-love',
                'copenhagen-wolves', 'giants-gaming', 'fc-schalke-04', 'origen', 'splyce', 'g2-esports', 'vitality',
                'huma', 'misfits', 'mysterious-monkeys', 'ninjas-in-pyjamas']

s3 = boto3.resource('s3')


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
            request['intent']['slots']['myTeam']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value'][
                'id']
        return get_match_response(team_name)


def get_match_response(team_name):
    bucket = "alexa-esports-times"
    key = "na-lcs/"+team_name + ".json"
    content_object = s3.Object(bucket, key)

    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    match_json = json_content['matches'][0]
    match_day = calendar.day_name[calendar.weekday(match_json['year'], match_json['month'], match_json['date'])]
    pdtTime = match_json['pdtHour']
    if pdtTime > 12:
        pdtTime -= 12
    speechOutput = team_name + " play " + match_json['opponent'] + " on " + match_day + " " + match_json[
        'monthName'] + " " + match_json['pdtDate'] + " at " + str(pdtTime) + " P.M."
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
