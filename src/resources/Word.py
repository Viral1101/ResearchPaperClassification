

class Word :

    '''
    Research Paper Word
    '''

    def __init__(self , chars , count = 0) :

        self.chars = chars

        self.count = count

    def _format(self) :
        '''formats the word (self.chars) to include no invalid characters and be all lower case'''

        new_chars = str()

        valid_chars = "abcdefghijklmnopqrstuvwxyz-0123456789'%$"

        for char in self.chars :

            if char in valid_chars :

                new_chars += char

        self.chars = new_chars

    def inc_count(self) :
        '''increments self.count by 1'''

        self.count += 1







