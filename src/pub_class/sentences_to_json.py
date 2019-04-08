


from nltk.corpus import stopwords
import Model

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


        self.data += \
"""
 {
    "phrases" :
    [
"""
        for i , sentence in enumerate(self.sentences) :

            self.data += \
"""
        {{
            "class" : {}
            "phrase": "{}",
            "topic" : "{}",
            "agree" : {}
        }} {}
""".format(sentence.classification , sentence.text , sentence.get_topic() , "False" , "," if i < len(self.sentences) - 1 else "")


        self.data += \
"""
    ]
}
"""

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
    return json.data
    # json.write_data()

'''
file_name = "example.pdf"

sentences_classifications_to_json(

    Model.get_sentence_list(file_name) ,
    Model.get_classification_list(file_name)

)
'''




