# Credits: https://stackoverflow.com/questions/11523918/python-start-a-function-at-given-time

from flask import Flask, request
import requests
from flask_cors import CORS
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import pyrebase
# scheduler = BackgroundScheduler()
# scheduler.start()

# Fix this - Add server key from environment variable in Heroku
# server_key = os.environ['serverKey']

# def firebase_cloud_messaging_notification(device_id):
#     url = "https://fcm.googleapis.com/fcm/send"
#     body = {
#         "to": device_id,
#         "notification": {
#             "title": "REMINDER: Fill XCAP Survey",
#             "body": "Touch here / open the app to fill the XCAP ResearchSurvey"
#        }
#     }

#     body = json.dumps(body)
#     headers = {
#         'Authorization': 'key=' + server_key,
#         'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, data=body)

#     # print(response.text)

#     return response

app = Flask(__name__)
CORS(app, support_credentials=True)

firebaseConfig = {
    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "databaseURL": os.environ['databaseURL'],
    "projectId": os.environ['projectId'],
    "storageBucket": os.environ['storageBucket'],
    "serviceAccount": {
        "type": os.environ['type'],
        "project_id": os.environ['project_id'],
        "private_key_id": os.environ['private_key_id'],
        "private_key": os.environ['private_key'].replace('\\n', '\n'),
        "client_email": os.environ['client_email'],
        "client_id": os.environ['client_id'],
        "auth_uri": os.environ['auth_uri'],
        "token_uri": os.environ['token_uri'],
        "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
        "client_x509_cert_url": os.environ['client_x509_cert_url']
    },
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId'],
    "measurementId": os.environ['measurementId']
}
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()


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
    
    # print(input_date_time)
    # print(device_id)

    # https://stackabuse.com/converting-strings-to-datetime-in-python/ 
    notification_time = datetime.strptime(input_date_time, '%Y-%m-%d %H:%M:%S')
    # print(notification_time)

    save_info = {}
    save_info['notification_time'] = notification_time
    save_info['device_id'] = device_id

    # Add notfication_time and device_id to Firebase database
    database.child("notification_info").save(save_info)
    # scheduler.add_job(firebase_cloud_messaging_notification, 'date', run_date=notification_time, args=[device_id])
    # print('Scheduled!')
    return 'OK'
