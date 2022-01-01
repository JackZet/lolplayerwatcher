import pymongo
from pymongo import MongoClient

def addListToCollection(toAdd, collection):
    collection.insert_many(toAdd)

def printDocumentsFromCursor(cursor):
    for doc in cursor:
        print(doc)

        
def getDatabase():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://<user>:<password>@<cluster-name>.w7emo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['lol']
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = getDatabase()
    collection_name = dbname["player_names"]
