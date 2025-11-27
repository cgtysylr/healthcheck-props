from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Varsayılan healthcheck JSON'u
default_healthcheck = {
  "status": "UnHealthy",
  "totalDuration": "00:00:00.1234567",
  "entries": {
    "Database": {
      "status": "UnHealthy",
      "description": "Database Running",
      "duration": "00:00:00.0123456",
      "tags": [
        "core",
        "database",
        "postgres"
      ],
      "priority": "CRITICAL",
      "data": {
        "total": "Post Count 20456"
      }
    },
    "Edocbroker": {
      "status": "Healthy",
      "description": "Edocbroker Not Connecting",
      "duration": "00:00:00.0234567",
      "tags": [
        "internal",
        "application"
      ],
      "priority": "OPTIONAL",
      "data": {
        "error": "Timeout occurred while connecting to example dependency 2."
      }
    },
    "Graylog": {
      "status": "Healthy",
      "description": "Logging",
      "duration": "00:00:00.0234567",
      "tags": [
        "internal",
        "application",
        "thirdparty"
      ],
      "priority": "OPTIONAL",
      "data": {}
    },
    "Keycloak": {
      "status": "Healthy",
      "description": "Authentication",
      "duration": "00:00:00.0234567",
      "tags": [
        "internal",
        "application",
        "thirdparty"
      ],
      "priority": "DEPENDS",
      "data": {}
    },
    "GIB": {
      "status": "Degraded",
      "description": "Example dependency 3 is experiencing higher than normal latency.",
      "duration": "00:00:00.0345678",
      "tags": [
        "external",
        "rabbitmq"
      ],
      "priority": "CRITICAL",
      "data": {
        "latency": "200ms"
      }
    },
    "AWS": {
      "status": "Healthy",
      "description": "AWS Connected",
      "duration": "00:00:00.0345678",
      "tags": [
        "external",
        "cloud"
      ],
      "priority": "DEPENDS",
      "data": {
        "latency": "200ms"
      }
    }
  }
}

# Mevcut healthcheck JSON'u (başlangıçta default)
current_healthcheck = default_healthcheck.copy()

# Live endpoint durumu (başlangıçta True = 200)
live_status = True

@app.route('/health/ready', methods=['GET'])
def health_ready():
    """Healthcheck ready endpoint - mevcut healthcheck JSON'unu döndürür"""
    return jsonify(current_healthcheck), 200

@app.route('/health/live', methods=['GET'])
def health_live():
    """Healthcheck live endpoint - live_status'a göre 200 veya 500 döndürür"""
    if live_status:
        return jsonify({"status": "alive"}), 200
    else:
        return jsonify({"status": "down"}), 500

@app.route('/live-down', methods=['GET'])
def live_down():
    """Live durumunu toggle eder (200 <-> 500)"""
    global live_status
    live_status = not live_status
    status_text = "200" if live_status else "500"
    return jsonify({
        "message": f"Live status toggled. /health/live will now return {status_text}",
        "current_status": "alive" if live_status else "down"
    }), 200

@app.route('/set-healthcheck', methods=['POST'])
def set_healthcheck():
    """POST edilen JSON'u healthcheck olarak ayarlar"""
    global current_healthcheck
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        current_healthcheck = data
        return jsonify({
            "message": "Healthcheck updated",
            "healthcheck": current_healthcheck
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

