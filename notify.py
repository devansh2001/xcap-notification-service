import os
import requests
import json
import pyrebase
import datetime

server_key = os.environ['serverKey']

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



def firebase_cloud_messaging_notification(device_id):
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "to": device_id,
        "notification": {
            "title": "REMINDER: Fill XCAP Survey",
            "body": "Touch here / open the app to fill the XCAP ResearchSurvey"
       }
    }

    body = json.dumps(body)
    headers = {
        'Authorization': 'key=' + server_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=body)

    # print(response.text)

    return response

now = datetime.datetime.now()
notifs = database.child("notification_info").get()
trigger_notifs = []
for notif in notifs:
    scheduled_time = notif['notification_time']
    diff = datetime.timedelta(seconds=300)
    if scheduled_time >= now - diff:
        trigger_notifs.append(notif['device_id'])

for i in range(0, len(trigger_notifs)):
    firebase_cloud_messaging_notification(trigger_notifs[i])