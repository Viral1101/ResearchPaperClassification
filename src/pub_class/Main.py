import pub_class.Model as Model
import pub_class.Processing as Processing
from pub_class.sentences_to_json import *
# import Model as Model
# import Processing as Processing
# from sentences_to_json import *
import os
import wget
import json


def getJSON(url):

    #getting pdf file
    import urllib.request

    filename = 'something.pdf'

    # url = "https://firebasestorage.googleapis.com/v0/b/researchclassification.appspot.com/o/docs%2Fexample.pdf?alt=media&token=7821e44c-6851-4750-b50b-13dd8528b533"
    urllib.request.urlretrieve(url, filename)
    # print(url2)
    # wget.download(url2, out = "something.pdf")

    #end getting pdf file

    # preprocessed_file = Processing.preprocess_file(filename)
    # x = Model.create_input_vector(filename)
    # classifications = Model.classify(x)
    # classifications = Model.get_classification_list(filename)

    # print(classifications)

    # data = Processing.readPDF(filename)

    # sentences = Processing.get_sentences(data)
    # for i in range(0, len(sentences)):
    #     print(Processing.format_sentence(sentences[i]))
    #     print(classifications[i])

    #output to json

    # sentences = Model.get_sentence_list(filename)
    # classifications = Model.get_classification_list(filename)
    sentences = Model.create_input_vector(filename)

    count = len(sentences)
    phrases = []
    for i in range(0, count):
        temp = {
            "phrase": sentences[i],
            # "class": int(classifications[i]),
            "class": int(0),
            "agree": False,
            "topic": "Not Implemented"
        }
        phrases.append(temp)

    # output = []
    # for phrase in phrases:
    #     dic = {}
    #     dic['phrase'] = phrase['phrase']
    #     dic['class'] = phrase['class']
    #     dic['agree'] = phrase['agree']
    #     dic['topic'] = phrase['topic']
    #     output.append(dic)

    output = json.dumps(phrases)
    #
    # temp = {
    #     "phrases": phrases
    # }

    # output = {
    #     "phrases": json.dumps(phrases)
    # }
    # output = sentences_classifications_to_json(
    #
    #     sentences,
    #     classifications
    #
    # )

    # os.remove(filename)
    return output
    # Model.train_model(x, classifications)


# if __name__ == '__main__':
#     url = "http://downloads.bbc.co.uk/worldservice/learningenglish/ask_about_english/pdfs/aae_sf_something_of_a.pdf"
#     print("THE END: ", getJSON(url))
