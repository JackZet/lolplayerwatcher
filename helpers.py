import requests as req

#Replace the string with your riot games API key
def getAPIkey():
    return 'RGAPI-YOUR-API-KEY'

#Replace the string with your summoner name
def getSummonerName():
    return 'Summoner Name'

def getSummonerInfo():
    response = req.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{getSummonerName()}?api_key={getAPIkey()}").json()
    encryptedSummonerID = response.get("id", False)
    puuid = response.get("puuid", False)
    if not encryptedSummonerID:
        print("There was an error retrieving encrypted summoner ID for", getSummonerName())
    if not puuid:
        print("There was an error retrieving puuid for", getSummonerName())
    
    return (encryptedSummonerID, puuid)

def getEncryptedSummonerID():
    encryptedSummonerID, _ = getSummonerInfo()
    return encryptedSummonerID

def getPuuid():
    _, puuid = getSummonerInfo()
    return puuid
        
def create_item(match_id, game_id, game_mode, game_type, summonerName, team, win, role, champion, remarks):
    item = {
        "match_id" : match_id,
        "game_id" : game_id,
        "game_mode" : game_mode,
        "game_type" : game_type,
        "summonerName" : summonerName,
        "team" : team,
        "win" : win,
        "role" : role,
        "champion" : champion,
        "remarks" : remarks
    }
    return item
