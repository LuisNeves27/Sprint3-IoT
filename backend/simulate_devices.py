import requests
import random
import time

BACKEND_URL = "http://127.0.0.1:5000/device_update"  # ajuste se rodar em rede

# Função para enviar dados
def enviar_dado(sensor_id, sensor_type, location, value):
    try:
        payload = {
            "id": sensor_id,
            "type": sensor_type,
            "location": location,
            "value": value
        }
        res = requests.post(BACKEND_URL, json=payload)
        print(f"[OK] {sensor_id} -> {value} | Status {res.status_code}")
    except Exception as e:
        print("[ERRO]", e)


def simular():
    while True:
        # 🌡️ Sensor 1: Temperatura
        temp = round(random.uniform(20, 35), 2)
        enviar_dado("temp-01", "temperature", "Garagem", temp)

        # 💧 Sensor 2: Umidade
        umid = round(random.uniform(40, 80), 2)
        enviar_dado("umid-01", "humidity", "Garagem", umid)

        # 🏍️ Sensor 3: Localização da Moto
        # Casos de uso realistas
        caso = random.choice(["normal", "fora", "desaparecida"])
        
        if caso == "normal":
            loc = "Garagem"
        elif caso == "fora":
            loc = "Rua 123"
        elif caso == "desaparecida":
            loc = "DESAPARECIDA"

        enviar_dado("moto-01", "gps", loc, 1 if caso != "desaparecida" else 0)

        print(f"[SIMULAÇÃO] Caso Moto: {caso.upper()}")

        time.sleep(5)  # intervalo entre leituras


if __name__ == "__main__":
    simular()
