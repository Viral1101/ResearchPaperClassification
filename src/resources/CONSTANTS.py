
from Word import CW


def get_CWs() -> list :
    '''returns a list of mcew (ZW objects)'''

    MCEW = list()

    with open("formatted_CWs.txt" , "r") as reader :

        lines = reader.readlines()

        for line in lines :

            words_in_line = line.split(",")

            #word
            chars = words_in_line[0].lower()

            #frequency per million
            fpm = words_in_line[1]

            #rank
            rank = words_in_line[2]

            MCEW.append(CW(chars , fpm , rank))

    return MCEW

#most common english words
CWs = get_CWs()


#testing
if __name__ == "__main__" :

    for word in CWs :

        print(word.chars , word.fpm , word.rank)
