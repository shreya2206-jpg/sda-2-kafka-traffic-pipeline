from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["traffic_db"]
collection = db["traffic_events"]

# Kafka consumer
consumer = KafkaConsumer(
    "traffic-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="mongodb-consumer-group-v2",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening for traffic events...")

for message in consumer:
    event = message.value

    # Insert Kafka event into MongoDB
    collection.insert_one(event)

    print(
        f"Saved to MongoDB: "
        f"{event['event_id']} | "
        f"{event['congestion_level']}"
    )