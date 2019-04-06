
class Word :

    def __init__(self , chars) :

        self.chars = chars


class RPW(Word) :
    '''
    Research Paper Word

    words composed in the research paper
    '''

    def __init__(self , chars , count = 0) :

        Word.__init__(self , chars)

        self.count = count

    def _format(self) :
        '''formats the word (self.chars) to include no invalid characters and be all lower case'''

        new_chars = str()

        valid_chars = "abcdefghijklmnopqrstuvwxyz-"

        for char in self.chars :

            if char in valid_chars :

                new_chars += char

        self.chars = new_chars

    def inc_count(self) :
        '''increments self.count by 1'''

        self.count += 1


class KW(RPW):
    '''
    Keyword
    '''

    def __init__(self, chars , count):

        RPW.__init__(self, chars , count)



class CW(Word) :
    '''
    Common word

    based on Zipf's law
    '''

    def __init__(self , chars , fpm , rank) :

        Word.__init__(self , chars)

        #frequency per million
        self.fpm = fpm

        self.rank = rank




