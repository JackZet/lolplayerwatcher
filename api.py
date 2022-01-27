from flask import Flask
from checkPlayers import getParticipants
from db import getDatabase

app = Flask(__name__)

def returnParticipantsExistingInCollection(participants, collection):
    
    encounteredPlayers = {}
    
    for p in participants:
                summonerName = p['summonerName']
                col = collection.find({"summonerName": summonerName})
                
                encounters = len(list(col))
                
                if encounters > 0:
                    encounteredPlayers[summonerName] = encounters
                    
    return encounteredPlayers

def buildHTML(encounteredPlayers):
    html = ""
    
    for key, val in encounteredPlayers.items():
        html = html + "<p>You have encountered " + key + " " + int(val) + " times before<p>"
    
    return html

@app.route('/')
def update():
    dbname = getDatabase()
    collection = dbname["players"]
    participants = getParticipants()
    
    if participants:
        encounteredPlayers = returnParticipantsExistingInCollection(participants, collection)
        
        if len(encounteredPlayers) > 0:
            return buildHTML(encounteredPlayers)
        
        return '<p>You have not met any of the summoners before</p>'    
        
        
    else:
        return '<p>No active game currently</p>'

