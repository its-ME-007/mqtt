import paho.mqtt.client as mqtt
import json
# lack of client subscribe acknowledgement
broker = "localhost"
port = 1883

json_file_path = "json.data.json"

def update_json_file(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def on_message(client,userdata,message):
# This is the callback function that will be called when a message is received from the MQTT broker
    topic = message.topic
    payload = message.payload.decode("utf-8")
    
    try:
        data = json.loads(payload)  # Expect the payload to be in valid JSON format
    except json.JSONDecodeError:
        print(f"Error decoding JSON for topic {topic}: {payload}")
        return

    # Load existing data from JSON file
    with open(json_file_path, 'r') as file:
        current_data = json.load(file)

    # Update data for the specific topic
    current_data[topic] = data['value']  # Assuming the JSON structure is {"value": value}

    # Save the updated data back to the JSON file
    update_json_file(current_data)
    print(f"Received message on {topic}: {data}")


def subscriber():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"head_light_subscriber")
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.subscribe("head_light")  # Specific topic
    client.loop_forever()  # Start non-blocking loop

if __name__ == "__main__":
    subscriber()
