from flask import Flask, jsonify, render_template
import subprocess
import psutil
import os
import requests

app = Flask(__name__)
stress_process = None

@app.route('/start_stress', methods=['GET'])
def start_stress():
    global stress_process
    if stress_process is None or stress_process.poll() is not None:
        stress_process = subprocess.Popen(['stress', '--cpu', '1'])
        return jsonify(status="Stress test started"), 200
    else:
        return jsonify(status="Stress test already running"), 409

@app.route('/reboot_instance', methods=['GET'])
def reboot_instance():
    try:
        subprocess.run(['sudo', 'reboot'], check=True)
        return jsonify(status="Reboot initiated"), 200
    except subprocess.CalledProcessError as e:
        return jsonify(status="Reboot failed", error=str(e)), 500

@app.route('/')
def index():
    machine_name = os.uname()[1]
    ip_address = "Unavailable"
    try:
        azure_metadata_url = "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
        headers = {"Metadata": "true"}
        response = requests.get(azure_metadata_url, headers=headers, timeout=2)
        azure_metadata = response.json()
        ip_address = azure_metadata.get("network", {}).get("interface", [])[0].get("ipv4", {}).get("ipAddress", [])[0].get("privateIpAddress", "")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")

    return render_template('index.html', machine_name=machine_name, ip_address=ip_address)

@app.route('/cpu_utilization')
def cpu_utilization():
    utilization = psutil.cpu_percent(interval=1)
    return jsonify(utilization=utilization)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
