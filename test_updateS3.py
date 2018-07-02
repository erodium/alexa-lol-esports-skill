import updateS3bucket
from pprint import pprint
from datetime import datetime

dtg = datetime.utcnow().strftime("%Y-%m-%d")
event = {"time":dtg}
resp=updateS3bucket.lambda_handler(event,0)