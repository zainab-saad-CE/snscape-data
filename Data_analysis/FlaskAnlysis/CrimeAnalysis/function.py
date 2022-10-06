from CrimeAnalysis import twitter as twitterScraper
import json
from pymongo import MongoClient
import pycountry
import re
from textblob import TextBlob


def collecting_twitter_data_seacrh(search_query,since_date,data_number,file_name):
     query_search ="" + search_query + " since:" + str(since_date) 
     scraper_search = twitterScraper.TwitterSearchScraper(query_search)
     file = open(str(file_name))
     for i, tweet in enumerate(scraper_search.get_items()):
        if i > data_number:
            break
        file.write(tweet.json()+"\n")
     file.close()

def collecting_twitter_data_hashtags(hashtag_query,since_date,data_number,file_name):
     query_hastags = "" + hashtag_query + " since:" + str(since_date) 
     scraper_hastag = twitterScraper.TwitterHashtagScraper(query_hastags)
     file = open(str(file_name))
     
     for i, tweet in enumerate(scraper_hastag.get_items()):
        if i > data_number:
            break
        file.write(tweet.json()+"\n")
     file.close()


def connect_twitterdata_to_mongodb_locally(db_name,coll_name,filename):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[coll_name]
    tweet = [json.loads(line) for line in open('{}.json'.format(filename), 'r')]
    collection.insert_many(tweet)
    
def update_date_format(connection,db_name,coll_name):   
    client =MongoClient(connection)
    database = client[db_name]
    collection = database[coll_name]  
    cursor = collection.aggregate([{"$project": {"hashtags": 1,"mentionedUsers": 1,"user":1, "updatedate": { "$dateFromString": {"dateString": "$date"}}}}, {"$out": "changeformatofdate"}])
    collection1 = database["changeformatofdate"]
    return collection1

def update_located_format(connection,db_name,coll_name):   
    client =MongoClient(connection)
    database = client[db_name]
    collection = database[coll_name]  
    cursor = collection.aggregate([{"$project": {"user": 1, "updatedate": { "$dateFromString": {"dateString": "$user.created"}}}}, {"$out": "changeformatofcreateddate"}])
    collection1 = database["changeformatofcreateddate"]
    return collection1


def tweet_location_shared():
    client = MongoClient("mongodb://localhost:27017")
    database = client["twitter_db"]
    collection = database["twitter_collection"]
    database["location"].drop()
    cursor1 = collection.aggregate(  [{"$group": {"_id": {"user": "$user.location"},"cnt":{"$sum":1}}},{"$sort":{"cnt":-1}}])
    output=[]
    for val in cursor1:
        for country in pycountry.countries:
            if country.name in val["_id"]["user"]:
                output.append({"code3":country.alpha_3,"name":country.name,"value":val["cnt"],"code":country.alpha_2})               
    database["location"].insert_many(output) 
      
def user_location_shared():
    client = MongoClient("mongodb://localhost:27017")
    database = client["twitter_db"]
    collection = database["twitter_collection"]
    database["locationofinfluncer"].drop()
    cursor2=collection.aggregate([{"$unwind": "$user"}, {"$group": {"_id": {"user": "$user.id"},"location":{"$first":"$user.location"}}}])
    output2=[]
    for val in cursor2:
        for country in pycountry.countries:
            if country.name in val["location"]:
                output2.append({"code3":country.alpha_3,"userid":val["_id"]["user"],"code":country.alpha_2})          
    database["locationofinfluncer"].insert_many(output2) 
    
def connection(connection_url, database_name, collection_name):
    client = MongoClient(connection_url)
    database = client[database_name]
    return database[collection_name]

def clean_tweet(tweet):
   return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment( tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
def get_tweets(query):
        client = MongoClient("mongodb://localhost:27017")
        database = client["twitter_db"]
        # empty list to store parsed tweets
        tweets = []
  
    
        #  call twitter api to fetch tweets
  
        # parsing tweets one by one
        for tweet in query:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
  
                # saving text of tweet
                parsed_tweet['text'] = tweet["rawContent"]
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = get_tweet_sentiment(tweet["rawContent"])
  
                # appending parsed tweet to tweets list
                if tweet["retweetCount"] > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
        database["sentiment"].insert_many(tweets)
              