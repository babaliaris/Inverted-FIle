from Source_Files.Euretirio.euretirio_node import EuretirioNode

import os


class Euretirio:

    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
    def __init__(self):

        #Error messanger.
        self.error = ''

        #Filename.
        self.filename = 'euretirio.dat'

        #Buffer Size.
        self.bufferSize = 128

        #Create the file.
        self.__openFile__(self.filename)
    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#





    #==============================Open File==============================#
    def __openFile__(self, filename):
        '''Open a file by handling exceptions.'''

        #Try to open the file.
        try:
            file = open(filename, 'wb')
            return file


        #File Not Found Error.
        except FileNotFoundError:
            self.error = 'BTree Error: The file:"'+filename+'", could not'+\
                         ' been found.'
            return None


        #Permission Error.
        except PermissionError:
            self.error = 'BTree Error: Your operate system denied'+\
                         ' permission for file handling.'
            return None
    #==============================Open File==============================#





    #===============================Insert================================#
    def insert(self, filename, number, page):

        #Calculate the disk pages.
        pages = os.path.getsize(self.filename) // self.bufferSize

        #Create a new page.
        if page >= pages:

            #Create a new node.
            new_node = EuretirioNode()

            #Update the page of this node.
            new_node.page = page

            #Add the key into this node.
            new_node.addKey(filename, number)
            pass


        #Update a page.
        else:
            
            #Open the node from the file.
            node = EuretirioNode()
            node.read(page)

            #Add the key to this node.
            node.addKey(filename, number)      
    #===============================Insert================================#





    #==============================Get Page===============================#
    def getPage(self, page):

        #Create a new node.
        new_node = EuretirioNode()

        #Read.
        new_node.read(page)

        return new_node
    #==============================Get Page===============================#
