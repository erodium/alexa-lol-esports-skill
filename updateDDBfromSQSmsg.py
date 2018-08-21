import boto3
from datetime import datetime
import requests
#from botocore.vendored import requests
import json

LEAGUES= [
    {"name":"NA_LCS",
     "tournament_id":"8531db79-ade3-4294-ae4a-ef639967c393",
     "teams":[
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
    ]},
    {"name":"EU_LCS",
     "tournament_id":"e1e96873-55a3-4a91-8def-e4fe9d461538",
     "teams":[
        {"id":28, "slug":"roccat"},
        {"id":34, "slug":"unicorns-of-love"},
        {"id":15, "slug":"fnatic"},
        {"id":55, "slug":"fc-schalke-04"},
        {"id":165, "slug":"vitality"},
        {"id":33, "slug":"h2k"},
        {"id":54, "slug":"giants-gaming"},
        {"id":228, "slug":"misfits"},
        {"id":97, "slug":"splyce"},
        {"id":163, "slug":"g2-esports"}
    ]}
]

#format items
SCHEDULED_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
ITEM_TEMPLATE= {"nextMatchUTC":"","slug":"","id":"","opponent":""}

#constants
DYNAMODB_TABLE_NAME="teams_na-lcs-id"
SQS_QUEUE_NAME = 'eSportsTeamQueue'

#set up DynamoDB and SQS resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

sqs = boto3.resource('sqs')
queue  = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)

#for each SQS message received, pull updated data from LOLeSports API and update the database
def lambda_handler(event, context):
    overallStatus = 0
    message = event['Records'][0]
    messageBody = json.loads(message['body'])
    leagueName = messageBody['league']
    slug = messageBody['slug']
    teamID = messageBody['id']
    print("Checking " + slug)
    league = next((item for item in LEAGUES if item["name"] == leagueName))
    APIteamData = getTeam(slug, league['tournament_id'])
    APInextScheduledItem = APIteamData['scheduleItems'][0]
    APIteams = APIteamData['teams']
    APIcurrentTeam = APIteams[len(APIteams) - 1]
    APInsiTimeStr = APInextScheduledItem['scheduledTime']
    DBteamData = table.get_item(Key={"id":teamID})
    if 'Item' in DBteamData:
        DBnextMatchTimeStr = DBteamData['Item']['nextMatchUTC']
        if dataHasBeenUpdated(APInsiTimeStr,DBnextMatchTimeStr):
            updateExpression = "SET nextMatchUTC = :p"
            expressionAttributeValue = {":p": APInsiTimeStr}
            table.update_item(Key={"id":teamID},UpdateExpression=updateExpression,ExpressionAttributeValues=expressionAttributeValue)
            print("Updated " + slug + " from " + DBnextMatchTimeStr + " to " + APInsiTimeStr)
        else:
            print("No changes made to " + slug)
    else:
        newItem = ITEM_TEMPLATE.copy()
        newItem['id']=APIcurrentTeam['id']
        newItem['nextMatchUTC'] = APInsiTimeStr
        newItem['slug'] = APIcurrentTeam['slug']
        table.put_item(Item=newItem)
        print("No item found for " + slug + "; created.")
    return(overallStatus)

#determine whether the API returns updated or stale data;
#returns TRUE if data is new, FALSE if data is stale
def dataHasBeenUpdated(APIupdatedAtStr, DBupdatedAtStr):
    TimeAPIupdated = datetime.strptime(APIupdatedAtStr, SCHEDULED_TIME_FORMAT)
    TimeDBupdated = datetime.strptime(DBupdatedAtStr, SCHEDULED_TIME_FORMAT)
    if TimeDBupdated < TimeAPIupdated:
        return True
    return False

#get the team's data from the API
def getTeam(slug, tournamentId):
    r = requests.get("https://api.lolesports.com/api/v1/teams?slug=" + str(slug) + "&tournament=" + str(tournamentId)).json()
    return r