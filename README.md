# lolplayerwatcher

Requirements:
- Python3
- Requests module
- PyMongo module

Use "pip3 install requests" and "pip3 install pymongo" 

Before running:
1. In helpers.py fill in your riot API key in the getAPIkey function
2. In helpers.py fill in your summoner name in the getSummonerName function
3. Create a free database using MongoDB and copy the connection string from your cluster into db.py in the CONNECTION_STRING variable

How to run:
- Run "python3 addPlayers.py" and "python3 checkPlayers.py"

Region:
- The endpoints in the code is for euw players. If you are on another region go to riot games api and change the endpoints in the code to your own region.
