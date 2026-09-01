import csv
import json
import time
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic-events"
CSV_FILE = "traffic_events.csv"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print(f"Reading data from: {CSV_FILE}")
print(f"Sending messages to Kafka topic: {TOPIC_NAME}\n")

with open(CSV_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        message = {
            "event_id": row["event_id"],
            "crossing_id": row["crossing_id"],
            "timestamp": row["timestamp"],
            "congestion_level": row["congestion_level"],
            "traffic_delay_seconds": int(row["traffic_delay_seconds"]),
            "current_speed_kmph": float(row["current_speed_kmph"]),
            "free_flow_speed_kmph": float(row["free_flow_speed_kmph"]),
            "road_name": row["road_name"]
        }

        future = producer.send(TOPIC_NAME, value=message)

        # Wait for Kafka to confirm the message was sent
        record_metadata = future.get(timeout=10)

        print(
            f"Successfully sent: {message['event_id']} "
            f"| Crossing: {message['crossing_id']} "
            f"| Congestion: {message['congestion_level']} "
            f"| Partition: {record_metadata.partition} "
            f"| Offset: {record_metadata.offset}"
        )

        # Send one message every 2 seconds
        time.sleep(2)

producer.flush()
producer.close()

print("\nAll traffic events sent successfully.")