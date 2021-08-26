#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FUNCTION: Script to run sentiment analysis on text. This script also handles 
          text that contains emojis converting the emojis first to text 
          descriptions using emot and then running sentiment analysis using 
          those descriptions embedded back in the text at the right spot. 

LAST UPDATED: 07/31/2021

OWNER: David J. Cox, PhD, MSB, BCBA-D
'''

# Packages and modules
import pandas as pd
import nltk
nltk.download('vader_lexicon') # Check to make sure it's up-to-date
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import emot as e
import dabl

pd.set_option("display.max_columns", None)

#%% Read in the data
raw_data = pd.read_csv('/Users/davidjcox/Dropbox (Personal)/Projects/Manuscripts In Progress/Empirical/Endicott Data/Comparing Twitter Sentiment Between ABA Practitioners & Med Practitioners/aba_twitter_scrape.csv')
data = raw_data.copy()
data.head()

#%% Get sentiment for all tweets without handling emojis
sid = SentimentIntensityAnalyzer() # specify model for asneitment analysis

neg = []
neu = []
pos = []
compound = []

for i in range(len(data)):
    text = str(data['content'][i]) # Isolate tweet for analysis
    text_s = sid.polarity_scores(text) # Get the sentiment scores

    # Append sentiment to lists for later adding to df
    neg.append(text_s.get('neg'))
    neu.append(text_s.get('neu'))
    pos.append(text_s.get('pos'))
    compound.append(text_s.get('compound'))

# Add sentiment to df
data['neg'] = neg
data['neu'] = neu
data['pos'] = pos
data['compound'] = compound

#%% Get sentiment for all tweets including emojis
neg = []
neu = []
pos = []
compound = []

for i in range(len(data)):
    text = str(data['content'][i]) # Isolate tweet for analysis

    # Get emoji information
    emoji_info = e.emoji(text)
    emoji_info = pd.DataFrame(emoji_info)
    if len(emoji_info)==0:
        # Get the sentiment scores
        text_s = sid.polarity_scores(text)
    
        # Append sentiment to lists for later adding to df
        neg.append(text_s.get('neg'))
        neu.append(text_s.get('neu'))
        pos.append(text_s.get('pos'))
        compound.append(text_s.get('compound'))
    else:
        add_str = str(' ')
        for j in range(len(emoji_info)):
            add_str = add_str + emoji_info['mean'][j] + ' '
        first_emoji = emoji_info['location'][0][0]
        text = text[:first_emoji] + add_str + text[first_emoji:]

        # Get the sentiment scores
        text_s = sid.polarity_scores(text)
    
        # Append sentiment to lists for later adding to df
        neg.append(text_s.get('neg'))
        neu.append(text_s.get('neu'))
        pos.append(text_s.get('pos'))
        compound.append(text_s.get('compound'))

    # Give update
    if (i+1)%100==0:
        print(f'{i+1} tweets complete')

# Add sentiment to df
data['neg_e'] = neg
data['neu_e'] = neu
data['pos_e'] = pos
data['compound_e'] = compound

#%% Save it
data.to_csv('/Users/davidjcox/Dropbox (Personal)/Projects/Manuscripts In Progress/Empirical/Endicott Data/Comparing Twitter Sentiment Between ABA Practitioners & Med Practitioners/aba_twitter_scrape_sentiment.csv')

#%% Looking at trends in twitter sentiment over time
raw_data = pd.read_csv('/Users/davidjcox/Dropbox (Personal)/Projects/Manuscripts In Progress/Empirical/Endicott Data/twitter-aba-sentiment/data/03_primary/aba_twitter_scrape_sentiment.csv')
data = raw_data.copy()

#%% Playing with dabl
df_clean = dabl.clean(data, verbose=1)

#%% Some cleanup of cols
df_clean = df_clean.drop(['Unnamed: 0.1_ @PMOIndia @AmitShah @drharshvardhan @IMAIndiaOrg @ANI',\
                         'Unnamed: 0.1_#MedTwitter #MedStudentTwitter #MedEd #AcademicChatter #AcademicTwitter',\
                         'Unnamed: 0.1_#MedTwitter #PeruvianPhysiciansCrew',\
                         'Unnamed: 0.1_#SelfDefenceIsLegal',
                         'Unnamed: 0.1_#たてたてよこよこ横山結衣 #ディズニーランド #Disney #初調査員 #あべこうじ #横山結衣 #中村かさね #藤原祐輝 #木邨将太 #服部未佳 #土曜日 #９時３５分 #青森 #夢はここから #生放送 #ハッピィ #土曜日 #9時35分 #ABA #青森朝日放送 #aomori https://t.co/On0xqhbqoX',
                         'Unnamed: 0.1_1-70 dias', 'Unnamed: 0.1_1-dos meses ',
                         'Unnamed: 0.1_1-tres meses ', 'Unnamed: 0.1_2-Maracay Estado Aragua ',
                         'Unnamed: 0.1_3- #ABA cantv reporte No 19650849',
                         'Unnamed: 0.1_3- #ABA cantv reporte No 19650849 l',
                         "Unnamed: 0.1_D govt they're waiting on for help is actually d one killing them",
                         'Unnamed: 0.1_cortados durante la Cuarentena. Nos engañan o que?',
                         'Unnamed: 0.1_por falta de pago. Y no hay manera de pagarlo xqse debe pagar en Zoom y ellos no estan trabajando. ES UN ABUSO DE CANTV',
                         'Unnamed: 0.1_dabl_continuous'], axis=1)

#%% Quick plots
dabl.plot(df_clean, target_col='compound') # Overall

# Bx twitter only
df_bx = df_clean[df_clean['focus']!= 'medtwitter']
dabl.plot(df_bx, target_col='compound')

# Medtwitter
df_med = df_clean[df_clean['focus']== 'medtwitter']
dabl.plot(df_med, target_col='compound')

#%% Sweetviz for exploration and df comparisons
import sweetviz as sv

# All
all_report = sv.analyze(df_clean)
all_report.show_html()

# Bx twitter vs. medtwitter
compare_report = sv.compare([df_bx, "Behavior Twitter"], [df_med, "Med Twitter"], feature_config)
compare_report.show_html()

#%% Quick regression modeling
from lazypredict.Supervised import LazyClassifier, LazyRegressor
from sklearn.model_selection import train_test_split

# Load data and split
y = df_clean['compound']
y_e = df_clean['compund_e']
X = df_clean.drop(['compound', 'compund_e', 'pos_e', 'neu_e', 'neg_e', 'neu', 'pos', 'neg'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=159753456852)
X_train_e, X_test_e, y_train_e, y_test_e = train_test_split(X, y_e, test_size=0.2, random_state=159753456852)

# Fit LazyRegressor
reg = LazyRegressor(
    ignore_warnings=True,
    random_state=1121218,
    verbose=True
  )

# Tweets without emoji conversion
models, predictions = reg.fit(X_train, X_test, y_train, y_test)  # pass all sets

# Tweets with emoji conversion
models_e, predictions_e = reg.fit(X_train, X_test, y_train_e, y_test_e)  # pass all sets

#%%