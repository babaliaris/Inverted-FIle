import struct, os


#*********************************Key Class*********************************#
class Key:

    #Constructor.
    def __init__(self, filename, number):
        '''Constructor.'''

        #-----------------------Wrong Attributes-----------------------#
        if type(filename) != str:
            raise AttributeError('Attribute: filename must be type of str.')

        if type(number) != int:
            raise AttributeError('Attribute: number must be type of int.')
        #-----------------------Wrong Attributes-----------------------#


        #More than 8 characters was given.
        if len(filename) > 8:
            raise ValueError("Value of: filename must be 8 characters max.")


        #If the filename is less than 8 characters,
        #fill the rest with spaces (Make sure that
        #is going to be exactly 8 bytes).
        else:
            for i in range( len(filename), 8 ):
                filename += ' '


        #_____Class Variables_____#
        self.filename = filename
        self.number   = number
        #_____Class Variables_____#
        pass


    #To Bytes.
    def toBytes(self):
        '''Returns a byte object. This method always return's 16 bytes.'''
        return str.encode(self.filename) + struct.pack("i", self.number)
#*********************************Key Class*********************************#




#******************************Euretirio Class******************************#
class EuretirioNode:

    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
    def __init__(self):

        #Filename.
        self.filename = 'euretirio.dat'

        #Buffer Size.
        self.bufferSize = 128

        #-------Variables below will be written into the disk page-------#
        
        #Keys (Maximum is 10).
        self.keys = []

        #Next page.
        self.next_page = -1

        #Current page.
        self.page = -1

        #-------Variables above will be written into the disk page-------#

        
    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#





    #===============================Reinitialize==============================#
    def __Reinitialize__(self):
        '''I use this to re initialize this node when i'm using the read
           method, because when i store new data to this node everything
           must be clear first.'''

        #-------Variables below will be written into the disk page-------#

        #Keys (Maximum is 10).
        self.keys     = []

        #Next page.
        self.next_page = -1

        #Current page.
        self.page = -1

        #-------Variables above will be written into the disk page-------#
    #===============================Reinitialize==============================#





    #================================Open File================================#
    def __openFile__(self, filename, mode):
        '''Open's a file by handling exceptions.'''

        #Try to open the file.
        try:
            file = open(filename, mode)
            return file


        #File Not Found Error.
        except FileNotFoundError:
            raise Exception('BTree Error: The file:"'+filename+'", could not'+\
                         ' been found.')
            return None


        #Permission Error.
        except PermissionError:
            raise Exception('BTree Error: Your operate system denied'+\
                         ' permission for file handling.')
            return None
    #================================Open File================================#




    #=================================Add Next================================#
    def __addNext__(self, filename, number):

        #Create a new node.
        new_node = EuretirioNode()

        #Next page do not exists.
        if self.next_page == -1:

            #Calculate the disk pages.
            pages = os.path.getsize(self.filename) // self.bufferSize

            #Update the page of the new node.
            new_node.page = pages

            #Set the next page of this node.
            self.next_page = new_node.page

            #Update this node.
            self.write(self.page)

            #Add the key to the new node.
            new_node.addKey(filename, number)
            pass


        #Next page exists.
        else:

            #Open the next page.
            new_node.read(self.next_page)

            #Add the key to the new node.
            new_node.addKey(filename, number)
    #=================================Add Next================================#





    #=================================Add Key=================================#
    def addKey(self, filename, number):

        #Keys are not full.
        if len(self.keys) < 10:
            self.keys.append( Key(filename, number) )
            self.write(self.page)
            pass

        #This node is full, so create a new one
        #and connect it with it.
        else:
            self.__addNext__(filename, number)
    #=================================Add Key=================================#





    #===================================Write=================================#
    def write(self, page):

        '''Write this node into the file. This method will write exactly
           bufferSize bytes.'''

        #Negative page.
        if page < 0:
            raise ValueError("Value of: page, must be greater or equal to 0.")

        #Open the file.
        file = self.__openFile__(self.filename, 'rb+')

        #Seek into the file.
        file.seek(self.bufferSize * page)

        #Create an empty byte object.
        buffer = bytes()

        #-------------------------Keys-------------------------#
        
        #Add all the keys into the buffer.
        for key in self.keys:
            buffer += key.toBytes()
            pass

        #Fill the rest with something.
        for i in range( len(self.keys), 10 ):
            buffer += str.encode("zzzzzzzz") + struct.pack('i', -1)
            pass

        #-------------------------Keys-------------------------#

        #Add the page.        
        buffer += struct.pack('i', self.page)

        #Add the next page.
        buffer += struct.pack('i', self.next_page)

        #Write the buffer into the file.
        file.write(buffer)

        #Close the file.
        file.close()

        return len(buffer)
    #===================================Write=================================#





    #=================================Read====================================#
    def read(self, page):
        '''Read a BNode from the file.'''

        #Negative page.
        if page < 0:
            raise ValueError("Value of: page, must be greater or equal to 0.")

        #Reinitialize this node.
        self.__Reinitialize__()

        #Open file.
        file = self.__openFile__(self.filename, 'rb')

        #Seek into the file.
        file.seek(self.bufferSize * page)

        #Read the page.
        buffer = file.read(self.bufferSize)

        #-------------------------Keys-------------------------#
        for i in range( 0, 120, 12 ):

            filename = bytes.decode( buffer[i:i+8] )
            number   = struct.unpack('i', buffer[i+8:i+12] )[0]

            #Append the key into the keys if its not garbage.
            if filename != 'zzzzzzzz' and number != -1:
                self.keys.append( Key(filename, number) )
        #-------------------------Keys-------------------------#

        #Get the page.
        self.page = struct.unpack('i', buffer[120:124] )[0]

        #Get the next page.
        self.next_page = struct.unpack('i', buffer[124:128] )[0]

        #Close the file.
        file.close()

        return len(buffer)
    #=================================Read====================================#





    #=================================Print===================================#
    def print(self):
        '''This is just for debbuging.'''

        print("Page\t\t:", self.page)
        print("Next Page\t:", self.next_page,'\n')
        
        print("Printing Keys...")
        for i in range( len(self.keys) ):
            print('filename['+str(i)+'] =',self.keys[i].filename,
                  ', place['+str(i)+'] =',self.keys[i].number)
    #=================================Print===================================#

        

        
#******************************Euretirio Class******************************#

