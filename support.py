import tweepy as tw
import json
import datetime
import pandas as pd

if __name__ == '__main__':

    path = input("""Where do you want to store data ?
    >> """)

    # Open the last saved data in the .csv file
    last_subject = 0
    try:
        last_fetch = pd.read_csv(rf"Data\{path}.csv", engine='c').tail(1)
        last_data_date = datetime.datetime.strptime(
            last_fetch.iat[0, 0], '%Y-%m-%d %H:%M:%S'
        )
        last_subject = last_fetch.columns[2]
    except Exception as e:
        last_data_date = False
        write_header = True
        print(fr"""{e}
csv file does not exist or is empty.

...Data\tweet_count_data.csv and header's labels created.

...Start date to fetch set form seven days ago
    """)
    else:
        del last_fetch
        write_header = False

    if last_subject:
        if input(f"""The previous subject was {last_subject}, do you want to keep it ? (y/n)
    >> """) == "y":
            subject = last_subject
        else:
            subject = input("""What subject do you want to count ?
    >> """)
    else:
        subject = input("""What subject do you want to count ?
    >> """)

   
    # Set up the query
    search_query = f"({subject}) (-is:retweet -is:reply)"

    # Set up the start date
    local_date = datetime.datetime.now()
    if last_data_date:
        last_data_date += datetime.timedelta(seconds=3600)
        start_date = f"{last_data_date.year}-{last_data_date.month}-{last_data_date.day}T{last_data_date.hour}:00:00.00z"
    else:
        start_date = local_date - datetime.timedelta(days=7)
        start_date = f"{start_date.year}-{start_date.month}-{start_date.day}T{start_date.hour}:00:00.00z"

    # Get tweet count
    end_date = local_date - datetime.timedelta(seconds=3600)
    end_date = f"{end_date.year}-{end_date.month}-{end_date.day}T{end_date.hour}:00:00.00z"

    if start_date == end_date:
        input("Warning: No more data are available, you have to wait at least 1 hour to send another request")
        exit(0)
    else:
        tweet_count = client.get_recent_tweets_count(
            query=search_query,
            granularity="hour",
            start_time=start_date,
            end_time=end_date
        )

    # Create a DataSet
    new_data={
        'date':[],
        'tweet count':[],
        f'{subject}': None
    }
    for count in tweet_count[0]:
        tw_date = datetime.datetime.strptime(
            count['start'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        new_data['date'].append(tw_date)
        new_data['tweet count'].append(count['tweet_count'])

    new_data = pd.DataFrame(new_data)

    new_data.to_csv(
                    fr"Data\{path}.csv",
                    mode='a',
                    index=False,
                    header=write_header
                    )

    print("Data fetched to .csv file:")
    print(new_data)


def get_wd():
    wd = "C:/imds/tweet/data/"
    new_wd = input(fr"""Diretorio para armazenar dados
    >> {wd}
    pressione enter para mante-lo
    digite "mudar" para muda-lo  
    """)
    if new_wd.lower() == "mudar":
       wd = input(fr"""Digite o caminho para novo diretorio
    >> """)

    return wd


def get_subject():

    subject = input("""What subject do you want to count ?
    >> """)
    
    return subject

def dates(n_anterior = 0):
    entrada = input(fr"""Dados até hoje ::::> zero dias atrás
    pressione enter para mante-lo
    digite um número para muda-lo  
    """)
    if entrada:
        if int(entrada) != 0:
            n_anterior = int(entrada)


        # Set up the start date
    local_date = datetime.datetime.now()
    if n_anterior != 0:
        start_date = local_date - datetime.timedelta(days=n_anterior)
        start_date = f"{start_date.year}-{start_date.month}-{start_date.day}T{start_date.hour}:00:00.00z"
    else:
        start_date = f"{local_date.year}-{local_date.month}-{local_date.day}T{local_date.hour}:00:00.00z"

    return start_date

    # Get tweet count
    ##end_date = local_date - datetime.timedelta(seconds=3600)
    #end_date = f"{end_date.year}-{end_date.month}-{end_date.day}T{end_date.hour}:00:00.00z"


def auth():
    # Fetch keys from the .json config file
    with open('./config/twitter_API_config.json') as f:
        keys = json.load(f)
        API_Key = keys["API Key"]
        API_Key_Secret = keys["API Key Secret"]
        Access_Token = keys["Access Token"]
        Access_Token_Secret = keys["Access Token Secret"]
        Bearer_Token = keys["Bearer Token"]
        f.close()
        del keys

    # Authenticate to the API
    client = tw.Client(Bearer_Token, API_Key, API_Key_Secret,
                    Access_Token, Access_Token_Secret, wait_on_rate_limit=True)

    

    return client








