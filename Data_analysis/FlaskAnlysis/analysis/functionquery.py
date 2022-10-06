from pymongo import MongoClient
from CrimeAnalysis.function import update_date_format, update_located_format
from .query import col1,coll,col
import datetime



def connection(connection_url, database_name, collection_name):
    client = MongoClient(connection_url)
    database = client[database_name]
    return database[collection_name]

def verifieduser(connection_name, database_name, collection_name):
    collection = update_date_format(connection_name, database_name, collection_name)
    verified = collection.aggregate([{"$match": {"user.verified": True}}, {"$count": "verified account"}])
    for val in verified:
        verified= val["verified account"]
    return verified    
    
def verified_unverified_user(connection_name, database_name, collection_name):
    collection = update_date_format(
        connection_name, database_name, collection_name)
    verified = collection.aggregate(
        [{"$match": {"user.verified": True}}, {"$count": "verified account"}])
    unverified = collection.aggregate(
        [{"$match": {"user.verified": False}}, {"$count": "inverified account"}])
    output = []
    for val in verified:
        output.append({"verification": "verified",
                      "number": val["verified account"]})
    for val in unverified:
        output.append({"verification": "unverified",
                      "number": val["inverified account"]})
    return output


def case_search_year(connection_name, database_name, collection_name):
    collection1 = update_date_format(
        connection_name, database_name, collection_name)
    curs = collection1.aggregate([{"$group": {"_id": {"year": {
                                 "$year": "$updatedate"}}, "count": {"$sum": 1}}}, {"$sort": {"_id.year": 1}}])
    output = []
    for val in curs:
        output.append(
            {"year": val["_id"]["year"], "count": val["count"]})
    return output


def top_tweet_count(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    curs = collection.aggregate([{"$project": {"user.username": 1,"rawContent":1, "score": {"$sum": [
                                "$replyCount", "$retweetCount", "$likeCount"]}}}, {"$sort": {"score": -1}}, {"$limit": 10}])
    output = []
    for val in curs:
        output.append(
            {"name": val["user"]["username"], "sum": val["score"],"text":val["rawContent"]})
    return output


def topinfluncer_hashtags():
    curs = coll.aggregate([{"$group": {"_id": {"_id": "$_id.user"}, "count": {"$max": "$cnt"}, "username": {
                          "$first": "$username"}, "hashtags": {"$first": "$_id.hashtags"}}}, {"$sort": {"count": -1}}, {"$limit": 25}])
    output = []
    for val in curs:
        output.append(
            {"name": val["username"], "hashtags": val["hashtags"], "count": val["count"]})
    return output

def user_data():
    curs = coll.aggregate([{"$group": {"_id": {"_id": "$_id.user"}, "count": {"$max": "$cnt"}, "username": {
                          "$first": "$username"}, "hashtags": {"$first": "$_id.hashtags"},"verified":{"$first":"$verification"},"follower":{"$first":"$followers"},"friend":{"$first":"$friends"}}}, {"$sort": {"count": -1}}])
    output = []
    for val in curs:
        output.append([val["username"], val["hashtags"],val["verified"],val["follower"],val["friend"]])
    return output

def topinfluncer_url():
    curs = col1.aggregate([{"$group": {"_id": {"_id": "$_id.user"}, "count": {"$max": "$cnt"}, "username": {
                          "$first": "$username"}, "url": {"$first": "$url"}}}, {"$sort": {"count": -1}}, {"$limit": 6}])
    output = []
    for val in curs:
        output.append(
            {"name": val["username"], "steps": val["count"], "pictureSettings":{"src":val["url"]} })
    return output

def location_of_tweet(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    cursor4 = collection.aggregate([{"$group": {"_id": {"name": "$name"}, "value": {"$sum": "$value"}, "code3": {
                                    "$first": "$code3"}, "code": {"$first": "$code"}}}, {"$sort": {"value": -1}}])
    output = []
    for val in cursor4:
        output.append({"code3": val["code3"], "name": val["_id"]
                      ["name"], "value": val["value"], "code": val["code"]})
    return output

def total_number_of_user(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    cur=collection.aggregate([{"$group": { "_id": "null", "myCount": { "$sum": 1 } } }])
    for val in cur:
        total=val["myCount"]
    return total    


    

def location_of_influncer(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    cursor = collection.aggregate([{"$group": {"_id": {"code": "$code"}, "count": {
                                   "$sum": 1}, "code3": {"$first": "$code3"}}}, {"$sort": {"count": -1}}])
    output = []
    for val in cursor:
        output.append(
            {"code3": val["code3"], "z": val["count"], "code": val["_id"]["code"]})
    return output


def user_age_count(connection_name, database_name, collection_name):
    collection2 = update_located_format(
        connection_name, database_name, collection_name)
    cursor = collection2.aggregate(
        [{"$group": {"_id": {"year": {"$year": "$updatedate"}}, "cnt": {"$sum": 1}}}])
    output = []
    currentDate = datetime.date.today()
    for val in cursor:
        age = int(currentDate.strftime("%Y"))-val['_id']["year"]
        output.append({"age": age, "count": val['cnt']})
    output.sort(key=lambda x: x["age"])
    return output



def top_influncer_shared():
    cur = col1.aggregate([{"$group": {"_id": {"year": "$_id.year", "month": "$_id.month", "day": "$_id.day"}, "topinfluncer": {
        "$max": "$cnt"}, "username": {"$first": "$username"}}}, {"$sort": {"topinfluncer": -1}}])
    output = []
    for val in cur:
        output.append({"name": val["username"], "count": val['topinfluncer']})
    return output


def top_hashtags_of_tweet():
    cur = col.aggregate([{"$group": {"_id": {"year": "$_id.year", "month": "$_id.month", "day": "$_id.day"}, "tophashtags": {
        "$max": "$cnt"}, "hashtags": {"$first": "$_id.hashtags"}}}])
    output = []
    for val in cur:
        year = val["_id"]["year"]
        month = val["_id"]["month"]
        day = val['_id']['day']
        output.append({"date": f'{year}-{month}-{day}',
                      "hashtags": val["hashtags"], "count": val['tophashtags']})
    return output

def url_created(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    cursor = collection.aggregate([{"$group":{"_id":{"sourceLabel":"$sourceLabel"},"count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":20}])
    output = []
    for value in cursor:
        output.append({"sourcelabel": value["_id"]["sourceLabel"], "count": value["count"]})
    return output

def all_hashtags(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    cursor = collection.aggregate([{"$unwind": "$hashtags"}, {"$project":{"hashtags": { "$toLower": "$hashtags" }}}, {"$group": {"_id":  {
                                   "hashtags": "$hashtags"}, "cnt": {"$sum": 1}}}, {"$sort": {"cnt": -1}}, {"$limit": 100}])
    output = []
    for value in cursor:
        output.append(
            {"name": value["_id"]["hashtags"], "weight": value["cnt"]})
    return output

def sentiment_anlysis(connection_name, database_name, collection_name):
    collection = connection(connection_name, database_name, collection_name)
    cursor = collection.aggregate([ {"$group": {"_id":  {"sentiment": "$sentiment"}, "cnt": {"$sum": 1}}}])
    cur=collection.aggregate([{"$group": { "_id": "null", "myCount": { "$sum": 1 } } }])
    for val in cur:
        total=val["myCount"]
    output=[]
    for val in cursor:
      number=val["cnt"]
      output.append({"name":val["_id"]["sentiment"],"count":number,"percentage":100*number/total})
       
    return output