from pymongo import MongoClient
from CrimeAnalysis.function import update_date_format, update_located_format


collection1 = update_date_format(
    "mongodb://localhost:27017", "twitter_db", "twitter_collection")

client = MongoClient("mongodb://localhost:27017")
database = client["twitter_db"]



collection1.aggregate([{"$unwind": "$user"}, {"$unwind": "$hashtags"}, {"$group": {"_id": {"user": "$user.id", "hashtags": "$hashtags"}, "username": {
                      "$first": "$user.username"},"verification":{"$first":"$user.verified"},"followers":{"$first":"$user.followersCount"},"friends":{"$first":"$user.friendsCount"} ,"cnt": {"$sum": 1}}}, {"$out": "TopInfluencers_hashtags"}])
coll = database["TopInfluencers_hashtags"]


collection1.aggregate([{"$unwind": "$user"}, {"$group": {"_id": {"year": {"$year": "$updatedate"}, "month": {"$month": "$updatedate"}, "day": {
                      "$dayOfMonth": "$updatedate"}, "user": "$user.id"},"url":{"$first": "$user.profileImageUrl"}, "username": {"$first": "$user.username"}, "cnt": {"$sum": 1}}}, {"$sort": {"cnt": -1}}, {"$out": "CountTopInfluencers"}])
col1 = database["CountTopInfluencers"]


collection1.aggregate([{"$unwind": "$hashtags"},{"$group": {"_id": {"year": {"$year": "$updatedate"}, "month": {"$month": "$updatedate"}, "day": {"$dayOfMonth": "$updatedate"}, "hashtags": "$hashtags"},"cnt": {"$sum": 1}}}, {"$sort": {"cnt": -1}}, {"$out": "counthashtags"}])
col= database['counthashtags']