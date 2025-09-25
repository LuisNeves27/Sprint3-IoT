from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import oracledb
import time

app = Flask(__name__)
CORS(app)

DB_USER = "rm558127"
DB_PASS = "270406"
DB_DSN  = oracledb.makedsn("oracle.fiap.com.br", 1521, sid="orcl")

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
            MERGE INTO sensors s
            USING (SELECT :id AS id FROM dual) d
            ON (s.id = d.id)
            WHEN MATCHED THEN
              UPDATE SET sensor_name = :name,
                         sensor_type = :type,
                         location = :location,
                         last_value = :value,
                         last_update = SYSTIMESTAMP
            WHEN NOT MATCHED THEN
              INSERT (id, sensor_name, sensor_type, location, last_value, last_update)
              VALUES (:id, :name, :type, :location, :value, SYSTIMESTAMP)
        """, {
            "id": data["id"],
            "name": data["name"],
            "type": data["type"],
            "location": data["location"],
            "value": data["value"]
        })
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

@app.route("/occurrences", methods=["GET"])
def get_occurrences():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT o.id,
                       o.description,
                       l.city,
                       l.state,
                       o.weather,
                       o.severity_level,
                       TO_CHAR(SYSTIMESTAMP, 'DD/MM/YYYY HH24:MI:SS') AS timestamp
                FROM occurrences o
                JOIN locations l ON o.location_id = l.id
                ORDER BY o.id DESC
            """)
            rows = cur.fetchall()
            
            # Debug: imprimir no console
            print(f"Found {len(rows)} occurrences")
            for row in rows:
                print(row)

        result = [
            {
                "id": r[0],
                "description": r[1],
                "city": r[2],
                "state": r[3],
                "weather": r[4],
                "severity": r[5],
                "timestamp": r[6]
            }
            for r in rows
        ]
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in /occurrences: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Rotas de debug para teste
@app.route("/test-db")
def test_db():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM dual")
            result = cur.fetchone()
            return jsonify({"db_connection": "success", "result": result[0]})
    except Exception as e:
        return jsonify({"db_connection": "failed", "error": str(e)})

@app.route("/debug/occurrences")
def debug_occurrences():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            # Verifica se há dados na tabela
            cur.execute("SELECT COUNT(*) FROM occurrences")
            count = cur.fetchone()[0]
            
            cur.execute("SELECT * FROM occurrences")
            rows = cur.fetchall()
            
            return jsonify({
                "count": count,
                "data": rows,
                "columns": [desc[0] for desc in cur.description]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/dashboard/<path:path>")
def serve_dashboard(path):
    return send_from_directory("dashboard", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)