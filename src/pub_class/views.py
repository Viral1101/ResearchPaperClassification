import pyrebase
from django.shortcuts import render
from django.contrib.auth import views as auth_views

config = {
    "apiKey": "AIzaSyBFGDWiQz7cDvw-hFdYidFpWWeMWqPF078",
    "authDomain": "researchclassification.firebaseapp.com",
    "databaseURL": "https://researchclassification.firebaseio.com",
    "projectId": "researchclassification",
    "storageBucket": "researchclassification.appspot.com",
    "messagingSenderId": "383247879128"
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


def login(request):
    return render(request, "login.html")


def index(request):
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    count = 0

    docs = database.child('users').child(a).child('pubs').shallow().get().val()
    if len(docs):
        count = len(docs)

    return render(request, "index.html", {'e': name, 'count': count})


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "login.html", {"messg": message})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    count = 0

    docs = database.child('users').child(a).child('pubs').shallow().get().val()
    if len(docs):
        count = len(docs)

    return render(request, "index.html", {'e': name, 'count': count})


def logout(request):
    auth_views.LogoutView.as_view()
    return render(request, 'login.html')


def register(request):
    return render(request, "register.html")


def postsignup(request):
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.create_user_with_email_and_password(email, passw)
    except:
        message = "Unable to create account try again"
        return render(request, "register.html", {"messg": message})

    uid = user['localId']
    data = {"firstname": firstname, "lastname": lastname, "status": "1"}
    database.child("users").child(uid).child("details").set(data)
    return postsign(request)


def create(request):
    return render(request, 'create.html')


def upload(request):
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    return render(request, "upload.html", {'e': name})


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

    # data = {
    #     "work": work,
    #     'progress': progress,
    #     'url': url
    # }

    data = {
        'url': url
    }

    database.child('users').child(a).child('pubs').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request, 'index.html', {'e': name})


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

def publications(request):

    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    docs = database.child('users').child(a).child('pubs').shallow().get().val()
    doc_list = []
    for doc in docs:
        doc_list.append(doc)

    titles = []
    for i in doc_list:
        title = database.child('users').child(a).child('pubs').child(i).child('title').get().val()
        titles.append(title)

    authors_list = []
    for i in doc_list:
        authr = database.child('users').child(a).child('pubs').child(i).child('authors').get().val()
        authors_list.append(authr)

    urls = []
    for i in doc_list:
        url = database.child('users').child(a).child('pubs').child(i).child('url').get().val()
        urls.append(url)

    comb_lis = zip(doc_list, titles, authors_list, urls)
    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    return render(request, 'publications.html', {'comb_lis': comb_lis, 'e': name})


def phrases(request, pid):

    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    phrase_ids = database.child('users').child(a).child('pubs').child(pid).child('phrases').shallow().get().val()
    phrase_id_ls = []

    for phrase_id in phrase_ids:
        phrase_id_ls.append(phrase_id)

    agrees = []
    phrases = []
    cores = []
    topics = []

    for i in phrase_id_ls:
        agree = database.child('users').child(a).child('pubs').child(pid).child('phrases').child(i).child('agree').get().val()
        agrees.append(agree)

        phrase = database.child('users').child(a).child('pubs').child(pid).child('phrases').child(i).child('phrase').get().val()
        phrases.append(phrase)

        core = database.child('users').child(a).child('pubs').child(pid).child('phrases').child(i).child('class').get().val()
        cores.append(core)

        topic = database.child('users').child(a).child('pubs').child(pid).child('phrases').child(i).child('topic').get().val()
        topics.append(topic)

    comb_lis = zip(phrase_id_ls, agrees, phrases, cores, topics)
    return render(request, 'phrases.html', {'comb_lis': comb_lis, 'e': name})
