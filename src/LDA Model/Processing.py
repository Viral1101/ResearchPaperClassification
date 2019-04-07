import nltk
import string
import PyPDF2


def readPDF(filename):
    data = ""
    reader = PyPDF2.PdfFileReader(open(filename, 'rb'))
    for i in range(0, reader.getNumPages()):
        data += reader.getPage(i).extractText()
    return data


def get_sentences(data):
    sentence_list = list()
    sentences = nltk.sent_tokenize(data)
    for sentence in sentences:
        sentence_list.append(sentence)
    return sentence_list


def get_words(data):
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # Tokenize the text and apply lemmatization
    lemma_list = list()
    words = nltk.word_tokenize(data)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for word in words:
        word = word.lower()

        new_word = ""
        for char in word:
            if char.isalnum():
                new_word += char
        word = new_word

        if word not in stop_words:
            if word not in string.punctuation:
                lemma = lemmatizer.lemmatize(word)
                lemma_list.append(lemma)

    # Return lemmatized list of words
    return lemma_list


def preprocess_file(filename):
    # Read in PDF
    data = readPDF(filename)
    return get_words(data)


def encode_ngram(model, ngram):
    n = len(ngram)
    vector = 0 * model.wv[ngram[0]]
    for word in ngram:
        vector += model.wv[word]
    vector /= n
    return vector


def accept_char(char):
    if char.isalnum():
        return True
    elif char.isspace():
        return True
    elif char in string.punctuation:
        return True
    else:
        return False


def format_sentence(sentence):
    new_sentence = ""
    for char in sentence:
        if char.isspace():
            char = ' '
        if accept_char(char):
            new_sentence += char
    return new_sentence


def classification_to_text(classification):
    if classification == 0:
        return 'Core'
    elif classification == 1:
        return 'Peripheral'
    else:
        return 'Other'


def text_to_classification(text):
    if text == 'core':
        return 0
    elif text == 'peripheral':
        return 1
    else:
        return 2
