#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define the currency
CURRENCY = "bitcoin"
CURRENCY_SYMBOL = "BTC"

## personal config
TWEETS_FOLDER    = "data/crypto/%s"%(CURRENCY) # Relative path to historical data
SEP_CHAR         = '~' # character seperating dates from and to in filename
ENVS             = ['CRYPTO', 'LINE_COUNT', 'MOST_RECENT_FILE', 'MOST_RECENT_ID'] # Stored in var.csv
MAX_ROW_PER_FILE = 20000 # Each file storing data has a maximum amount of rows

tweets_raw_file = 'data/twitter/%s/%s_tweets_raw.csv'%(CURRENCY_SYMBOL,CURRENCY)
tweets_clean_file = 'data/twitter/%s/%s_tweets_clean_extended.csv'%(CURRENCY_SYMBOL,CURRENCY)
query = '#%s OR #%s'%(CURRENCY,CURRENCY_SYMBOL) ####TODO PUT BACK  OR {CURRENCY} OR ${CURRENCY} OR ${CURRENCY_SYMBOL}


# In[2]:


from twython import Twython


# In[26]:


APP_KEY =  'mPQKoRwd2Pb9qpQyQmyG5s8KR'
APP_SECRET =  'HLvIhusvfzDLKaRXY8CnZGP143kp3E3f2KqQBIEMfVL5mOxZjq'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
twitter.get_application_rate_limit_status()['resources']['search']


# In[4]:


from time import sleep
import json
import pandas as pd
import io
from tqdm import tqdm


# In[36]:


hours=168


# In[37]:


import datetime


# In[38]:


while(hours!=0):
    
    file=open("twitter_script_extended.txt",'a')
    d = pd.read_csv(tweets_raw_file)
    NUMBER_OF_QUERIES = 450
    data = {"statuses": []}
    next_id = "" #"1147236962945961984"
    since_id=str(d['ID'][0])
    print("here")
    with open(tweets_raw_file,"w", encoding='utf-8') as f:
        
        if not next_id and not since_id:
            f.write("ID,Text,UserName,UserFollowerCount,RetweetCount,Likes,CreatedAt\n")
        while(True):
            twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
            last_size = 0
            for i in tqdm(range(NUMBER_OF_QUERIES)):
                if not next_id:
                    data = twitter.search(q=query, lang='en', result_type='recent', count="100",tweet_mode='extended',since_id=since_id) # Use since_id for tweets after id
                elif since_id:
                    data["statuses"].extend(twitter.search(q=query, lang='en', result_type='mixed', count="100",max_id=next_id,since_id=since_id,tweet_mode='extended')["statuses"])
                else:
                    data["statuses"].extend(twitter.search(q=query, lang='en', result_type='mixed', count="100", max_id=next_id,tweet_mode='extended')["statuses"])
                if len(data["statuses"]) > 1:
                    next_id = data["statuses"][len(data["statuses"]) - 1]['id']
                if last_size + 1 == len(data["statuses"]):
                    break
                else:
                    last_size = len(data["statuses"])
            file.write('Retrieved {0}, waiting for 15 minutes until next queries'.format(len(data["statuses"])))
            print('Retrieved {0}, waiting for 15 minutes until next queries'.format(len(data["statuses"])))
            df = pd.DataFrame([[s["id"], s["full_text"].replace('\n','').replace('\r',''), s["user"]["name"], s["user"]["followers_count"], s["retweet_count"], s["favorite_count"], s["created_at"]] for s in data["statuses"]], columns=('ID', 'Text', 'UserName', "UserFollowerCount", 'RetweetCount', 'Likes', "CreatedAt"))
            df = df.append(d,ignore_index=True)
            df.to_csv(f, mode='w', encoding='utf-8',index=False,header=True)
            if last_size + 1 == len(data["statuses"]):
                print('No more new tweets, stopping...')
                break
            data["statuses"] = []

            sleep(910)
    
    file.write('Written till row %s and id %s at time %s \n'%(str(df.shape[0]),since_id,str(datetime.datetime.now())))
    file.close()
    sleep(3600)
    hours=hours-1


# In[ ]:




