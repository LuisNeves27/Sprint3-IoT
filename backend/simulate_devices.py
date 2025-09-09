import requests
import time
import random

BACKEND_URL = "http://localhost:5000/device_update"

# Lista de sensores IoT (3 tipos distintos)
devices = [
    {"id": "sensor_temp_01", "type": "temperature", "location": "Zona Leste"},
    {"id": "sensor_lock_01", "type": "lock_status", "location": "Zona Leste"},
    {"id": "sensor_gps_01", "type": "gps", "location": "Zona Leste"}
]

# Função para simular os casos de uso
def simulate_device(device):
    if device["type"] == "temperature":
        value = round(random.uniform(25.0, 35.0), 1) 
    elif device["type"] == "lock_status":
        # 0 = destravada, 1 = travada
        value = random.choice([0, 1])
    elif device["type"] == "gps":
       
        value = random.choice(["Zona Leste", "Zona Norte", "Desconhecida"])
    else:
        value = "N/A"

    payload = {
        "id": device["id"],
        "type": device["type"],
        "location": device["location"],
        "value": value
    }

    try:
        r = requests.post(BACKEND_URL, json=payload)
        print(f"Enviado: {payload} -> {r.status_code}")
    except Exception as e:
        print(f"Erro ao enviar {device['id']}: {e}")


if __name__ == "__main__":
    print("Simulador de dispositivos IoT iniciado...")
    while True:
        for dev in devices:
            simulate_device(dev)
        time.sleep(3)  