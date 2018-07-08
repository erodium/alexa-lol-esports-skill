import calendar
import boto3
from datetime import datetime
from pytz import timezone
from boto3.dynamodb.conditions import Key

PYTZ_TIMEZONES=["US/Pacific","US/Mountain","US/Central","US/Eastern"]

SKILL_NAME = "N.A.L.C.S."
MATCH_TABLE_NAME= "teams_na-lcs-id"
USER_TABLE_NAME = "esportsSkillCustomerSettings"
SCHEDULED_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

dynamoDB = boto3.resource('dynamodb')
matchTable = dynamoDB.Table(MATCH_TABLE_NAME)
userTable = dynamoDB.Table(USER_TABLE_NAME)

tzItems = ["US/Pacific", "US/Mountain", "US/Central", "US/Eastern"]


def lambda_handler(event, context):
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        print("Session Ended.")

def on_session_started(session_started_request, session):
    print("Started new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    speechOutput = "Welcome to the N.A.L.C.S. skill. " \
                   "You can ask me for a team's match date by saying, " \
                   "When does Cloud 9 play? Or set your time zone by saying," \
                    "use eastern time."
    reprompt_text = "Please ask me about a team."
    should_end_session = False
    return response(SKILL_NAME, speechOutput, reprompt_text, should_end_session)

def on_intent(request, session):
    intent_name = request['intent']['name']
    userID = session['user']['userId']
    resp = userTable.query(
        KeyConditionExpression=Key('userID').eq(userID)
    )
    if resp['Count'] == 0:
        userItem['userID'] = userID
        userItem['preferredTimeZone'] = 0
        userTable.put_item(
            Item={userItem}
        )
        print("New user created.")
    else:
        userItem = resp['Items'][0]

    if intent_name == "getMatchTime":
        request_id = request['intent']['slots']['myTeam']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        return get_match_response(request_id, userItem['preferredTimeZone'])
    elif intent_name == "setTimeZone":
        request_id = request['intent']['slots']['myTimeZone']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        return set_time_zone_response(userItem['userID'], request_id)

def set_time_zone_response(userID, timeZoneID):
    updateExpression = "SET preferredTimeZone = :p"
    expressionAttributeValue = {":p": timeZoneID}
    userTable.update_item(Key={"userID": userID}, UpdateExpression=updateExpression,
                      ExpressionAttributeValues=expressionAttributeValue)
    print("Updated user to timezone " + timeZoneID)
    speechOutput = "Updated user to timezone " + timeZoneID
    return response(SKILL_NAME,speechOutput,speechOutput,False)

def get_match_response(team_id_str, tzID_str):
    team_id = int(team_id_str)
    tzID = int(tzID_str)
    DBitemData = matchTable.get_item(Key={"id": team_id})
    DBteamData = DBitemData['Item']
    DBdateTime = datetime.strptime(DBteamData['nextMatchUTC'], SCHEDULED_TIME_FORMAT)
    tzString = tzItems[tzID]
    pdt = timezone(tzString)
    pdtDateTime = pdt.normalize(DBdateTime.astimezone(pdt))
    if pdtDateTime.hour < 12:
        timeHour = pdtDateTime.hour
        dayTime = " A.M."
    else:
        dayTime = " P.M."
        if pdtDateTime.hour > 12:
            timeHour = pdtDateTime.hour - 12
        else:
            timeHour = 12
    speechOutput = DBteamData['slug'] + " play on " + calendar.day_name[pdtDateTime.weekday()] + ", " + calendar.month_name[pdtDateTime.month] + " " + str(pdtDateTime.day) + " at " + str(timeHour) + dayTime + " " + tzString[3:]
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
