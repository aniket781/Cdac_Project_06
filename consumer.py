from confluent_kafka import Consumer, KafkaError
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from kafka import KafkaConsumer
import nltk
import json

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create a Spark session
spark = SparkSession.builder.appName("YouTubeSentimentAnalysis").getOrCreate()


# Create a UDF (User Defined Function) for sentiment analysis
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    if compound_score > 0.05:
        return "Positive"
    elif compound_score < -0.05:
        return "Negative"
    else:
        return "Neutral"


sentiment_udf = udf(analyze_sentiment, StringType())


# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Consumer group and topic
group_id = 'my-consumer-group'
topic = 'youtube_comments'

# Consumer configuration
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # or 'latest' or 'none'
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe([topic])
print("subscription done")

# Initialize an empty list to store messages
messages = []

# Poll for new messages
while True:
    msg = consumer.poll(1.0)


    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            print('Reached end of partition')
        else:
            print('Error: {}'.format(msg.error()))
    else:
        try:

                if len(messages) >=10:
                    print("break loop")
                    break
                else:
                    value = msg.value().decode('utf-8')  # Assuming the message value is in bytes
                    dictionary = eval(value)  # Safely evaluate the string as a dictionary
                    print('Received dictionary:', dictionary)
                    messages.append(dictionary)
        except Exception as e:
           print('Error decoding or processing message:', e)



# Close the Kafka consumer
consumer.close()

#rdd = spark.sparkContext.parallelize(messages)
# Create a DataFrame from the list of messages

df = pd.DataFrame(messages)
df["Sentiment"] = df["cleaned_comment"].apply(analyze_sentiment)
print(df)

# Write the DataFrame to a CSV file
df.to_csv("D:\project\processed csv\output21.csv", index=False)

#df_with_sentiment.write \
    #.format("csv") \
    #.option("header", "true") \
    #.mode("overwrite") \
    #.save("D:\project\processed csv\output222.csv")
# Stop the Spark session
spark.stop()


# Print the DataFrame
print("file saved")



