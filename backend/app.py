from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import oracledb
import os
import time

app = Flask(__name__)
CORS(app)


DB_USER = ""
DB_PASS = ""
DB_DSN  = oracledb.makedsn("", 1521, sid="")

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)



@app.route("/")
def index():
    return send_from_directory("dashboard", "index.html")


@app.route("/device_update", methods=["POST"])
def device_update():
    data = request.json
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sensors (sensor_name, sensor_type, location, last_value, last_update)
            VALUES (:1, :2, :3, :4, SYSTIMESTAMP)
        """, [data.get("id"), data.get("type"), data.get("location"), data.get("value")])
        conn.commit()
    return jsonify({"ok": True})


@app.route("/detections", methods=["POST", "GET"])
def detections():
    if request.method == "POST":
        data = request.json
        timestamp = data.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
        num_detections = len(data.get("detections", []))
        post_latency_ms = max(
            [d.get("post_latency_ms", 0) for d in data.get("detections", [])],
            default=0
        )

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO detections (image, detections, post_latency_ms, timestamp)
                VALUES (:1, :2, :3, TO_TIMESTAMP(:4, 'YYYY-MM-DD HH24:MI:SS'))
            """, [data.get("image"), num_detections, post_latency_ms, timestamp])
            conn.commit()
        return jsonify({"ok": True})

    else:  
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT image,
                       detections,
                       TO_CHAR(timestamp, 'DD/MM/YYYY HH24:MI:SS'),
                       post_latency_ms
                FROM detections
                ORDER BY timestamp DESC
            """)
            rows = cur.fetchall()

        result = [
            {
                "image": r[0],
                "detections": int(r[1]),
                "sent": True,
                "timestamp": r[2],
                "post_latency_ms": float(r[3]) if r[3] else 0
            } for r in rows
        ]
        return jsonify(result)


@app.route("/devices", methods=["GET"])
def get_devices():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, sensor_name, sensor_type, location, last_value,
                   TO_CHAR(last_update, 'DD/MM/YYYY HH24:MI:SS')
            FROM sensors
            ORDER BY id
        """)
        rows = cur.fetchall()

    result = [
        {
            "id": r[0],
            "name": r[1],
            "type": r[2],
            "location": r[3],
            "value": r[4],
            "last_update": r[5]
        }
        for r in rows
    ]
    return jsonify(result)


@app.route("/dashboard/<path:path>")
def serve_dashboard(path):
    return send_from_directory("dashboard", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
