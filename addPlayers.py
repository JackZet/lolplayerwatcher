import requests as req
from helpers import create_item, getAPIkey, getPuuid, getSummonerName
from db import getDatabase, addListToCollection
import time

def getRecentMatches(count):
    #Endpoint: Get recent matches
    print("Checking for recent matches...")
    response = req.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{getPuuid()}/ids?start=0&count={count}&api_key={getAPIkey()}")
    matches = response.json()
    return matches

def addSummonersFromMatchToCollection(matchID, collection):
    #Endpoint get game info via match id
    response = req.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={getAPIkey()}").json()

    info = response.get('info', False)
    if info:
        summoners = getSummonersFromMatch(matchID, info)
        print("Adding players to collection")
        addListToCollection(summoners, collection)
    else:
        print("Was no info on match id:", matchID)

def addSummonersFromMatchesToCollection(matches, collection):
    for matchID in matches:
        col = collection.find({"match_id": matchID})
        
        #If we already inserted the players for a particular matchID we stop the loop.
        #The early stop is due to the retrieved match list being sorted by newest to oldest.
        #If we reach a matchID in the list that is already in the database, we know that the subsequent
        #matches are also in the database.
        matchAlreadyAddedInDB = len(list(col)) > 0
        if matchAlreadyAddedInDB:
            break
    
        addSummonersFromMatchToCollection(matchID, collection)
        
def getMyTeam(participants):
    for p in participants:
        if p['summonerName'] == getSummonerName():
            myTeam = p['teamId']
    return myTeam

def getSummonersFromMatch(matchID, info):
    summoners = []
    gameID = info['gameId']
    gameMode = info['gameMode']
    gameType = info['gameType']
    participants = info['participants']
    myTeam = getMyTeam(participants)

    #For every participant in the game we extract their info
    for p in participants:
        summonerName = p['summonerName']

        #Exclude own summoner
        if summonerName == getSummonerName():
            continue
        
        #Check if summoner was a teammate or an opponent
        team = p['teamId']
        if team == myTeam:
            team = "Teammate"
        else:
            team = "Opponent"
    
        win = p['win']
        role = p['role']
        champion = p['championName']

        #Create the db item
        dItem = create_item(matchID, gameID, gameMode, gameType, summonerName, team, win, role, champion, "")
        
        #Append the item to a list
        summoners.append(dItem)
    return summoners

def main():
    
    #10 min = 600 sec
    sleepTime = 600
    
    dbname = getDatabase()
    collection = dbname['players']
    
    while True:
        matches = getRecentMatches(20)
        print(matches)
        addSummonersFromMatchesToCollection(matches, collection)
        print("Waiting", sleepTime, "seconds before next check.")
        time.sleep(sleepTime)

if __name__ == '__main__':
    main()
