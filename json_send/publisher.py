import paho.mqtt.client as mqtt
import json
import time

# Define the MQTT broker address and port
broker = "localhost"
port = 1883  # Default MQTT port

# Define the topics
topics = ["roof_light", "puddle_light", "head_light", "back_light"]

# Publisher function
def publisher():
    client = mqtt.Client()
    client.connect(broker, port, 60)

    # Here, the payload being published is for each of the different lights, but we can set a script to default all values to zero on startup and then
    # publish only the json objects of the setting that has changed in value w the repective topic
    payloads = {
        "roof_light": 70,
        "puddle_light": 13,
        "head_light": 74,
        "back_light": 45
    }

    for topic, payload in payloads.items():
        payload_json = json.dumps({"value": payload})  # Send the payload in a proper JSON format
        client.publish(topic, payload_json)
        print(f"Published to {topic}: {payload_json}")
        time.sleep(1)

if __name__ == "__main__":
    publisher()
