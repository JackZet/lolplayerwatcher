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
        html = html + "<p>You have encountered " + key + " " + val + " times before<p>"
    
    return html

@app.route('/')
def update():
    dbname = getDatabase()
    collection = dbname["players"]
    participants = getParticipants()
    
    if participants:
        encounteredPlayers = returnParticipantsExistingInCollection(participants, collection)
        return buildHTML(encounteredPlayers)
        
    else:
        return '<p>No active game currently</p>'

