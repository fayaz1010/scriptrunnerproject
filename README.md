# ScriptRunner Project

## Overview
The ScriptRunner Project automates the development and deployment of code to Google Cloud Run, allowing you to see the output and errors directly from the cloud.

## Features
- Automated build and deployment with Google Cloud Build
- Easy management of scripts through a web interface
- Real-time log viewing
- Script approval, editing, scheduling, and publishing functionalities

## Getting Started

### Prerequisites
- Google Cloud account
- GitHub account
- Google Cloud SDK installed
- Docker installed

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/fayaz1010/scriptrunnerproject.git
    cd scriptrunnerproject
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google Cloud:
    - Enable the Cloud Run API
    - Enable the Cloud Build API
    - Create a service account and download the JSON key

4. Update `cloudbuild.yaml` with your project ID:
    ```yaml
    steps:
      - name: 'gcr.io/cloud-builders/docker'
        args: ['build', '-t', 'gcr.io/YOUR_PROJECT_ID/scriptrunner', '.']
      - name: 'gcr.io/cloud-builders/docker'
        args: ['push', 'gcr.io/YOUR_PROJECT_ID/scriptrunner']
      - name: 'gcr.io/cloud-builders/gcloud'
        args: ['run', 'deploy', 'scriptrunner', '--image', 'gcr.io/YOUR_PROJECT_ID/scriptrunner', '--platform', 'managed', '--region', 'us-central1', '--allow-unauthenticated']

    options:
      logging: CLOUD_LOGGING_ONLY
    ```

5. Commit and push the changes:
    ```bash
    git add .
    git commit -m "Added README.md and updated cloudbuild.yaml"
    git push origin main
    ```

### Usage
1. **Approve a Script**: Navigate to `/approve`, enter the script name and bucket name, and click "Approve".
2. **Edit a Script**: Navigate to `/edit`, enter the script name and bucket name, and click "Edit".
3. **Schedule a Script**: Navigate to `/schedule`, enter the script name, bucket name, and schedule time, and click "Schedule".
4. **Publish a Script**: Navigate to `/publish`, enter the script name and bucket name, and click "Publish".
5. **View Logs**: Navigate to `/logs` to view the execution logs.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

### License
This project is licensed under the MIT License.
