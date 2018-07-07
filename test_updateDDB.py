import updateDynamoDB
from pprint import pprint
from datetime import datetime

dtg = datetime.utcnow().strftime("%Y-%m-%d")
event = {"time":dtg}
resp=updateDynamoDB.lambda_handler(event, 0)