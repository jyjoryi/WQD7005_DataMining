# -*- coding: utf-8 -*-

import os
os.chdir('C:/Users/tan.joryi/Desktop/p/data_mining/01. web scraping/WQD7005-data-mining-master/newscrawler')

import pandas as pd
import re
from textblob import TextBlob

# read data from csv file
news = pd.read_csv('news.csv')

#remove null rows and duplicate rows
news.dropna(inplace=True)
news.drop_duplicates(inplace=True)
news = news.reset_index(drop=True)

#filter down to only news about gold
for i in range(0,len(news)):
    if re.search(r'gold',news['news'][i],re.I) is not None:
        continue
    else:
        news.drop(i, inplace=True)

news = news.reset_index(drop=True)

#pd.to_datetime is able to read this format >> 01:06 AM10/18/2019 01:06:03 AM UTC-0400
news['DateTime'] = pd.to_datetime(news['DateTime'])

for i in range(0,len(news)):
    news['DateTime'][i] = news['DateTime'][i].date()

news.sort_values(by=['DateTime'],inplace=True)
news = news.reset_index(drop=True)

#derive sentiments in terms of polarity and subjectivity using textblob
news['polarity'] = ''
news['subjectivity'] = ''
news['polarity_description'] = ''

for i in range(0,len(news)):
    blob = TextBlob(news['news'][i])
    Sentiment = blob.sentiment
    news['polarity'][i] = Sentiment.polarity
    news['subjectivity'][i] = Sentiment.subjectivity
    
    if Sentiment.polarity > 0:
        news['polarity_description'][i] = 'Positive'
    elif Sentiment.polarity < 0:
        news['polarity_description'][i] = 'Negative'
    else:
        news['polarity_description'][i] = 'Neutral'
        
news['polarity'] = pd.to_numeric(news['polarity'])
news['subjectivity'] = pd.to_numeric(news['subjectivity'])

news = news[['DateTime','news','polarity_description','polarity','subjectivity']]
news.to_csv('news_preprocessed.csv',index=False)

#average sentiment score group by date 
polarity_mean = news.groupby('DateTime', as_index=False)['polarity'].mean()
polarity_mean.rename(columns={'polarity':'polarity_mean'},inplace=True)

polarity_mean['polarity_description'] = ''

for i in range(0,len(polarity_mean)):
    if polarity_mean['polarity_mean'][i] > 0:
        polarity_mean['polarity_description'][i] = 'Positive'
    elif polarity_mean['polarity_mean'][i] < 0:
        polarity_mean['polarity_description'][i] = 'Negative'
    else:
        polarity_mean['polarity_description'][i] = 'Neutral'

polarity_mean.to_csv('polarity_mean.csv',index=False)