class FileReader:

    '''This class is opening a file and gives us functionality to drain an amount of words from the file.
       In order to take all the words that are inside the file, you must create a while loop and every time
       call the getWords(amount) method until hasNext() return False. Don't forget to close FileReader when
       you're done!!!'''
       
    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
    def __init__(self, filename):

        '''FileReader Constructor.'''


        #This is the error messanger.
        #If not change, it means everything is OK.
        self.error = ""

        #End Of file flag.
        self.eof = False

        #Where i'am inside the file.
        self.fileIndex = -1

        #Unwanted Symbols.
        self.unwantedSymbols = ['\n', '!', '@', '#', '$', '%','^',
                                '&', '*', '(', ')', '-', '_', '+',
                                '=', '\\', '|', '[', ']', '{', '}',
                                ';', ':', '"', ',', '.', '<',
                                '>', '/', '?', '\t']

        #Try to open the file.
        try:
            self.file = open(filename, "r")
            pass

        #The file could not been found.
        except FileNotFoundError:
            self.error = 'FileReaderError: The file: "'+filename+'", could not been found.'
            return

        #The operate system denied to open the file.
        except PermissionError:
            self.error = 'FileReaderError: Access Denied. Your operate system won\'t let me open the file: "'+filename+'".'
            return
    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#





    #================================Get Words================================#
    def getWords(self, amount):

        '''Returns a list with max size "amount", which contains pairs of (word, place).
           The "place" is the distance from the beggining of the file.'''

        #_____Variables_____#
        words   = []
        word    = ""
        counter = 0
        first   = True
        place   = 0
        #_____Variables_____#
        


        #----------Create at least "amount" words----------#
        while counter < amount:

            #Get a single character.
            ch = self.file.read(1)

            #Increase the file index.
            self.fileIndex += 1

            #End of file reached.
            if ch == "":

                #Change the flag.
                self.eof = True

                #Last word into the file.
                if len(word.replace(" ","")) > 0:
                    words.append( (word.replace(" ","").lower(), place) )
                    first = True
                    
                break

            #Word created.
            elif (ch == " " or ch == "\n") and len(word.replace(" ","")) > 0:
                words.append( (word.replace(" ","").lower(), place) )
                word = ""
                counter += 1
                first = True
                pass

            #Create the word.
            elif ch not in self.unwantedSymbols:
                word += ch

                #Set the place of this word inside the file.
                if first:
                    place = self.fileIndex
                    first = False
        #----------Create at least "amount" words----------#


        return words
    #================================Get Words================================#




    #================================Has Next=================================#
    def hasNext(self):
        return not self.eof
    #================================Has Next=================================#




    #==================================Close==================================#
    def close(self):
        self.file.close()
        pass
    #==================================Close==================================#
