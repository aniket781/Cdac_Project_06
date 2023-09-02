import time
from json import dumps
from bson import ObjectId
from kafka import KafkaProducer
import pymongo
import json

topic = "youtube_comments"
bootstrap_servers = "localhost:9092"

if __name__ == "__main__":
    print("Kafka Producer Application Started ...")

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers
    )


def handle_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
def main():
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["proceesed_data_YoutuubeComments"]
    collection = db["Comments"]

    comment_documents = collection.find()

    for document in comment_documents:
     message_value = json.dumps(document, default=handle_objectid, ensure_ascii=False).encode('utf-8')
     producer.send(topic,value=message_value)
     print(document)

    producer.close()

main()

