# simulators/simulate_vision.py
import requests
import time
import random

BACKEND = "http://localhost:5000/detections"  # ajuste se necessário

IMAGES = ["img001.jpg", "img002.jpg", "img003.jpg", "img004.jpg"]

def simulate_once(image_name):
    # gerar detections (lista) — compatível com backend que faz len(detections)
    n = random.randint(0, 4)
    detections = []
    for i in range(n):
        detections.append({
            "id": f"moto_{i+1}",
            "bbox": [random.randint(0, 200), random.randint(0,200), random.randint(20,80), random.randint(20,80)],
            "score": round(random.uniform(0.5, 1.0), 2)
        })

    payload = {
        "image": image_name,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "detections": detections
    }

    try:
        start = time.time()
        r = requests.post(BACKEND, json=payload, timeout=6)
        latency = (time.time() - start) * 1000.0
        print(f"[POST detections] {image_name} -> status {r.status_code}, detections={len(detections)}, latency={latency:.2f} ms")
        # opcional: enviar um evento de correção ou log com a latência para o backend se precisar
    except Exception as e:
        print("[ERROR detections POST]", e)

def main():
    print("Simulador de visão iniciado...")
    while True:
        img = random.choice(IMAGES)
        simulate_once(img)
        time.sleep(4)  # intervalo entre envios

if __name__ == "__main__":
    main()
