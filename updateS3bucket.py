import boto3
from datetime import datetime
#from botocore.vendored import requests
import requests
import pytz
from pytz import timezone
import logging

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

ITEM_TEMPLATE= {"updatedAt":"","slug":"","nextMatch":""}
DYNAMODB_TABLE_NAME="teams_na-lcs-id"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    print("Update requested at " + event['time'])
    overallStatus = 0
    for team in NA_LCS_TEAMS:
        logger.info("starting %s", team['slug'])
        APIteamData = getTeam(team['slug'], NA_TOURN_ID)
        APInextScheduledItem = APIteamData['scheduleItems'][0]
        APIteams = APIteamData['teams']
        APIcurrentTeam = APIteams[len(APIteams) - 1]
        APInsiTimeStr = APInextScheduledItem['scheduledTime'][:-5]
        DBteamData = table.get_item(Key={"id":team['id']})
        if 'Item' in DBteamData:
            DBnextMatchTimeStr = DBteamData['Item']['nextMatch']
            if dataHasBeenUpdated(APInsiTimeStr,DBnextMatchTimeStr):
                logger.info("Updating %s from %s to %s", team['slug'], APInsiTimeStr, DBnextMatchTimeStr)
                pdt = timezone('US/Pacific')
                APInsiDTO = datetime.strptime(APInsiTimeStr, SCHEDULED_TIME_FORMAT)
                utc_dt = pytz.utc.localize(APInsiDTO)
                pdt_dt = utc_dt.astimezone(pdt)
                pdtNSIstr = pdt_dt.strftime(SCHEDULED_TIME_FORMAT)
                updateExpression = "SET nextMatch = :m"
                expressionAttributeValue = {":m": pdtNSIstr}
                table.update_item(Key={"id":team['id']},UpdateExpression=updateExpression,ExpressionAttributeValues=expressionAttributeValue)
                print(team['slug'])
            else:
                logger.info("No changes made to %s", team['slug'])
        else:
            logger.info("No item found for %s; creating", team['slug'])
            newItem = ITEM_TEMPLATE.copy()
            newItem['id']=APIcurrentTeam['id']
            newItem['updatedAt'] = APIcurrentTeam['updatedAt']
            newItem['slug'] = APIcurrentTeam['slug']
            pdt = timezone('US/Pacific')
            APInsiDTO = datetime.strptime(APInextScheduledItem['scheduledTime'][:-5],SCHEDULED_TIME_FORMAT)
            utc_dt = pytz.utc.localize(APInsiDTO)
            pdt_dt = utc_dt.astimezone(pdt)
            pdtNSIstr = pdt_dt.strftime(SCHEDULED_TIME_FORMAT)
            newItem['nextMatch'] = pdtNSIstr
            table.put_item(Item=newItem)
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