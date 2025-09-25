# backend/simulator.py
import threading
import requests
import random
import time

BACKEND = "http://localhost:5000/device_update"  # ajuste se usar IP diferente

def send_payload(payload):
    try:
        r = requests.post(BACKEND, json=payload, timeout=5)
        print(f"[POST] {BACKEND} -> {r.status_code} | {payload}")
    except Exception as e:
        print("[ERROR POST]", e, payload)

def sensor_temperature(sensor_id=1, interval=5):
    while True:
        value = round(random.uniform(20.0, 35.0), 2)
        payload = {
            "id": sensor_id,            # numeric id (compatível com schema identity)
            "device_id": sensor_id,
            "name": f"temp-{sensor_id}",
            "type": "temperature",
            "location": "Garagem",
            "value": value
        }
        send_payload(payload)
        time.sleep(interval)

def sensor_humidity(sensor_id=2, interval=6):
    while True:
        value = round(random.uniform(35.0, 85.0), 1)
        payload = {
            "id": sensor_id,
            "device_id": sensor_id,
            "name": f"hum-{sensor_id}",
            "type": "humidity",
            "location": "Garagem",
            "value": value
        }
        send_payload(payload)
        time.sleep(interval)

def sensor_gps_moto(sensor_id=3, interval=7):
    """
    Simula a localização da moto com 3 casos:
     - normal -> 'Garagem'
     - fora do lugar -> 'Rua 123'
     - desaparecida -> 'DESAPARECIDA' (value=0)
    """
    cases = ["normal", "fora", "desaparecida"]
    while True:
        caso = random.choices(cases, weights=[0.7, 0.2, 0.1])[0]  # mais vezes 'normal'
        if caso == "normal":
            loc = "Garagem"
            value = 1
        elif caso == "fora":
            loc = "Rua 123"
            value = 1
        else:
            loc = "DESAPARECIDA"
            value = 0

        payload = {
            "id": sensor_id,
            "device_id": sensor_id,
            "name": f"moto-{sensor_id}",
            "type": "gps",
            "location": loc,
            "value": value,
            "case": caso  # campo extra para depuração / logs
        }
        send_payload(payload)
        print(f"[MOTO] caso={caso}")
        time.sleep(interval)

def main():
    threads = [
        threading.Thread(target=sensor_temperature, args=(1, 5), daemon=True),
        threading.Thread(target=sensor_humidity, args=(2, 6), daemon=True),
        threading.Thread(target=sensor_gps_moto, args=(3, 7), daemon=True),
    ]
    for t in threads:
        t.start()

    print("Simulador IoT iniciado: 3 sensores ativos (temp, humidity, moto GPS). Ctrl+C para sair.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Parando simulador...")

if __name__ == "__main__":
    main()
