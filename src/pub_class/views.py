import pyrebase
from django.shortcuts import render
from django.contrib.auth import views as auth_views

config = {
    "apiKey": "AIzaSyBiES-x7782uGeakjuI1TOT49h_yr9faU0",
    "authDomain": "hackathon2019-236723.firebaseapp.com",
    "databaseURL": "https://hackathon2019-236723.firebaseio.com",
    "projectId": "hackathon2019-236723",
    "storageBucket": "hackathon2019-236723.appspot.com",
    "messagingSenderId": "397133042952",
    "serviceAccount": "resources/hackathon2019-236723-firebase-adminsdk-gws9s-1fde13929b.json"
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def singIn(request):
    return render(request, "login.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "signIn.html", {"messg": message})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "welcome.html", {"e": email})


def logout(request):
    auth_views.LogoutView.as_view()
    return render(request, 'signIn.html')


def signup(request):
    return render(request, "SignUp.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.create_user_with_email_and_password(email, passw)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    uid = user['localId']
    data = {"name": name, "status": "1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request, "SignIn.html")


def create(request):
    return render(request, 'create.html')


def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('America/Chicago')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    print("mili" + str(millis))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    url = request.POST.get('url')
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    print("info" + str(a))

    data = {
        "work": work,
        'progress': progress,
        'url': url
    }

    database.child('users').child(a).child('pubs').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request, 'welcome.html', {'e': name})


def check(request):
    import datetime

    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestamps = database.child('users').child(a).child('pubs').shallow().get().val()
    lis_time = []

    for i in timestamps:
        lis_time.append(i)

    lis_time.sort(reverse=True)
    print(lis_time)
    work = []

    for i in lis_time:
        wor = database.child('users').child(a).child('pubs').child(i).child('work').get().val()
        work.append(wor)

    print(work)

    date = []

    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    print(date)

    comb_lis = zip(lis_time, date, work)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request, 'check.html', {'comb_lis': comb_lis, 'e': name})


def post_check(request):
    import datetime

    time = request.GET.get('z')
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    work = database.child('users').child(a).child('pubs').child(time).child('work').get().val()
    progress = database.child('users').child(a).child('pubs').child(time).child('progress').get().val()
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request, 'post_check.html', {'w': work, 'p': progress, 'd': dat, 'e': name})
