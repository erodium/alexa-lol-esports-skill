import boto3
from datetime import datetime
#from botocore.vendored import requests
import requests
import pytz
from pytz import timezone

NA_TOURN_ID="8531db79-ade3-4294-ae4a-ef639967c393" #should go away when this supports multiple tournaments
NA_LCS_TEAMS = [
        {"id":18, "slug":"cloud9"},
        {"id":11, "slug":"team-solomid"},
        {"id":23, "slug":"counter-logic-gaming"},
        {"id":53, "slug":"team-liquid"},
        {"id":169, "slug":"echo-fox"},
        {"id":264, "slug":"flyquest"},
        {"id":405, "slug":"golden-guardians"},
        {"id":406, "slug":"clutch-gaming"},
        {"id":407, "slug":"100-thieves"},
        {"id":408, "slug":"optic-gaming"}
    ]
UPDATED_AT_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
SCHEDULED_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

ITEM_TEMPLATE= {"nextMatchUTC":"","slug":"","nextMatchPDT":"","id":""}
DYNAMODB_TABLE_NAME="teams_na-lcs-id"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def lambda_handler(event, context):
    print("Update requested at " + event['time'])
    overallStatus = 0
    for team in NA_LCS_TEAMS:
        APIteamData = getTeam(team['slug'], NA_TOURN_ID)
        APInextScheduledItem = APIteamData['scheduleItems'][0]
        APIteams = APIteamData['teams']
        APIcurrentTeam = APIteams[len(APIteams) - 1]
        APInsiTimeStr = APInextScheduledItem['scheduledTime'][:-5]
        DBteamData = table.get_item(Key={"id":team['id']})
        if 'Item' in DBteamData:
            DBnextMatchTimeStr = DBteamData['Item']['nextMatchUTC']
            if dataHasBeenUpdated(APInsiTimeStr,DBnextMatchTimeStr):
                pdt = timezone('US/Pacific')
                APInsiDTO = datetime.strptime(APInsiTimeStr, SCHEDULED_TIME_FORMAT)
                utc_dt = pytz.utc.localize(APInsiDTO)
                pdt_dt = utc_dt.astimezone(pdt)
                pdtNSIstr = pdt_dt.strftime(SCHEDULED_TIME_FORMAT)
                updateExpression = "SET nextMatchUTC = :m, nextMatchPDT = :p"
                expressionAttributeValue = {":m": pdtNSIstr, ":p": APInsiTimeStr}
                table.update_item(Key={"id":team['id']},UpdateExpression=updateExpression,ExpressionAttributeValues=expressionAttributeValue)
                print("Updated " + team['slug'] + " from " + APInsiTimeStr + " to " + DBnextMatchTimeStr)
            else:
                print("No changes made to " + team['slug'])
        else:
            newItem = ITEM_TEMPLATE.copy()
            newItem['id']=APIcurrentTeam['id']
            newItem['nextMatchUTC'] = APInsiTimeStr
            newItem['slug'] = APIcurrentTeam['slug']
            pdt = timezone('US/Pacific')
            APInsiDTO = datetime.strptime(APInextScheduledItem['scheduledTime'][:-5],SCHEDULED_TIME_FORMAT)
            utc_dt = pytz.utc.localize(APInsiDTO)
            pdt_dt = utc_dt.astimezone(pdt)
            pdtNSIstr = pdt_dt.strftime(SCHEDULED_TIME_FORMAT)
            newItem['nextMatchPDT'] = pdtNSIstr
            table.put_item(Item=newItem)
            print("No item found for " + team['slug'] + "; created.")
    return(overallStatus)


def dataHasBeenUpdated(APIupdatedAtStr, DBupdatedAtStr):
    TimeAPIupdated = datetime.strptime(APIupdatedAtStr, SCHEDULED_TIME_FORMAT)
    TimeDBupdated = datetime.strptime(DBupdatedAtStr, SCHEDULED_TIME_FORMAT)
    if TimeDBupdated < TimeAPIupdated:
        return True
    return False


def getTeam(slug, tournamentId):
    r = requests.get("https://api.lolesports.com/api/v1/teams?slug=" + str(slug) + "&tournament=" + str(tournamentId)).json()
    return r