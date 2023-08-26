import os
import requests
from datetime import datetime

class Status:
    def __init__(self, status, filename, timestamp, explanation):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation

    def is_done(self):
        return self.status == 'done'

class UploadClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        #URL where Flask application's /upload endpoint is located.
        upload_url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            return response.json()['uid']
        else:
            response.raise_for_status()

    def status(self, uid):
        status_url = f"{self.base_url}/status"
        params = {'uid': uid}
        response = requests.get(status_url, params=params)
        response_data = response.json()

        if response.status_code == 200:
            response_data = response.json()
            status = Status(
                status=response_data['status'],
                filename=response_data['filename'],
                timestamp=response_data['timestamp'],
                explanation=response_data['explanation']
            )
        elif response.status_code == 404:
            # Handle 'not found' case
            status = Status(
                status='not found',
                filename=None,
                timestamp=None,
                explanation=None
            )
        else:
            response.raise_for_status()

        return status
# Usage example
if __name__ == '__main__':
    base_url = 'http://127.0.0.1:5000'
    client = UploadClient(base_url)

    file_path = 'End of course exercise - kickof - upload (1).pptx'
    try:
        uid = client.upload(file_path)
        print(f"Upload successful. UID: {uid}")

        status = client.status(uid)
        print(f"Status: {status.status}")
        print(f"Filename: {status.filename}")
        print(f"Timestamp: {status.timestamp}")
        print(f"Explanation: {status.explanation}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
