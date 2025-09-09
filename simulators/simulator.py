import time, json, random, argparse
import paho.mqtt.client as mqtt
import requests  


MQTT_BROKER = 'test.mosquitto.org'
MQTT_PORT = 1883


parser = argparse.ArgumentParser()
parser.add_argument('--id', required=True)
parser.add_argument('--interval', type=float, default=2.0)
args = parser.parse_args()


client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)


while True:
    payload = {
        'device_id': args.id,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'latitude': round(-23.5 + random.random() * 0.02, 6),
        'longitude': round(-46.6 + random.random() * 0.02, 6),
        'status': random.choice(['idle', 'moving', 'parked']),
        'battery': random.randint(10, 100),
        'actuator_lock': random.choice([True, False]),
        'temperature': round(20 + random.random() * 10, 1)
    }

    
    topic = f'systack/iot/{args.id}'
    client.publish(topic, json.dumps(payload))
    print('Published', topic, payload)

    
    backend_payload = {
        "id": int(args.id),
        "status": payload["status"],
        "timestamp": payload["timestamp"],
        "value": payload["temperature"] 
    }
    try:
        r = requests.post("http://localhost:5000/device_update", json=backend_payload, timeout=2)
        print(f"Sent to backend, status code: {r.status_code}")
    except Exception as e:
        print("Error sending to backend:", e)

    
    time.sleep(args.interval)
