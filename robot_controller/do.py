from robot import *
from conversion import *
import pyrebase

config = {
  "apiKey": null,
  "authDomain": "detritech-fd3cd.firebaseapp.com",
  "databaseURL": "https://detritech-fd3cd.firebaseio.com",
  "storageBucket": "detritech-fd3cd.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
storage = firebase.storage()

def stream_handler(message):
    print('event: ' + message["event"]) # put
    print('path: '  + message["path"]) # /-K7yGTTEp7O549EzTYtI
    print('data: '  + message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    
    print(message["data"] != "")
    if (message["data"] != ""):
        dechets = message["data"]
        dechets_l1 = dechets.split("#")
        dechets_l2 = []
        print(dechets_l1)
        for i in range(len(dechets_l1)):
          dechets_l2.append(list(map(int, dechets_l1[i].split())))
        dechets = conversion_to_robot(dechets_l2)
        tri_dechet(dechets)

my_stream = db.child("coord").stream(stream_handler)
