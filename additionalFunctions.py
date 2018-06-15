


def get_match_response(team_name):
    date_time_string = get_match_datetime_api(team_name)
    datetime_obj = convert_date_time(date_time_string)
    match_day = calendar.day_name[calendar.weekday(datetime_obj.year, datetime_obj.month, datetime_obj.day)]
    match_month = calendar.month_name[datetime_obj.month]
    match_date = str(datetime_obj.day)
    speechOutput = team_name + " play on " + match_day + " " + match_month + " " + match_date + "."
    return response(SKILL_NAME, speechOutput, speechOutput, True)


def get_match_datetime_api(slug):
    if slug in NA_LCS_TEAMS:
        tourn_id = "8531db79-ade3-4294-ae4a-ef639967c393"
    elif slug in EU_LCS_TEAMS:
        tourn_id = "e1e96873-55a3-4a91-8def-e4fe9d461538"
    else:
        tourn_id = ""
    api_url = "http://api.lolesports.com/api/v1/teams?slug=" + slug + "&tournament=" + tourn_id
    api_resp = requests.get(api_url)
    next_match = api_resp.json()['scheduleItems'][0]['scheduledTime']
    return (next_match)


def convert_date_time(date_time_string):
    format1 = "%Y-%m-%dT%H:%M:%S.%f%z"
    new_date = datetime.strptime(date_time_string, format1)
    return (new_date)

def old_get_match_response(team_name):
    bucket = "alexa-esports-times"
    key = "na-lcs/"+team_name + ".json"
    content_object = s3.Object(bucket, key)

    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    match_json = json_content['matches'][0]
    match_day = calendar.day_name[calendar.weekday(match_json['year'], match_json['month'], match_json['date'])]
    pdtTime = match_json['pdtHour']
    if pdtTime > 12:
        pdtTime -= 12
    speechOutput = team_name + " play " + match_json['opponent'] + " on " + match_day + " " + match_json[
        'monthName'] + " " + match_json['pdtDate'] + " at " + str(pdtTime) + " P.M."
    return response(SKILL_NAME, speechOutput, speechOutput, True)