
from Word import Word
import os
from nltk.corpus import stopwords
from N_Gram import N_Gram
import PyPDF2


class RP :

    def __init__(self) :

        self.file_name = None

        self.text = list()

        #list of words (RPW object)
        self.words = list()

        self.n_limit = int()

        #list of n_gram objects
        self.n_grams = list()

        #list of dictionaries
        self.n_gram_counts = list()

        #list of stopwords
        self.sws = set(stopwords.words('english'))

    def set_file_name(self , file_name) :
        '''checks if the file is in the current working directory and if it is, sets self.file_name equal to that file's name'''

        try :

            if file_name in os.listdir() :

                self.file_name = file_name


            else :

                raise ValueError

        except ValueError :

            print("Error. {} is not in {}".format(file_name , os.getcwd()))

    def get_text(self) :
        '''sets self.text equal to a list of the lines (as strings) of the file (self.file_name)'''

        reader = open(self.file_name, 'rb')
        # The pdfReader variable is a readable object that will be parsed
        pdf_reader = PyPDF2.PdfFileReader(reader)
        # discerning the number of pages will allow us to parse through all #the pages
        num_pages = pdf_reader.numPages
        count = 0
        text = ""

        # The while loop will read each page
        while count < num_pages:
            pageObj = pdf_reader.getPage(count)
            count += 1
            text += pageObj.extractText()



        self.text = text

    def get_stop_words(self) :

        with open("SWs.txt" , "r") as reader :

            self.sws = reader.readlines()

        for i , sw in enumerate(self.sws) :

            sw = list(sw)
            sw.pop(-1)

            self.sws[i] = "".join(sw)

    def display_sws(self) :

        for sw in self.sws :

            print(sw)

    def get_words(self) :
        '''parses all the words from the file self.file_name, counts them, and puts them into the list self.words'''
        '''FIXME'''

        delimiters = ["\n" , "\t" , "." , "," , "?" , "/"]

        for delimiter in delimiters :

            self.text = self.text.replace(delimiter , " ")

        words = self.text.split(" ")


        for word in words :

            new_word = Word(word.lower())
            new_word._format()

            if len(new_word.chars) > 0 :

                self.words.append(new_word)

    def set_n_limit(self , n_limit) :

        self.n_limit = n_limit

    def get_n_grams(self) :

        def const_lst_n_grams(degree , words):

            lst_n_grams = list()

            for i in range(len(words)):

                if i <= (len(words) - degree):
                    lst_n_grams.append(
                        N_Gram(degree , [words[i + n] for n in range(degree)])
                    )



            return lst_n_grams

        for degree in range(1 , self.n_limit + 1) :

            self.n_grams.append(const_lst_n_grams(degree , self.words))

    def filter_n_grams(self) :

        for degree in range(self.n_limit) :

            for n_gram in self.n_grams[degree].copy() :

                for word in n_gram.words :

                    if word.chars in self.sws :

                        try :

                            self.n_grams[degree].remove(n_gram)

                        except ValueError :

                            is_something_wrong = "no"

    def display_n_grams(self) :

        for degree in range(self.n_limit) :

            for n_gram in self.n_grams[degree][:10] :

                print([word.chars for word in n_gram.words] , n_gram.count , end = " ")

            print()

    def get_n_gram_counts(self) :
        '''list of dictionaries of containingn_gram_counts by their words'''

        for degree in range(self.n_limit) :

            self.n_gram_counts.append(dict())

            for n_gram in self.n_grams[degree] :

                #",".join([word.chars for word in n_gram.words])
                try :

                    self.n_gram_counts[degree][",".join([word.chars for word in n_gram.words])] += 1

                except KeyError :

                    self.n_gram_counts[degree][",".join([word.chars for word in n_gram.words])] = 1

    def display_n_gram_counts(self) :
        ''''''

        for degree in range(self.n_limit) :

            iterations = 0

            for n_gram , count in self.n_gram_counts[degree].items() :

                print(n_gram , count , end = " ")

                iterations += 1

                if iterations == 10 :

                    break

            print()

    def sort_n_grams(self) :

        self.n_grams = list()

        for degree in range(self.n_limit) :

            self.n_grams.append(list())

            for words , count in self.n_gram_counts[degree].items() :

                self.n_grams[degree].append(

                    N_Gram(

                        degree + 1 ,

                        [Word(word) for word in words.split(",")] ,

                        count
                    )

                )

        for degree in range(self.n_limit) :

            self.n_grams[degree].sort(key = lambda n_gram : n_gram.count , reverse = True)









                

