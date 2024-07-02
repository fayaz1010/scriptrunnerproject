from flask import Flask, request, jsonify, render_template, redirect, url_for
from google.cloud import storage, firestore
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/logs", methods=["GET"])
def view_logs():
    firestore_client = firestore.Client()
    logs_ref = firestore_client.collection('execution_logs')
    logs = logs_ref.stream()
    log_entries = [log.to_dict() for log in logs]
    return render_template("logs.html", logs=log_entries)

@app.route("/approve", methods=["GET", "POST"])
def approve_script():
    if request.method == "POST":
        # Approve script logic here
        return redirect(url_for("view_logs"))
    return render_template("approve.html")

@app.route("/edit", methods=["GET", "POST"])
def edit_script():
    if request.method == "POST":
        # Edit script logic here
        return redirect(url_for("view_logs"))
    return render_template("edit.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule_task():
    if request.method == "POST":
        # Schedule task logic here
        return redirect(url_for("view_logs"))
    return render_template("schedule.html")

@app.route("/publish", methods=["GET", "POST"])
def publish_script():
    if request.method == "POST":
        # Publish script logic here
        return redirect(url_for("view_logs"))
    return render_template("publish.html")

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()
    bucket_name = data.get("bucket_name")
    script_name = data.get("script_name")
    argument = data.get("argument", "")

    # Download the script from Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(script_name)
    script_path = f"/tmp/{script_name}"
    blob.download_to_filename(script_path)

    # Execute the script
    result = subprocess.run(['python', script_path, argument], capture_output=True, text=True)

    response = {
        "output": result.stdout,
        "error": result.stderr,
        "returncode": result.returncode
    }

    # Store the execution result in Firestore
    firestore_client = firestore.Client()
    doc_ref = firestore_client.collection('execution_logs').document()
    doc_ref.set({
        'bucket_name': bucket_name,
        'script_name': script_name,
        'argument': argument,
        'output': result.stdout,
        'error': result.stderr,
        'returncode': result.returncode,
        'timestamp': datetime.utcnow()
    })

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
