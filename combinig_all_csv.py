#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


Alone=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Alone.csv")


# In[3]:


Alone_2=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Alone_2.csv")


# In[4]:


Darkside=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Darkside.csv")


# In[5]:


Diamond_Heart=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Diamond_Heart.csv")


# In[6]:


Fake_A_Smile=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Fake_A_Smile.csv")


# In[7]:


Force=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Force.csv")


# In[8]:


Hope=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Hope.csv")


# In[9]:


PLAY=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.PLAY.csv")


# In[10]:


Sing_Me_To_Sleep=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Sing_Me_To_Sleep.csv")


# In[11]:


The_Spectre=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.The_Spectre.csv")


# In[12]:


Time=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.Time.csv")


# In[13]:


faded=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.faded.csv")


# In[14]:


heading_home=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.heading_home.csv")


# In[15]:


on_my_way=pd.read_csv(r"D:\project\all csv\Youtube_comment_database.on_my_way.csv")


# In[16]:


Alan_walker_comments=pd.concat([Alone,Alone_2,Darkside,Diamond_Heart,Fake_A_Smile,Force,Hope,PLAY,Sing_Me_To_Sleep,The_Spectre,Time,faded,heading_home,on_my_way], ignore_index=True)


# In[17]:


Alan_walker_comments.to_csv("D:\project\Alan_walker_comments.csv",index=True)


# In[ ]:




