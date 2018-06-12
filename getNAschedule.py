import json
import boto3
from pprint import pprint

with open("naSchedule.json") as f:
    data = json.load(f)

tournaments_array = data["highlanderTournaments"]
S3fileName = []
tourneys = []
brackets = []


for tourney in tournaments_array:
    tourneys.append(tourney)
    agg = tourney['title'] + ".json"
    S3fileName.append((agg))
    for bracket in tourney['brackets']:
        brackets.append(bracket)
        pprint(bracket)



for fileName in S3fileName:
    print(fileName)

for bracket in brackets:
    pprint(bracket)


