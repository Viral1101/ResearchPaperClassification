import pyrebase
from flask import *

app = Flask(__name__)
config = {
    "apiKey": "AIzaSyBiES-x7782uGeakjuI1TOT49h_yr9faU0",
    "authDomain": "hackathon2019-236723.firebaseapp.com",
    "databaseURL": "https://hackathon2019-236723.firebaseio.com",
    "projectId": "hackathon2019-236723",
    "storageBucket": "hackathon2019-236723.appspot.com",
    "messagingSenderId": "397133042952"
  }

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def basic():
    return "Hello World"


if __name__ == '__main__':
    app.run()
