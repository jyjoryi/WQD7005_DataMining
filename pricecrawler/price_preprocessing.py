# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:05:18 2019

@author: leow.weiqin
"""
import os
os.chdir('C:/Users/tan.joryi/Desktop/p/data_mining/01. web scraping/WQD7005-data-mining-master/pricecrawler')

import pandas as pd
from datetime import timedelta

goldprice = pd.read_csv('goldprice.csv',thousands=',')

goldprice.info()
goldprice.describe()
len(goldprice)

goldprice['date_text'] = pd.to_datetime(goldprice['date_text'])
goldprice.sort_values(by=['date_text'],ascending=False,inplace=True)
goldprice.dropna(inplace=True)
goldprice = goldprice.reset_index(drop=True)

goldprice['trend'] = ''

for i in range (0,len(goldprice)-1):
    if goldprice['closing_price'][i] > goldprice['closing_price'][i+1]:
        goldprice['trend'][i] = 'upward'
    elif goldprice['closing_price'][i]== goldprice['closing_price'][i+1]:
        goldprice['trend'][i] = 'maintain'
    else:
        goldprice['trend'][i] = 'downward'

goldprice['closing_at_daily_high'] = ''

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['daily_high'][i]:
        goldprice['closing_at_daily_high'][i] = 1
    else:
        goldprice['closing_at_daily_high'][i] = 0

goldprice['closing_at_daily_low'] = ''

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['daily_low'][i]:
        goldprice['closing_at_daily_low'][i] = 1
    else:
        goldprice['closing_at_daily_low'][i] = 0

goldprice['open_equals_closing'] = ''

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['open_price'][i]:
        goldprice['open_equals_closing'][i] = 1
    else:
        goldprice['open_equals_closing'][i] = 0

goldprice['all_day_maintain'] = ''

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['open_price'][i] == goldprice['daily_high'][i] == goldprice['daily_low'][i]:
        goldprice['all_day_maintain'][i] = 1
    else:
        goldprice['all_day_maintain'][i] = 0

for i in range (0,len(goldprice)):
    if goldprice['date_text'][i] - goldprice['date_text'][i+1] == timedelta(days=4):
        goldprice = goldprice.append({'date_text':goldprice['date_text'][i]-timedelta(days=1)},ignore_index=True)
        goldprice = goldprice.append({'date_text':goldprice['date_text'][i]-timedelta(days=2)},ignore_index=True)
        goldprice = goldprice.append({'date_text':goldprice['date_text'][i]-timedelta(days=3)},ignore_index=True)
    elif goldprice['date_text'][i] - goldprice['date_text'][i+1] == timedelta(days=3):
        goldprice = goldprice.append({'date_text':goldprice['date_text'][i]-timedelta(days=1)},ignore_index=True)
        goldprice = goldprice.append({'date_text':goldprice['date_text'][i]-timedelta(days=2)},ignore_index=True)
    elif goldprice['date_text'][i] - goldprice['date_text'][i+1] == timedelta(days=2):
        goldprice = goldprice.append({'date_text':goldprice['date_text'][i]-timedelta(days=1)},ignore_index=True)
    else:
        continue

goldprice.sort_values(by=['date_text'],inplace=True)
goldprice = goldprice.reset_index(drop=True)

def get_day(x):
    return x.day_name()

def get_day_no(x):
    return x.weekday()+1
    
def get_month(x):
    return x.month_name()

goldprice['day'] = goldprice['date_text'].apply(get_day)
goldprice['day_no'] = goldprice['date_text'].apply(get_day_no)
goldprice['month'] = goldprice['date_text'].apply(get_month)
goldprice['year'] = goldprice['date_text'].dt.year

goldprice = goldprice[['year','month','date_text','day','day_no','open_price','daily_low','daily_high','closing_price','trend',
                       'open_equals_closing','all_day_maintain','closing_at_daily_low','closing_at_daily_high']]
goldprice.to_csv('goldprice_preprocessed.csv',index=False)

'''
MODIFY PROCESS
'''

import numpy as np

for i in range(0,len(goldprice)):
    if np.isnan(goldprice['open_price'][i]) and np.isnan(goldprice['open_price'][i+1]) and np.isnan(goldprice['open_price'][i+2]):
        new_price = np.mean([goldprice['closing_price'][i-1],goldprice['open_price'][i+3]])
        goldprice['open_price'][i] = goldprice['open_price'][i+1] = goldprice['open_price'][i+2] = new_price
        goldprice['closing_price'][i] = goldprice['closing_price'][i+1] = goldprice['closing_price'][i+2] = new_price
        goldprice['daily_low'][i] = goldprice['daily_low'][i+1] = goldprice['daily_low'][i+2] = new_price
        goldprice['daily_high'][i] = goldprice['daily_high'][i+1] = goldprice['daily_high'][i+2] = new_price
    elif np.isnan(goldprice['open_price'][i]) and np.isnan(goldprice['open_price'][i+1]):
        new_price = np.mean([goldprice['closing_price'][i-1],goldprice['open_price'][i+2]])
        goldprice['open_price'][i] = goldprice['open_price'][i+1] = new_price
        goldprice['closing_price'][i] = goldprice['closing_price'][i+1] = new_price
        goldprice['daily_low'][i] = goldprice['daily_low'][i+1] = new_price
        goldprice['daily_high'][i] = goldprice['daily_high'][i+1] = new_price
    elif np.isnan(goldprice['open_price'][i]):
        new_price = np.mean([goldprice['closing_price'][i-1],goldprice['open_price'][i+1]])
        goldprice['open_price'][i] = new_price
        goldprice['closing_price'][i] = new_price
        goldprice['daily_low'][i] = new_price
        goldprice['daily_high'][i] = new_price
    else:
        continue
    
for i in range (1,len(goldprice)):
    if goldprice['closing_price'][i] > goldprice['closing_price'][i-1]:
        goldprice['trend'][i] = 'upward'
    elif goldprice['closing_price'][i]== goldprice['closing_price'][i-1]:
        goldprice['trend'][i] = 'maintain'
    else:
        goldprice['trend'][i] = 'downward'

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['daily_high'][i]:
        goldprice['closing_at_daily_high'][i] = 1
    else:
        goldprice['closing_at_daily_high'][i] = 0

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['daily_low'][i]:
        goldprice['closing_at_daily_low'][i] = 1
    else:
        goldprice['closing_at_daily_low'][i] = 0

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['open_price'][i]:
        goldprice['open_equals_closing'][i] = 1
    else:
        goldprice['open_equals_closing'][i] = 0

for i in range (0,len(goldprice)):
    if goldprice['closing_price'][i] == goldprice['open_price'][i] == goldprice['daily_high'][i] == goldprice['daily_low'][i]:
        goldprice['all_day_maintain'][i] = 1
    else:
        goldprice['all_day_maintain'][i] = 0

if goldprice['open_price'][894] > goldprice['closing_price'][894]:
    goldprice['daily_high'][894] = goldprice['open_price'][894]
    goldprice['daily_low'][894] = goldprice['closing_price'][894]
elif goldprice['open_price'][894] == goldprice['closing_price'][894]:
    goldprice['daily_high'][894] = goldprice['daily_low'][894] = goldprice['closing_price'][894]
else:
    goldprice['daily_high'][894] = goldprice['closing_price'][894]
    goldprice['daily_low'][894] = goldprice['open_price'][894]

goldprice.to_csv('goldprice_modified.csv',index=False)

'''
MERGE NEWS POLARITY TO GOLDPRICE TREND
'''

get_polarity_mean = pd.read_csv('C:/Users/tan.joryi/Desktop/p/data_mining/01. web scraping/WQD7005-data-mining-master/newscrawler/polarity_mean.csv')
get_polarity_mean['DateTime'] = pd.to_datetime(get_polarity_mean['DateTime'])

merge = pd.merge(get_polarity_mean,
                 goldprice[['date_text','trend']],
                 how='left',
                 left_on=['DateTime'],
                 right_on=['date_text']
                 )

merge['analysis'] = ''

for i in range(0,len(merge)):
    if (merge['polarity_mean'][i] > 0 and merge['trend'][i] == 'upward'):
        merge['analysis'][i] = 'makes sense'
    elif (merge['polarity_mean'][i] < 0 and merge['trend'][i] == 'downward'):
        merge['analysis'][i] = 'makes sense'
    elif (merge['polarity_mean'][i] == 0 and merge['trend'][i] == 'maintain'):
        merge['analysis'][i] = 'makes sense'
    else:
        merge['analysis'][i] = 'hmmm'

merge.to_csv('C:/Users/tan.joryi/Desktop/p/data_mining/01. web scraping/WQD7005-data-mining-master/merge_price_to_news.csv',index=False)