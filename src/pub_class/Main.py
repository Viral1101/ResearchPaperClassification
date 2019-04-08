import Model
import Processing
from sentences_to_json import *
import os
import wget


def getJSON(url):

    #getting pdf file

    #url = "http://downloads.bbc.co.uk/worldservice/learningenglish/ask_about_english/pdfs/aae_sf_something_of_a.pdf"

    wget.download(url , out = "something.pdf")

    #end getting pdf file


    filename = 'something.pdf'
    preprocessed_file = Processing.preprocess_file(filename)
    x = Model.create_input_vector(filename)
    classifications = Model.classify(x)

    data = Processing.readPDF(filename)

    sentences = Processing.get_sentences(data)
    for i in range(0, len(sentences)):
        print(Processing.format_sentence(sentences[i]))
        print(classifications[i])

    #output to json

    sentences = Model.get_sentence_list(filename)
    classifications = Model.get_classification_list(filename)

    output = sentences_classifications_to_json(

        sentences,
        classifications

    )

    # os.remove(filename)
    return output
    # Model.train_model(x, classifications)


# if __name__ == '__main__':
#     url = "http://downloads.bbc.co.uk/worldservice/learningenglish/ask_about_english/pdfs/aae_sf_something_of_a.pdf"
#     print("THE END: ", getJSON(url))
