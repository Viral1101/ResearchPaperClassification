from nltk.corpus import stopwords
import pub_class.Model as Model
# import Model as Model
import json

STOPWORDS = stopwords.words("english")


class Sentence :

    def __init__(self , text , classification) :

        self.text = text
        self.classification = classification

    def get_topic(self) :

        topic = str()

        for word in self.text.split(" ") :

            if word not in STOPWORDS :

                topic += word + " "

        return topic

class JSON_File :

    def __init__(self) :

        #list of phrases
        self.sentences = list()

        self.data = str()

    def get_sentences(self , sentence_texts , sentence_classifications) :

        for sentence_text , sentence_classification in zip(sentence_texts , sentence_classifications) :

            self.sentences.append(Sentence(sentence_text , sentence_classification))

    def set_phrases(self , phrases) :

        self.phrases = phrases

    def get_data(self) :

        self.data = json.dumps(
            {"phrases":
             [
                 {
                     "class": int(sentence.classification),
                     "phrase": sentence.text,
                     "topic": sentence.get_topic(),
                     "agree": False
                 }for sentence in self.sentences
             ]}
        )

    def write_data(self) :

        with open("json_example.json" , "w") as writer :

            writer.write(self.data)

    def display_data(self) :

        print(self.data)


def sentences_classifications_to_json(sentences , classifications) :

    json = JSON_File()

    json.get_sentences(sentences , classifications)
    json.get_data()
    json.display_data()
    return json.loads(json.data)
    # json.write_data()
    # return "json_example.json"

'''
file_name = "example.pdf"

sentences_classifications_to_json(

    Model.get_sentence_list(file_name) ,
    Model.get_classification_list(file_name)

)
'''




