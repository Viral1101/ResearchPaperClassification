
from Word import RPW , KW
from CONSTANTS import CWs
import os

import PyPDF2


class RP :

    def __init__(self) :

        self.file_name = None

        self.text = list()

        #list of words (RPW object)
        self.words = list()

        #list of keywords (KW object)
        self.keywords = list()

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



        self.text = text.split("\n")

    def get_words(self) :
        '''parses all the words from the file self.file_name, counts them, and puts them into the list self.words'''

        for line in self.text :

            words = line.split(" ")
            
            for word in words :

                append_new_word = True

                new_word = RPW(word.lower())
                new_word._format()

                if len(new_word.chars) > 0 :

                    if len(self.words) > 1 :
                        
                        for previous_word in self.words :

                            if new_word.chars == previous_word.chars :

                                previous_word.inc_count()

                                append_new_word = False


                    if append_new_word == True :
                    
                        self.words.append(new_word)

    def sort_words_by_count(self) :
        '''sorts all of the words in self.words by their count'''

        self.words.sort(key = lambda word : word.count , reverse = True)


    def get_keywords(self) :
        '''removes all the words that occur in CWsfrom self.words and sets it equal to self.keywords'''

        #zws stands for zipf words (contains the strings of all the zipf words)
        zws = [zw.chars for zw in CWs]

        self.keywords = [KW(word.chars , word.count) for word in self.words]

        remove_count = 0

        for word in self.keywords.copy() :

            #disqualifying conditions for words (RPW object) to become keywords (KW object)
            if word.chars in zws \
                    or len(word.chars) <= 4 :

                self.keywords.remove(word)
                remove_count += 1



            if remove_count == len(CWs) :


                break

    def display_words(self) :
        '''Prints to the console self.words'''

        print("Words: {}".format([(self.words[i].chars , self.words[i].count) for i in range(len(self.words))]))

    def display_keywords(self) :
        '''Prints to the console self.keywords'''

        print("Keywords: {}".format([(self.keywords[i].chars , self.keywords[i].count) for i in range(len(self.keywords))]))

                

