Sprint 3 - Integrated Delivery (IoT + Vision)

Steps:
1) Create venv and install requirements: python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt
2) Run backend: python backend/app.py
3) Run simulators: bash simulators/run_simulators.sh
4) Copy your 'valid' folder (images + _annotations.coco.json) into project root as 'valid' (next to README_RUN.md)
5) Run vision script: python vision/Iot.py
6) Open dashboard: http://localhost:5000/

Notes:
- The vision script saves annotated images to vision/annotated_output and writes vision/report.json with summary.
- Metrics (detection POST latency) and telemetry/detections persist in backend/systrack.db (SQLite).
