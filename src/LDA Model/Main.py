import Model
import Processing
from sentences_to_json import *
import urllib.request

url = "https://firebasestorage.googleapis.com/v0/b/researchclassification.appspot.com/o/docs%2Ftp53.pdf?alt=media&token=33b5d344-07ed-4c09-9d6a-7cea18747b25"
destination = "/Users/iamjo/Desktop/destination/something.pdf"

def get_file(url) :

    urllib.request.urlretrieve(url, destination)


if __name__ == '__main__':


    filename = 'example_4.pdf'
    preprocessed_file = Processing.preprocess_file(filename)
    x = Model.create_input_vector(filename)

    classifications = Model.classify(x)

    data = Processing.readPDF(filename)

#url and id

    sentences = Processing.get_sentences(data)
    for i in range(0, len(sentences)):
        print(Processing.format_sentence(sentences[i]))
        print(classifications[i])

    get_file(url)
    json = JSON_File()

    json.get_sentences(sentences, classifications)
    json.get_data()
    json.display_data()
    json.write_data()


    # Model.train_model(x, classifications)
