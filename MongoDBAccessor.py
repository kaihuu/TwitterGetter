from pymongo import MongoClient

#TweetのJSONをMongoDBにインサート
def InsertJSON(Tweet):
    client = MongoClient('localhost', 27017)
    db = client.FSAETwitterDB
    db.TwitterSearchResults.insert(Tweet)



