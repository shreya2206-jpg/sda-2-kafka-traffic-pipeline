import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

OUTPUT_FILE = "traffic_events.csv"
NUMBER_OF_RECORDS = 100

crossing_ids = ["LC-101", "LC-102", "LC-103", "LC-104", "LC-105"]

road_names = [
    "Station Road",
    "Railway Crossing Road",
    "Market Road",
    "Main Road",
    "Industrial Road"
]

congestion_levels = ["Low", "Moderate", "High", "Severe"]

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "event_id",
        "crossing_id",
        "timestamp",
        "congestion_level",
        "traffic_delay_seconds",
        "current_speed_kmph",
        "free_flow_speed_kmph",
        "road_name"
    ])

    for i in range(1, NUMBER_OF_RECORDS + 1):

        congestion_level = random.choice(congestion_levels)
        free_flow_speed = random.choice([40, 50, 60])

        if congestion_level == "Low":
            current_speed = random.uniform(30, free_flow_speed)
            delay = random.randint(0, 30)

        elif congestion_level == "Moderate":
            current_speed = random.uniform(20, 30)
            delay = random.randint(31, 90)

        elif congestion_level == "High":
            current_speed = random.uniform(10, 20)
            delay = random.randint(91, 180)

        else:  # Severe
            current_speed = random.uniform(2, 10)
            delay = random.randint(181, 300)

        timestamp = datetime.now() - timedelta(
            seconds=random.randint(0, 3600)
        )

        writer.writerow([
            f"TRAFFIC-{i:03d}",
            random.choice(crossing_ids),
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            congestion_level,
            delay,
            round(current_speed, 2),
            free_flow_speed,
            random.choice(road_names)
        ])

print(f"Successfully generated {NUMBER_OF_RECORDS} traffic records.")
print(f"File created: {OUTPUT_FILE}")