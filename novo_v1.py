import tweepy as tw
import json
import datetime
import support as sp

# Fetch keys from the .json config file
with open('./config/twitter_API_config.json') as f:
    keys = json.load(f)
    API_Key = keys["API Key"]
    API_Key_Secret = keys["API Key Secret"]
    Access_Token = keys["Access Token"]
    Access_Token_Secret = keys["Access Token Secret"]
    #Bearer_Token = keys["Bearer Token"]
    f.close()
    del keys

aut = tw.OAuthHandler(API_Key,API_Key_Secret)
aut.set_access_token(Access_Token,Access_Token_Secret)

API = tw.API(aut)

#API.update_status("Este é um tweet de teste!")

#time_line = API.home_timeline()

#for tweet in time_line:
 #   print(f"{tweet.author.name} - {tweet.text}")

start_date = sp.dates()

# Set up the query
tema = "#gsw"
search_query = f"({tema}) (-is:retweet -is:reply)"



imds_tweets = API.search_tweets(
    q = search_query,
    until = start_date
)

for tweet in imds_tweets:
    print(f"{tweet.author.name} - {tweet.text}")
