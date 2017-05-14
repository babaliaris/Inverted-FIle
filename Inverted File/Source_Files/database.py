from Source_Files.file_reader         import FileReader
from Source_Files.BTree.b_tree        import BTree
from Source_Files.Euretirio.euretirio import Euretirio

import os




class Database:

    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
    def __init__(self, bufferSize):

        #Error messanger.
        self.error = ''

        #BTree.
        self.tree = BTree('dictionary.dat', bufferSize)

        #Euretirio.
        self.euretirio = Euretirio()

        #Change's to True when the database
        #has been created.
        self.created = False

        #Just a flag.
        self.keepGoingOnError = True
    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#






    #==================================Create=================================#
    def create(self):

        #Get a list with all the filenames
        #inside the Files Input directory.
        filenames = os.listdir('Files Input')

        if len(filenames) == 0:
            self.error = 'No input files.'
            return

        #Go through all the files.
        for filename in filenames:

            #Keep the name.
            name    = filename.replace('.txt', '')

            #Create full file path.
            filename = os.path.join('Files Input', filename)

            #Create a file reader.
            reader = FileReader(filename)

            #An error occured.
            if reader.error != '':
                self.error = reader.error
                return


            #-----Get all the words from the current file-----#
            while reader.hasNext():

                #Get the next 10 words.
                words = reader.getWords(10)

                #Go though all the words.
                for word in words:

                    #Calculate the amount of euretirio pages.
                    pages = os.path.getsize(self.euretirio.filename) // 128

                    #Try to insert the new word into the tree.
                    try:
                        key = self.tree.insert(word[0], pages)
                        pass

                    #Word is more than 12 characters.
                    except ValueError:

                        #Show info to the user.
                        if self.keepGoingOnError:
                            print("One or more words are more than 12")
                            print("characters. Please note that these")
                            print("words will not be stored in the"\
                                  +" database.\n")
                            input("Press ENTER to continue...")
                            self.keepGoingOnError = False

                    #Word already in the tree.
                    if key != None:

                        try:
                            self.euretirio.insert(name, word[1], key.page)
                            pass

                        except ValueError:
                            self.error = \
                                       ("One or more filenames have more than"\
                                  +"\n8 characters. Please rename the files"\
                                  +"and run the program egain.")
                            return

                    #Create a new page for this word.
                    else:

                        try:
                            self.euretirio.insert(name, word[1], pages)
                            pass

                        except ValueError:
                            self.error = \
                                       ("One or more filenames have more than"\
                                  +" \n8 characters. Please rename the files"\
                                  +" and run the program again.")
                            return
            #-----Get all the words from the current file-----#


            #Close the reader.
            reader.close()

            #Created.
            self.created = True
    #==================================Create=================================#





    #=================================Navigate================================#
    def navigate(self, word):

        word = word.replace(" ", "").lower()
        key  = self.tree.search(word)

        #Word did not found.
        if key == None:
            print('The word: "'+word+'", could not been found in the database.')
            return

        #Get the page form the euretirio.
        node = self.euretirio.getPage(key.page)

        while True:
            print('\n==========|Euretirio Page:',str(key.page)+"|==========")
            node.print()
            print('\n==========|Euretirio Page:',str(key.page)+"|==========\n")

            #If there is a next page.
            if node.next_page != -1:

                while True:
                    print('\n')
                    print("1) Next page")
                    print("2) Main Menu\n")

                    choose = input("Choose: ")

                    if choose == "1":
                        node.read(node.next_page)
                        break

                    elif choose == "2":
                        return

            else:
                input('Press ENTER to continue...')
                return
    #=================================Navigate================================#






    def getTreeCreationAverage(self):

        return self.tree.diskAccesses // self.tree.totalInserts
                
