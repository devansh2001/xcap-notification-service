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

now = datetime.datetime.now()
notifs = database.child("notification_info").get()
trigger_notifs = []
for notif in notifs.each():
    data = notif.val()
    key = notif.key()
    print(key)
    scheduled_time = datetime.datetime.strptime(data['notification_time'], '%Y-%m-%d %H:%M:%S')
    diff = datetime.timedelta(seconds=60 * 60 * 24 * 3)
    print('Removing notfication data', scheduled_time, now, now - scheduled_time, diff)
    if (now - scheduled_time > diff):
        # delete
        print('Will delete', scheduled_time)
        pass
    else:
        print('Will not delete', scheduled_time)