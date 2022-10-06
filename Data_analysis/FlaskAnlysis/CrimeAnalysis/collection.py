from function import collecting_twitter_data_seacrh,collecting_twitter_data_hashtags,connect_twitterdata_to_mongodb_locally,tweet_location_shared,user_location_shared,connection,get_tweets

search_query = "criminal OR crime OR stabbing OR school shooting OR murder OR sexual assault OR murder OR kidnapping OR terrorist OR terrorism OR crime death OR crime emigrants OR crime gun OR war  OR war crime OR Explosions  mass destruction OR mass murder OR genocide OR terrorism OR treason OR crimes against peace OR breach of authority OR libel OR assault OR blackmail OR usurpation OR kidnapping OR desertion OR sowing discord OR  mass destruction for war crimes OR  killer cases"
hashtag_query = "#crime OR #school_shooting OR #terrorists OR #WarCrimial OR  #PalestineUnderAttack OR  #GazaUnderAttack OR #Guns  OR #war OR #WarCrimes OR  #RussianWarCrimes OR  #StopRussiaNOW OR  #UkraineRussiaWar OR #Ukraine OR #RussianWarCrimes OR #RussiaIsATerroristState  OR #russiaisateroriststate OR #terrorism OR #Terror OR #counterterrorism OR #DomesticTerrorism OR #criminaljustice OR #CrimeNews "

since_date="2020-01-01"
filename="FlaskAnlysis\CrimeAnalysis\data.json"
file="FlaskAnlysis\CrimeAnalysis\data"

collecting_twitter_data_seacrh(search_query,since_date,10,filename)
collecting_twitter_data_hashtags(hashtag_query,since_date,10,filename)
connect_twitterdata_to_mongodb_locally('twitter_db','twitter_collection',file)
tweet_location_shared()
user_location_shared()
collection= connection("mongodb://localhost:27017", "twitter_db", "twitter_collection")
cursor=collection.find()
get_tweets(cursor)