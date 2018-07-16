#import updateDynamoDB
from pprint import pprint
from datetime import datetime

"""
dtg = datetime.utcnow().strftime("%Y-%m-%d")
event = {"time":dtg}
resp=updateDynamoDB.lambda_handler(event, 0)
"""
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

event = {
	'Records': [{
		'messageId': '682de6c3-6314-43f1-94e6-c8c3b42afa1b',
		'receiptHandle': 'AQEBSvV4cI75vpMOYPTgnEbqJVm086Ic3gYC67X8ugmrhXtw2W7r3XzRRI0cqb/LFYefG5FPHbJKzOz9VslTJVF5+VMeXPVFrE+ch2bMQlhTigoRgImZfvmfk/WvuEZig48I6YtMfMJQxMdkPDnTYnqfzVgXVRz9RROK2KCMVionQVBMdIEr2kpxELXXz4nqx5aKDwV9KajuQ7/3tJvS0xfp28a7yHsav/y0619IHHdm7qqAIE3LkkNnjeXugQUeLD5T1uRTmkHpfmq/QG2MH814tQVthX7Z7njWjoiN8fNz73KkUtnUjAk10UFPQLlsH+ABTIrUa2CSwKMZ5+Ls1BnZInouAxRB1eIXsDmJDqtj7NJP5Hb8KtPe0L9uhRWn6ClD56F4hye0C7+ngRxcl9IWQA==',
		'body': '{"league": "NA_LCS", "slug": "cloud9", "id": 18}',
		'attributes': {
			'ApproximateReceiveCount': '1',
			'SentTimestamp': '1531686806365',
			'SenderId': '438961634630',
			'ApproximateFirstReceiveTimestamp': '1531686806376'
		},
		'messageAttributes': {

		},
		'md5OfBody': '91b053c4d0c8bc411f87608d56b3ae4e',
		'eventSource': 'aws: sqs',
		'eventSourceARN': 'arn: aws: sqs: us-west-2: 438961634630: eSportsTeamQueue',
		'awsRegion': 'us-west-2'
	}]
}

#import updateDDBfromSQSmsg

#updateDDBfromSQSmsg.lambda_handler(event, 0)

import updateDDBqueuer
updateDDBqueuer.lambda_handler(0,0)