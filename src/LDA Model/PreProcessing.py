import nltk
import string
import PyPDF2


def preprocess(filename):
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # Read in PDF
    data = ""
    reader = PyPDF2.PdfFileReader(open(filename, 'rb'))
    for i in range(0, reader.getNumPages()):
        data += reader.getPage(i).extractText()

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


def encode_ngram(model, ngram):
    n = len(ngram)
    vector = 0 * model.wv[ngram[0]]
    for word in ngram:
        vector += model.wv[word]
    vector /= n
    return vector
