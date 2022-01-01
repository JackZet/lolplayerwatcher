import requests as req
from helpers import getAPIkey, getEncryptedSummonerID, getAPIkey
from db import getDatabase, printDocumentsFromCursor
import time

def checkIfParticipantsExistInCollection(participants, collection):
    for p in participants:
                summonerName = p['summonerName']
                col = collection.find({"summonerName": summonerName})
                
                encounters = len(list(col))
                
                if encounters > 0:
                    print("You have encountered", summonerName, encounters, "times before!")
                    printDocumentsFromCursor(col)
                    

def getParticipants():  
    #Endpoint: Get live match based on summonerID
    response = req.get(f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{getEncryptedSummonerID()}?api_key={getAPIkey()}").json()
    participants = response.get("participants", False)
    
    return participants

def main():
    
    #5 min = 300 sec
    sleepTime = 300

    dbname = getDatabase()
    collection = dbname["players"]

    while True:
        print("Checking for active game...")
        #If reponse body contains participants then there is an active game
        participants = getParticipants()
        if participants:
            checkIfParticipantsExistInCollection(participants, collection)
        else:
            print("No active game currently")
        
        print("Waiting", sleepTime, "seconds before next check.")
        time.sleep(sleepTime)

if __name__ == "__main__":
    main()
