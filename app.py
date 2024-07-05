from flask import Flask, request, jsonify, render_template, redirect, url_for
from google.cloud import storage, firestore
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
from datetime import datetime
import logging

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/logs", methods=["GET"])
def view_logs():
    try:
        logging.debug("Fetching logs from Firestore.")
        firestore_client = firestore.Client()
        logs_ref = firestore_client.collection('execution_logs')
        logs = logs_ref.stream()
        log_entries = [{"id": log.id, **log.to_dict()} for log in logs]
        logging.debug(f"Fetched logs: {log_entries}")
        return render_template("logs.html", logs=log_entries)
    except Exception as e:
        logging.error(f"Error fetching logs: {e}")
        return "Internal Server Error", 500

@app.route("/approve", methods=["GET", "POST"])
def approve_script():
    if request.method == "POST":
        try:
            script_name = request.form["script_name"]
            bucket_name = request.form["bucket_name"]
            logging.debug(f"Approving script: {script_name} in bucket: {bucket_name}")

            # Approve script logic here
            # Placeholder logic for example
            if script_name and bucket_name:
                # Simulate approving script
                logging.info(f"Script {script_name} approved successfully.")
                return "Script approved successfully", 200
            else:
                return "Missing script name or bucket name", 400
        except Exception as e:
            logging.error(f"Error approving script: {e}")
            return "Internal Server Error", 500
    return render_template("approve.html")

@app.route("/edit", methods=["GET", "POST"])
def edit_script():
    if request.method == "POST":
        try:
            script_name = request.form["script_name"]
            bucket_name = request.form["bucket_name"]
            logging.debug(f"Editing script: {script_name} in bucket: {bucket_name}")

            # Edit script logic here
            # Placeholder logic for example
            if script_name and bucket_name:
                # Simulate editing script
                logging.info(f"Script {script_name} edited successfully.")
                return "Script edited successfully", 200
            else:
                return "Missing script name or bucket name", 400
        except Exception as e:
            logging.error(f"Error editing script: {e}")
            return "Internal Server Error", 500
    return render_template("edit.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule_task():
    if request.method == "POST":
        try:
            script_name = request.form["script_name"]
            bucket_name = request.form["bucket_name"]
            schedule_time = request.form["schedule_time"]
            logging.debug(f"Scheduling script: {script_name} in bucket: {bucket_name} at {schedule_time}")

            # Schedule task logic here
            # Placeholder logic for example
            if script_name and bucket_name and schedule_time:
                # Simulate scheduling task
                logging.info(f"Script {script_name} scheduled successfully.")
                return "Script scheduled successfully", 200
            else:
                return "Missing script name, bucket name, or schedule time", 400
        except Exception as e:
            logging.error(f"Error scheduling task: {e}")
            return "Internal Server Error", 500
    return render_template("schedule.html")

@app.route("/publish", methods=["GET", "POST"])
def publish_script():
    if request.method == "POST":
        try:
            script_name = request.form["script_name"]
            bucket_name = request.form["bucket_name"]
            logging.debug(f"Publishing script: {script_name} in bucket: {bucket_name}")

            # Publish script logic here
            # Placeholder logic for example
            if script_name and bucket_name:
                # Simulate publishing script
                logging.info(f"Script {script_name} published successfully.")
                return "Script published successfully", 200
            else:
                return "Missing script name or bucket name", 400
        except Exception as e:
            logging.error(f"Error publishing script: {e}")
            return "Internal Server Error", 500
    return render_template("publish.html")

@app.route("/run", methods=["POST"])
def run_script():
    try:
        data = request.get_json()
        bucket_name = data.get("bucket_name")
        script_name = data.get("script_name")
        argument = data.get("argument", "")

        logging.debug(f"Running script: {script_name} from bucket: {bucket_name} with argument: {argument}")

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

        logging.debug(f"Script output: {result.stdout}")
        logging.error(f"Script error: {result.stderr}")

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

        logging.info(f"Script run completed: {response}")
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error running script: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8080)