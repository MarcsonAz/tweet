from http import client
import tweepy as tw
import json
import datetime
import pandas as pd
import support as sp

if __name__ == '__main__':

   #pegar configuracoes
        # diretorio
        # pegar ultima data com valor
        # definir conteudo da busca

   #pegar credenciais
        # ler aquivo com credenciais
        # colocar credenciais no client

   #fazer query

    wd = sp.get_wd()
    subject = sp.get_subject()
    start_date = sp.dates()
    client = sp.auth()


    # Set up the query
    search_query = f"({subject}) (-is:retweet -is:reply)"


    if False:
        input("Warning: No more data are available, you have to wait at least 1 hour to send another request")
        exit(0)
    else:
        tweet_count = client.search_recent_tweets(
            query=search_query,
            #granularity="day",
            #until=start_date
            start_time=start_date,
            max_results=100
        )

    
    for t in tweet_count:
        print(t)

   