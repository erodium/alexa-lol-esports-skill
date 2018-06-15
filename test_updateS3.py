import updateS3bucket
from pprint import pprint

resp=updateS3bucket.lambda_handler(0,0)
pprint(resp)