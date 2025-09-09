import json, os, cv2, time, requests, pathlib
from collections import defaultdict

BASE_DIR = pathlib.Path(__file__).parent.resolve()
images_dir = BASE_DIR / "valid"
annotations_path = "_annotations.coco.json"
OUTPUT_DIR = BASE_DIR / "annotated_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BACKEND = os.environ.get('BACKEND_URL', 'http://localhost:5000/detections')

with open(images_dir / annotations_path) as f:
    data = json.load(f)

images = {img['id']: img['file_name'] for img in data['images']}
annotations_per_image = defaultdict(list)
for ann in data['annotations']:
    annotations_per_image[ann['image_id']].append(ann)

for image_id, anns in annotations_per_image.items():
    image_name = images[image_id]
    image_path = images_dir / image_name

    img = cv2.imread(str(image_path))
    if img is None:
        continue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detections = []
    for idx, ann in enumerate(anns):
        x, y, w, h = map(int, ann['bbox'])
        detections.append({
            'id': f'moto_{idx+1}',
            'bbox': [x, y, w, h],
            'confidence': ann.get('score', 1.0)
        })

    payload = {
        'image': image_name,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'detections': detections
    }

    try:
        start = time.time()
        r = requests.post(BACKEND, json=payload, timeout=5)
        latency = (time.time() - start) * 1000
        for d in payload['detections']:
            d['post_latency_ms'] = latency
        print(f"POST {image_name} {r.status_code} Latency: {latency:.2f} ms")
    except Exception as e:
        print("Erro POST:", e)
