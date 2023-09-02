#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install vaderSentiment')
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
data['Sentiment'] = data['cleaned_comment'].apply(analyze_sentiment)


# Count the sentiments
sentiment_counts = data['Sentiment'].value_counts()

