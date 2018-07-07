import json, requests

# taken from Scub3d GitHub
# https://gist.github.com/Scub3d/0523abc590028ff0e2fd6fda0fb4fa48/revisions#diff-7238b98fca276f97b70357d3d97584c1

# Start of request functions

LEAGUE_SLUGS = ["none", "all-star", "na-lcs", "eu-lcs", "na-cs", "eu-cs", "lck", "lpl-china", "lms", "worlds", "msi"]

def getLeagues(_id=None, slug=None):
	if(_id == None and slug == None):
		r = requests.get("http://api.lolesports.com/api/v1/leagues").json()
	elif(_id == None and slug != None):
		r = requests.get("http://api.lolesports.com/api/v1/leagues?slug=" + str(slug)).json()
	elif(_id != None and slug == None):
		r = requests.get("http://api.lolesports.com/api/v1/leagues?id=" + str(_id)).json()
	elif(_id != None and slug != None):
		r = requests.get("http://api.lolesports.com/api/v1/leagues?id=" + str(_id) + "?slug=" + str(slug)).json()
	return r

def getScheduleItems(leagueId):
    if isinstance(leagueId, str):
        leagueId = LEAGUE_SLUGS.index(leagueId)
    if leagueId > 0 and leagueId < len(LEAGUE_SLUGS):
        r = requests.get("http://api.lolesports.com/api/v1/scheduleItems?leagueId=" + str(leagueId)).json()
        return r
    else:
        return({'error':'invalid leagueID in getScheduleItems'})

def getTeam(slug, tournamentId):
	r = requests.get("http://api.lolesports.com/api/v1/teams?slug=" + str(slug) + "&tournament=" + str(tournamentId)).json()
	return r

def getPlayer(slug, tournamentId):
	r = requests.get("http://api.lolesports.com/api/v1/players?slug=" + str(slug) + "&tournament=" + str(tournamentId)).json()
	return r

def getTournaments(leagueId):
	if isinstance(leagueId, str) and leagueId in LEAGUE_SLUGS:
		leagueId = LEAGUE_SLUGS.index(leagueId)
	if isinstance(leagueId, int) and leagueId > 0 and leagueId < len(LEAGUE_SLUGS):
		r = requests.get("http://api.lolesports.com/api/v2/highlanderTournaments?league=" + str(leagueId)).json()
	else:
		r = {'error':'invalid leagueID in getTournaments'}
	return r

def getMatchDetails(tournamentId, matchId):
	r = requests.get("http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=" + str(tournamentId) + "&matchId=" + str(matchId)).json()
	return r

def getPlayerStats(tournamentId):
	r = requests.get("http://api.lolesports.com/api/v2/tournamentPlayerStats?tournamentId=" + str(tournamentId)).json()
	return r

def getArticles(language=None, _from=None):
	if(language == None and _from == None):
		r = requests.get("http://api.lolesports.com/api/v1/articles").json()
	elif(language == None and _from != None):
		r = requests.get("http://api.lolesports.com/api/v1/articles?from=" + str(_from)).json()
	elif(language != None and _from == None):
		r = requests.get("http://api.lolesports.com/api/v1/articles?language=" + str(language)).json()
	elif(language != None and _from != None):
		r = requests.get("http://api.lolesports.com/api/v1/articles?language=" + str(language) + "?from=" + str(_from)).json()
	return r

def getMarquees(locale):
	r = requests.get("http://api.lolesports.com/api/v1/marquees?locale=" + locale).json()
	return r

def getHTMLBlocks():
	r = requests.get("http://api.lolesports.com/api/v1/htmlBlocks").json()
	return r

def getVideos():
	r = requests.get("http://api.lolesports.com/api/v2/videos").json()
	return r

def getStreamGroups():
	r = requests.get("http://api.lolesports.com/api/v2/streamgroups").json()
	return r

def getGameStats(gameRealm, gameId, gameHash):
	r = requests.get("https://acs.leagueoflegends.com/v1/stats/game/" + str(gameRealm) + "/" + str(gameId) + "?gameHash=" + str(gameHash), verify=False).json()
	return r

def getGameTimeline(gameRealm, gameId, gameHash):
	r = requests.get("https://acs.leagueoflegends.com/v1/stats/game/" + str(gameRealm) + "/" + str(gameId) + "/timeline?gameHash=" + str(gameHash), verify=False).json()
	return r

# End of request functions
# Start of URL functions

def getLeaguesURL(_id=None, slug=None):
	if(_id == None and slug == None):
		return "http://api.lolesports.com/api/v1/leagues"
	elif(_id == None and slug != None):
		return "http://api.lolesports.com/api/v1/leagues?slug=" + str(slug)
	elif(_id != None and slug == None):
		return "http://api.lolesports.com/api/v1/leagues?id=" + str(_id)
	elif(_id != None and slug != None):
		return "http://api.lolesports.com/api/v1/leagues?id=" + str(_id) + "?slug=" + str(slug)

def getScheduleItemsURL(leagueId):
	return "http://api.lolesports.com/api/v1/scheduleItems?leagueId=" + str(leagueId)

def getTeamURL(slug, tournamentId):
	return "http://api.lolesports.com/api/v1/teams?slug=" + str(slug) + "&tournament=" + str(tournamentId)

def getPlayerURL(slug, tournamentId):
	return "http://api.lolesports.com/api/v1/players?slug=" + str(slug) + "&tournament=" + str(tournamentId)

def getTournamentsURL(leagueId):
	return "http://api.lolesports.com/api/v2/highlanderTournaments?league=" + str(leagueId)

def getMatchDetailsURL(tournamentId, matchId):
	return "http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=" + str(tournamentId) + "&matchId=" + str(matchId)

def getPlayerStatsURL(tournamentId):
	return "http://api.lolesports.com/api/v2/tournamentPlayerStats?tournamentId=" + str(tournamentId)

def getArticlesURL(language=None, _from=None):
	if(language == None and _from == None):
		return "http://api.lolesports.com/api/v1/articles"
	elif(language == None and _from != None):
		return "http://api.lolesports.com/api/v1/articles?from=" + str(_from)
	elif(language != None and _from == None):
		return "http://api.lolesports.com/api/v1/articles?language=" + str(language)
	elif(language != None and _from != None):
		return "http://api.lolesports.com/api/v1/articles?language=" + str(language) + "?from=" + str(_from)

def getMarqueesURL(locale):
	return "http://api.lolesports.com/api/v1/marquees?locale=" + locale

def getHTMLBlocksURL():
	return "http://api.lolesports.com/api/v1/htmlBlocks"

def getVideosURL():
	return "http://api.lolesports.com/api/v2/videos"

def getStreamGroupsURL():
	return "http://api.lolesports.com/api/v2/streamgroups"

def getGameStatsURL(gameRealm, gameId, gameHash):
	return "https://acs.leagueoflegends.com/v1/stats/game/" + str(gameRealm) + "/" + str(gameId) + "?gameHash=" + str(gameHash)

def getGameTimelineURL(gameRealm, gameId, gameHash):
	return "https://acs.leagueoflegends.com/v1/stats/game/" + str(gameRealm) + "/" + str(gameId) + "/timeline?gameHash=" + str(gameHash)

# End of URL functions




# Random Stuff
"""
def parseLeagues(json):
	for league in json["leagues"]:
		tournaments = getTournaments(league["id"])
		for tournament in tournaments["highlanderTournaments"]:
			if tournament["title"] == "lck_2016_summer":
				#for gameId in tournament["gameIds"]:
					#print gameId, tournament["id"]
					#print getMatchDetails(tournament["id"], gameId)
					#print "ok"
				print tournament["id"]



		
def getAllMatchURLS():
	matchDetailsURLs = []
	leaguesJSON = getLeagues()
	for league in leaguesJSON["leagues"]:
		tournaments = getTournaments(league["id"])
		for tournament in tournaments["highlanderTournaments"]:
			if tournament["title"] == "na_2016_summer":
				for bracket in tournament["brackets"]:
					for matchId in tournament["brackets"][bracket]["matches"]:
						matchDetailsURLs = getMatchDetailsURL(tournament["id"], matchId)
						print matchDetailsURLs

if __name__ == '__main__':
	#parseLeagues(getLeagues())
	#print len("6ccafe25-5e3c-4d9a-a67e-b4c3358df4de")
	#requestMatchDetails("91be3d78-874a-44e0-943f-073d4c9d7bf6", "22851f97-7555-494d-b234-1e4bbeaf8dd5")
	#print getGameStats("TRLH1", "1001440530", "8111bf29dfce9731")
	#doScheduleItems()
	#getAllMatchURLS()

	print parseLeagues(getLeagues())
"""

