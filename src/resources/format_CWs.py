
with open("CWs.txt" , "r") as reader :

    reader.readline()
    lines = reader.readlines()

whitespaces = [" " , "\t"]


with open("formatted_CWs.txt" , "w") as writer :

    del lines[0]

    for line in lines :

        new_line = str()

        for i , char in enumerate(line) :

            if char in whitespaces :

                if line[i - 1] not in whitespaces :

                    new_line += ","

            else :

                new_line += char

        new_line = new_line.split(",")

        
        new_line.pop(2)
        new_line.pop(3) #the list shrinks 1 (it is actually deleting the fourth element)
        
            
        #each line: word, frequency per million, rank
        writer.write(",".join(new_line) + "\n")
