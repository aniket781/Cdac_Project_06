#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install nltk')


# In[2]:


get_ipython().system('pip install emoji')


# In[3]:


get_ipython().system('pip install emoji_data_python')


# In[4]:


import emoji_data_python


# In[1]:


get_ipython().system('pip install vaderSentiment')


# 
# importing all modules which are required

# In[1]:


import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import emoji
import unicodedata
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# In[2]:


nltk.download('punkt')


# In[3]:


nltk.download('stopwords')


# In[4]:


comments=pd.read_csv(r"D:\Youtube_comment_database.landslide.csv")


# In[5]:


comments.info()


# In[6]:


comments.describe()


# In[7]:


comments.head(10)


# In[8]:


comments.tail(10)


# In[9]:


comments.size


# In[10]:


comments.shape


# In[11]:


comments.isna().sum()


# In[12]:


comments_1=comments.dropna(subset=["comment_text"])


# In[13]:


comments_1.isna().sum()


# In[16]:


comments_2=comments_1.iloc[:,2:]


# In[17]:


comments_2.head(10)


# In[18]:


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



# In[19]:


comments_2['cleaned_comment']=comments_2['comment_text'].apply(preprocess_text)

comments_2


# In[20]:


comments_2.isna().sum()


# In[21]:


# Print the preprocessed DataFrame
comments_2.head(10)


# 

# In[22]:


clean_comment=comments_2.iloc[:,1:]


# In[25]:


clean_comment


# clean_comment.to_csv("D:\project\clean_comment_withoutEmoji.csv")     
# 
# ""to convert all data to csv file"

# In[27]:


client = MongoClient("mongodb://localhost:27017")
db = client['proceesed_data_YoutuubeComments']
collection = db['Comments']


# In[28]:


records = clean_comment.to_dict(orient='records')
collection.insert_many(records)
print("Data inserted into MongoDB.")


# In[29]:





# In[ ]:




