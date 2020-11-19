# Credits: https://stackoverflow.com/questions/11523918/python-start-a-function-at-given-time

from flask import Flask, request
import requests
from flask_cors import CORS
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

scheduler = BackgroundScheduler()
scheduler.start()

# Fix this - Add server key from environment variable in Heroku
server_key = os.environ['serverKey']

def firebase_cloud_messaging_notification(device_id):
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "to": device_id,
        "notification": {
            "title": "Hello",
            "body": "Yellow"
       }
    }

    body = json.dumps(body)
    headers = {
        'Authorization': 'key=' + server_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=body)

    print(response.text)

    return response

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
def test():
    return 'Hello, World'

@app.route('/schedule-notification', methods=['POST'])
def schedule_notification():
    data = request.get_json()
    input_date_time = data.get('notification_time')
    device_id = data.get('device_id')

    if input_date_time is None or device_id is None:
        return 'Invalid'
    
    print(input_date_time)
    print(device_id)

    # https://stackabuse.com/converting-strings-to-datetime-in-python/ 
    notification_time = datetime.strptime(input_date_time, '%Y-%m-%d %H:%M:%S')
    print(notification_time)

    scheduler.add_job(firebase_cloud_messaging_notification, 'date', run_date=notification_time, args=[device_id])
    print('Scheduled!')
    return 'OK'
