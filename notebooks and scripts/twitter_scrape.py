#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FUNCTION: The purpose of this script is to scrape Twitter for Tweets containing
          text from the lists below pertaining to

LAST UPDATED: 08/26/2021

OWNER: Your Name
'''

# In case it needs to be installed
!pip install git+https://github.com/JustAnotherArchivist/snscrape.git

import snscrape.modules.twitter as sntwitter
import pandas

# Personal preference
pd.set_option('display.max_columns', None)

#%% Lists
# Terms related ot online learning
online_learning = ['digital learning', 'remote delivery', 'Teaching online',
                   'Online class','online course*','Online learning',
                   'blended learning', 'Synchronous', 'Asynchronous',
                   'Polysynchronous', 'Hybrid', 'Zoom','Microsoft teams',
                   'Moodle', 'Canvas', 'Blackboard', 'WebX',
                   'Google classroom']

# Terms related to Covid-19 (Koh & Liew, 2021)
covd_list = ['Covid', 'Covid-19', 'COVID19', 'Coronavirus', 'Corona virus']

# Terms related to higher education
higher_ed = ['College', 'University', 'Professor', 'Teacher', 'Higher ed',
             'Higher education']


#%% Scrape Twitter for seed dataframe
!snscrape --jsonl --progress --max-results 10000000 --since 2020-03-01 twitter-search "#digitallearning until:2020-05-01" > text-query-tweets.json

# Read in the json file
oneline_tweets = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
oneline_tweets = pd.DataFrame(oneline_tweets)

#%%

for i in online_learning[1:2]:
    !snscrape --jsonl --progress --max-results 10000000 --since 2020-03-01 twitter-search f"#{i} until:2020-05-01" > text-query-tweets.json

    # Read in the json file
    add_tweets = pd.read_json('text-query-tweets.json', lines=True)

    # Creating a dataframe from the tweets list above
    add_tweets = pd.DataFrame(add_tweets)

    # Add new data to our growing list
    online_tweets = pd.concat(online_tweets, add_tweets)

#%% Add col for hashtag focus
oneline_tweets['time'] = 'pre-COVID'

#%% Scrape Twitter for #ABATherapy
!snscrape --jsonl --progress --max-results 100000 --since 2018-01-01 twitter-search "#ABATherapy until:2021-07-25" > text-query-tweets.json

# Read in the jscon file
abtx_tweets = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
abtx_tweets = pd.DataFrame(abtx_tweets)

# Add col for hashtag focus
abtx_tweets['focus'] = 'abatherapy'

#%% #ABA
!snscrape --jsonl --progress --max-results 100000 --since 2018-01-01 twitter-search "#ABA until:2021-07-25" > text-query-tweets.json

# Read in the jscon file
aba_tweets = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
aba_tweets = pd.DataFrame(aba_tweets)

# Add col for hashtag focus
aba_tweets['focus'] = 'aba'

#%% #appliedbehavioranalysis
!snscrape --jsonl --progress --max-results 100000 --since 2018-01-01 twitter-search "#appliedbehavioranalysis until:2021-07-25" > text-query-tweets.json

# Read in the jscon file
appliedbehavioranalysis_tweets = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
appliedbehavioranalysis_tweets = pd.DataFrame(appliedbehavioranalysis_tweets)

# Add col for hashtag focus
appliedbehavioranalysis_tweets['focus'] = 'appliedbehavioranalysis'

#%% Scrape Twitter for #medtwitter
!snscrape --jsonl --progress --max-results 10000000 --since 2018-01-01 twitter-search "#medtwitter until:2021-07-25" > text-query-tweets.json

# Read in the jscon file
med_tweets = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
med_tweets = pd.DataFrame(med_tweets)

# Add col for hashtag focus
med_tweets['focus'] = 'medtwitter'

#%% Concatenate all the dfs to each other
print("Expected length: ", len(bx_tweets) + len(abtx_tweets) + len(aba_tweets) + len(appliedbehavioranalysis_tweets) + len(med_tweets))
all_tweets = bx_tweets.append(abtx_tweets)
all_tweets = all_tweets.append(aba_tweets)
all_tweets = all_tweets.append(appliedbehavioranalysis_tweets)
all_tweets = all_tweets.append(med_tweets)
print("Observed length: ", len(all_tweets))

#%% Save it
all_tweets.to_csv('aba_twitter_scrape.csv')