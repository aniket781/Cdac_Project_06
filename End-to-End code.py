#!/usr/bin/env python
# coding: utf-8

# # YouTube comment API

# In[ ]:


get_ipython().system('pip install pymongo')
get_ipython().system('pip install google-api-python-client')
get_ipython().system('pip install nltk')
get_ipython().system('pip install emoji')
get_ipython().system('pip install emoji_data_python')
get_ipython().system('pip install vaderSentiment')


# In[ ]:


from pymongo import MongoClient
import os
from pymongo import MongoClient
import json
import googleapiclient.discovery
import emoji_data_python
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import emoji
import unicodedata
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# In[ ]:


nltk.download('punkt')
nltk.download('stopwords')


# In[ ]:


counter=0
data_dict={}

def get_next_number():
    """ it gives comment number for perticular comment serial wise 1 to nth commeent"""
    global counter
    counter += 1
    return counter

def fetch_comments_with_pagination(page_token=None):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyC2D2ciRULyvrYGCU6Tcdahnrnv1PZodCE"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId="vqTssXuPgfk",  # Use the 'videoId' parameter, not 'parentId'
        pageToken=page_token  # Pass the pageToken for pagination
    )

    response = request.execute()
    return response

def main():
    
    next_page_token = None
    NUM_PAGES=2000

    # Fetch multiple pages of comments
    for _ in range(NUM_PAGES):  # Set NUM_PAGES according to your needs
        response = fetch_comments_with_pagination(page_token=next_page_token)
        
        items = response.get('items', [])
        
        # Loop through each comment thread item
        for item in items:
            snippet = item.get('snippet', {})
            topLevelComment = snippet.get('topLevelComment', {})
            commentSnippet = topLevelComment.get('snippet', {})
            
            text_original = commentSnippet.get('textOriginal')
            
            data_dict[get_next_number()] = text_original
         


        
        # Get the next page token for the next iteration
        next_page_token = response.get('nextPageToken')
        
        # If there's no next page, exit the loop
        if not next_page_token:
            break

if __name__ == "__main__":
    main()
    #print(data_dict)
    
    client = MongoClient("mongodb://localhost:27017")
    db = client['Youtube_comment_database']
    collection= db['landslide']

    for key, value in data_dict.items():
        document = {"comment_number": key, "comment_text": value, "Name":"landslide"}
        collection.insert_one(document)

    print("Data inserted successfully.")


   


#     videoid       name
# 
# 
#     1-xGerv5FOk   Alone
# 
#     HhjHYkPQ8F0   Alone_2
# 
#     M-P4QBt-FWw   Darkside
#  
#     sJXZ9Dok7u8   Diamond Heart
# 
#     6tkaatkbC2Y   Fake A Smile
# 
#     lqYQXIt4SpA   Force
# 
#     JhCEXRgbc_M   Hope
# 
#     YQRHrco73g4   PLAY
# 
#     2i2khp_npdE   Sing Me To Sleep
# 
#     wJnBTPUQS5A   The Spectre
# 
#     axRAL0BXNvw   Time
# 
#     60ItHLz5WEA   Faded
# 
#     mfSU_XwEnZA   Heading Home
# 
#     dhYOPzcsbGM   On My Way

# # Combining All CSV

# In[ ]:


Alone=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Alone.csv")

Alone_2=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Alone_2.csv")

Darkside=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Darkside.csv")

Diamond_Heart=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Diamond_Heart.csv")

Fake_A_Smile=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Fake_A_Smile.csv")

Force=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Force.csv")

Hope=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Hope.csv")

PLAY=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.PLAY.csv")

Sing_Me_To_Sleep=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Sing_Me_To_Sleep.csv")

The_Spectre=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.The_Spectre.csv")

Time=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Time.csv")

faded=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.faded.csv")

heading_home=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.heading_home.csv")

on_my_way=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.on_my_way.csv")



# In[ ]:


Alan_walker_comments=pd.concat([Alone,Alone_2,Darkside,Diamond_Heart,Fake_A_Smile,Force,Hope,PLAY,Sing_Me_To_Sleep,The_Spectre,Time,faded,heading_home,on_my_way], ignore_index=True)


# In[ ]:


Alan_walker_comments.to_csv("D:\project\Alan_walker_comments.csv",index=True)


# # Data preprocessing
# 

# In[ ]:


comments=pd.read_csv(r"D:\Youtube_comment_database.landslide.csv")


# In[ ]:


comments.info()


# In[ ]:


comments.describe()


# In[ ]:


comments.head(10)


# In[ ]:


comments.tail(10)


# In[ ]:


comments.size


# In[ ]:


comments.shape


# In[ ]:


comments.isna().sum()


# In[ ]:


comments_1=comments.dropna(subset=["comment_text"])


# In[ ]:


comments_1.isna().sum()


# In[ ]:


comments_2=comments_1.iloc[:,2:]


# In[ ]:


comments_2.head(10)


# In[ ]:


def preprocess_text(text):
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Tokenize the text
    words = word_tokenize(text)
    
    #Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    
    # Join the words back into a cleaned sentence
    cleaned_text = ' '.join(words)
    
    return cleaned_text



# In[ ]:


comments_2['cleaned_comment']=comments_2['comment_text'].apply(preprocess_text)

comments_2


# In[ ]:


comments_2.isna().sum()


# In[ ]:


# Print the preprocessed DataFrame
comments_2.head(10)


# In[ ]:


clean_comment=comments_2.iloc[:,1:]


# In[ ]:


clean_comment


# In[ ]:


client = MongoClient("mongodb://localhost:27017")
db = client['proceesed_data_YoutuubeComments']
collection = db['Comments']


# In[ ]:


records = clean_comment.to_dict(orient='records')
collection.insert_many(records)
print("Data inserted into MongoDB.")


# # Vader Algorithm

# In[ ]:





# In[ ]:


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Perform sentiment analysis using VADER
def analyze_sentiment(text):
    sentiment_scores =analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    if compound_score > 0.05:
        return "Positive"
    elif compound_score < -0.05:
        return "Negative"
    else:
        return "Neutral"


# Apply sentiment analysis to each comment
comments_2['Sentiment'] = comments_2['cleaned_comment'].apply(analyze_sentiment)


# Count the sentiments
sentiment_counts = comments_2['Sentiment'].value_counts()


# In[ ]:


print(comments_2)


# In[ ]:




