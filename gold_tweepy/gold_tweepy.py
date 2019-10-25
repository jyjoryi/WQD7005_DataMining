import os
import tweepy
#from tweepy import Stream
#from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener
#import json
import pandas as pd
#import csv
import re
from textblob import TextBlob
import string
#import preprocessor as p
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')

os.getcwd()
os.chdir('C:/Users/tan.joryi/Desktop/p/data_mining/01. web scraping/WQD7005-data-mining-master/gold_tweepy')

# Twitter credentials for the app
consumer_key = 'z1wtobsYAyRZNUS2OwHN6Ep2X'
consumer_secret = 'LJaGCw57bjhS401qYW9nyHyT402JRxQAGYspUgV2Qz4HaozTAD'
access_key = '477741252-TElKvftmgnbc90Arg6VvSXGRQ6ODaBPSZzZPmfNj'
access_secret = '7pNNpbNy14nkgIxzF3JYzpOMJ20a7NEBTL3iF30948bDs'

# Pass Twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Create file paths
goldprice_tweets = "goldprice_tweets.csv"

# Column to extract
COLS = ['id','created_at','source','original_text',
        'clean_text',
        'sentiment','polarity','subjectivity','lang',
        'favorite_count','retweet_count','original_author','possibly_sensitive','hashtags', 'user_mentions', 'place',
        'place_coord_boundaries']

#set two date variables for date range
start_date = '2019-09-01'
end_date = '2019-09-30'


# to remove these emojis or emoticons 
# HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD',
    'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP',
    ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)', '<3'])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<',
    ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('])

emoticons = emoticons_happy.union(emoticons_sad) # combine happy and sad emoticons

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
 
    #after tweepy preprocessing the colon left remain after removing mentions
    #or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
  
    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
 
    #filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
 
    #looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
            
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)


def write_tweets(keyword, file):
    #if the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header = 0)
    else:
        df = pd.DataFrame(columns = COLS)
    #page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q = keyword, count = 200, include_rts = False, since = start_date).pages(50):
        for status in page:
            new_entry = []
            status = status._json
            
            if status['lang'] != 'en':
                continue
            
            if status['created_at'] in df['created_at'].values:
                #get index number where created at in the existing data frame equals to current twitter data - status
                i = df.loc[df['created_at'] == status['created_at']].index[0] 
                #df.at getting the value in the particular row and column specified
                if status['favorite_count'] != df.at[i, 'favorite_count'] or \
                   status['retweet_count'] != df.at[i, 'retweet_count']:
                       df.at[i, 'favorite_count'] = status['favorite_count']
                       df.at[i, 'retweet_count'] = status['retweet_count']
                continue
            
            #clean_text = p.clean(status['text'])
            
            #filtered_tweet = clean_tweets(clean_text)
            clean_text = clean_tweets(status['text'])
            
            # pass textBlob method for sentiment calculations
            #blob = TextBlob(filtered_tweet)
            blob = TextBlob(clean_text)
            #blob = TextBlob(status['text'])
            Sentiment = blob.sentiment
            
            polarity = Sentiment.polarity
            subjectivity = Sentiment.subjectivity
            
            new_entry += [
                    status['id'], status['created_at'], status['source'], status['text'], 
                    clean_text, 
                    Sentiment,
                    polarity, subjectivity, status['lang'], status['favorite_count'], status['retweet_count']
                    ]
            
            new_entry.append(status['user']['screen_name'])
            
            try:
                is_sensitive = status['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            new_entry.append(is_sensitive)
            
            hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status['entities']['hashtags']])
            new_entry.append(hashtags)
            
            mentions = ", ".join([mention['screen_name'] for mention in status['entities']['user_mentions']])
            new_entry.append(mentions)
            
            try:
                location = status['user']['location']
            except TypeError:
                location = ''
            new_entry.append(location)
            
            try:
                coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
            except TypeError:
                coordinates = None
            new_entry.append(coordinates)
            
            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            #because we are appending two dataframes together, hence we need to ignore index to reindex again
            df = df.append(single_tweet_df, ignore_index = True)
            csvFile = open(file, 'a', encoding = 'utf-8') # 'a' open file in append mode

    df.to_csv(csvFile, mode = 'a', columns = COLS, index = False, encoding = 'utf-8')
    
goldprice_keywords = '#goldprice OR #goldnews'

write_tweets(goldprice_keywords, goldprice_tweets)