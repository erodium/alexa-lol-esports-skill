import boto3
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

SQS_QUEUE_NAME = 'eSportsTeamQueue'

sqs = boto3.resource('sqs')
queue  = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)

def lambda_handler(event, context):
    messages = []
    message = {}
    for league in LEAGUES:
        for team in league['teams']:
            message["Id"] = str(team["id"])
            team["league"] = league["name"]
            message["MessageBody"] = json.dumps(team)
            messages.append(message.copy())
            message.clear()
        response = queue.send_messages(Entries=messages)
        if 'Successful' in response:
            print("Success: " + str(len(response['Successful'])))
        if 'Failed' in response:
            print("Failed: " + str(len(response['Failed'])))
        messages.clear()
