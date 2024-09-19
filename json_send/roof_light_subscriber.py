import paho.mqtt.client as mqtt
import json
# lack of client subscribe acknowledgement

# Define the MQTT broker address and port
broker = "localhost"
port = 1883  # Default MQTT port

# Path to the JSON file
json_file_path = "json.data.json"

# Function to update the JSON file
def update_json_file(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Subscriber callback function
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"Error decoding JSON for topic {topic}: {payload}")
        return

    # Load existing data from JSON file
    with open(json_file_path, 'r') as file:
        current_data = json.load(file)

    # Update data for the specific topic
    current_data[topic] = data['value']

    # Save the updated data back to the JSON file
    update_json_file(current_data)
    print(f"Received message on {topic}: {data}")

def subscriber():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"roof_light_subscriber")
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.subscribe("roof_light")
    client.loop_forever()

if __name__ == "__main__":
    subscriber()
