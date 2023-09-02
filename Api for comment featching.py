#!/usr/bin/env python
# coding: utf-8

# # YouTube Comments Sentiment Analysis

# In[9]:


get_ipython().system('pip install pymongo')
get_ipython().system('pip install google-api-python-client')


# In[1]:


from pymongo import MongoClient
import os
from pymongo import MongoClient
import json
import googleapiclient.discovery

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


   



   


# In[ ]:





#     videoid       name

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
#     
#     

# In[ ]:




