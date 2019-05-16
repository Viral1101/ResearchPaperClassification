import pyrebase
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from pub_class.Main import *


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
storage = firebase.storage()


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
    try:
        count = len(docs)
    except:
        count = 0

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
    if docs is not None:
        count = len(docs)
    else:
        count = 0

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
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    import json
    info = json.loads(request.body)

    url = info['url']
    # pub = info['pub_id']

    print(url)


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

    import json
    info = json.loads(request.body)

    url = info['url']
    # pub = info['pub_id']

    print((url,))

    data = []

    title = "Temp Name"

    # print("mili" + str(millis))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    # url = request.POST.get('url')
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    # print("info" + str(a))

    # data = {
    #     "work": work,
    #     'progress': progress,
    #     'url': url
    # }

    # data = '{"title": ' + title + ', "url": ' + url + ',"authors": ' + author_list + ', "phrases": ' + phrase_list + '}'

    authors = {
        "authors":
        [
            "Author1",
            "Author2",
            "Author3"
        ]
    }

    phrase_list2 = {
        "phrases":
        [
            {
                "agree": False,
                "class": 0,
                "phrase": "aegouabevqo3uvbaolejbv",
                "topic": "jibberish"
            },
            {
                "agree": False,
                "class": 0,
                "phrase": "24gohajbervaoejg",
                "topic": "more jibberish"
            }
        ]
    }

    phrase_list = getJSON(url)
    phrase_list = json.loads(phrase_list)
    print(phrase_list)

    data = {
        "title": title,
        "url": url,
        "authors": authors['authors'],
        "phrases": phrase_list
    }

    # print(phrase_list)
    # data['phrases'].append(json.load(phrase_list))

    database.child('users').child(a).child('pubs').child(millis).set(data)
    # database.child('users').child(a).child('pubs').child(millis).update(authors)
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
    comb_lis = zip()
    doc_list = []
    try:
        for doc in docs:
            doc_list.append(doc)
    except:
        doc_list = None

    if doc_list is not None:
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


def predicts(request, pid):
    idtoken = request.session['uid']

    pid = int(pid)

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    import pandas as pd
    data2 = pd.read_csv('E:\\Documents\\GitHub\\ResearchPaperClassification\\src\\pub_class\\test.csv')

    from keras.models import load_model
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    from sklearn.preprocessing import LabelEncoder

    model = load_model('E:\\Documents\\GitHub\\ResearchPaperClassification\\src\\pub_class\\lstm_model.h5')
    text = data2.iloc[pid]['abstract']

    text = [text]

    max_features = 5000
    tokenizer = Tokenizer(num_words=max_features, split=' ')
    tokenizer.fit_on_texts(text)
    X = tokenizer.texts_to_sequences(text)
    print(X)
    X = pad_sequences(X, maxlen=263)
    print(X)

    data = pd.read_csv('E:\\Documents\\GitHub\\ResearchPaperClassification\\src\\pub_class\\training.csv')
    data = data[['abstract', 'mesh']]

    data = data[
        data['mesh'].isin(['Epitopes', 'Immunity, Cellular', 'Staining and Labeling', 'Antibody Formation', 'Genes',
                           'Hydrogen-Ion Concentration', 'Histocompatibility Antigens', 'Electroencephalography',
                           'Antigens', 'HLA Antigens', 'Aging'])]

    data['abstract'] = data['abstract'].apply(lambda x: x.lower())
    data['mesh'] = data['mesh'].apply(lambda x: x.lower())
    labelencoder = LabelEncoder()
    integer_encoded = labelencoder.fit_transform(data['mesh'])

    result = model.predict_classes(X)

    output = labelencoder.inverse_transform(result)[0]

    return render(request, 'predicts.html', {'abstract': text[0], 'mesh': data2.iloc[pid]['mesh'], 'output': output, 'e': name})

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
    return render(request, 'phrases.html', {'comb_lis': comb_lis, 'e': name, 'pid': pid})


def abstract(request):
    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    import pandas as pd
    data2 = pd.read_csv('E:\\Documents\\GitHub\\ResearchPaperClassification\\src\\pub_class\\test.csv')
    ids = list()

    for i in range(0, len(data2)):
        ids.append(i)

    comb_lis = zip(ids, data2['abstract'], data2['mesh'])

    return render(request, 'abstracts.html', {'comb_lis': comb_lis, 'e': name})

def update(request):
    import json
    info = json.loads(request.body)
    # print(info)

    idtoken = request.session['uid']

    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    firstname = database.child('users').child(a).child('details').child('firstname').get().val()
    lastname = database.child('users').child(a).child('details').child('lastname').get().val()
    name = firstname + " " + lastname

    dbupdate = info['output']
    phrases_update = dbupdate['phrases']
    pub = info['pub_id']

    phrase_ids = database.child('users').child(a).child('pubs').child(pub).child('phrases').shallow().get().val()
    phrase_id_ls = []

    for phrase_id in phrase_ids:
        phrase_id_ls.append(phrase_id)

    i = 0
    for phrase in phrases_update:
        database.child('users').child(a).child('pubs').child(pub).child('phrases').child(i).set(phrase)
        print(database.child('users').child(a).child('pubs').child(pub).child('phrases').child(i).get().val())
        i += 1


    # print(dbupdate)
    # print(pub)

    return render(request, 'index.html', {'msg': 'Data Saved.'})

