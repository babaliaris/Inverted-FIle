import struct, os

#*********************************Key Class*********************************#
class Key:

    #Constructor.
    def __init__(self, new_word, new_page):
        '''Constructor.'''

        #-----------------------Wrong Attributes-----------------------#
        if type(new_word) != str:
            raise AttributeError('Attribute: new_word must be type of str.')

        if type(new_page) != int:
            raise AttributeError('Attribute: new_page must be type of int.')
        #-----------------------Wrong Attributes-----------------------#


        #More than 12 characters was given.
        if len(new_word) > 12:
            raise ValueError("Value of: new_word must be 12 characters max.")


        #If the new_word is less than 12 characters,
        #fill the rest with spaces (Make sure that
        #is going to be exactly 12 bytes).
        else:
            for i in range( len(new_word), 12 ):
                new_word += ' '


        #_____Class Variables_____#
        self.word = new_word
        self.page = new_page
        #_____Class Variables_____#
        pass


    #To Bytes.
    def toBytes(self):
        '''Returns a byte object. This method always returns 16 bytes.'''
        return str.encode(self.word) + struct.pack("i", self.page)
#*********************************Key Class*********************************#





#********************************BNode Class********************************#
class BNode:

    '''
        Lets say, k = keys and k+1 = Order of Btree.
        How many keys can i have? (page+parent = 8).

        k*16 + (k+1)*4 + 8 <= bufferSize
        k*16 + 4*k + 4 + 8 <= bufferSize
        20*k + 12 <= bufferSize
        k <= (bufferSize - 12) / 20
    '''


    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
    def __init__(self, filename, bufferSize):

        #__________Class Variables__________#

        #The file where this node will read or write.
        self.filename     = filename

        #Buffer size of disk page.
        self.bufferSize   = bufferSize
        
        #Calculate maximum keys.
        self.maxKeys = k  = (bufferSize - 12) // 20

        #Calculate useless bytes.
        self.uselessBytes = bufferSize - ( k*16 + (k+1)*4 + 8 )
        

        #-------Variables below will be written into the disk page-------#
        
        #This node's children (Maximum: self.maxKeys + 1).
        self.children = []

        #Keys (Maximum: self.maxKeys).
        self.keys     = []

        #Pointer to this page.
        self.page     = -1

        #Pointer to parent page.
        self.parent   = -1

        #-------Variables above will be written into the disk page-------#

        #__________Class Variables__________#


        self.diskAccesses = 0
    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#





    #=============================Reinitialize============================#
    def __Reinitialize__(self):
        '''I use this to re initialize this node when i'm using the read
           method, because when i store new data to this node everything
           must be clear first.'''

        #-------Variables below will be written into the disk page-------#
        
        #This node's children (Maximum: self.maxKeys + 1).
        self.children = []

        #Keys (Maximum: self.maxKeys).
        self.keys     = []

        #Pointer to this page.
        self.page     = -1

        #Pointer to parent page.
        self.parent   = -1

        #-------Variables above will be written into the disk page-------#
    #=============================Reinitialize============================#






    #==============================Open File==============================#
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
    #==============================Open File==============================#





    #================================Split================================#
    def __split__(self):
        '''Split this node.'''

        #Calculate amount of pages in the file.
        file_pages = os.path.getsize(self.filename) // self.bufferSize

        #Calculate middle key index.
        mid = len(self.keys) // 2

        #Create new child
        new_child = BNode(self.filename, self.bufferSize)

        #Just a flag.
        recurciveSplit = False
        temp_key       = None

        #------------------If This Node Is The Root------------------#
        if self.parent == -1:

            #Create new root.
            new_root  = BNode(self.filename, self.bufferSize)

            #Adjust pages.
            new_root.page  = 0
            self.page      = file_pages
            new_child.page = file_pages+1

            #Adjust parents.
            self.parent      = 0
            new_child.parent = 0

            #Connect children to root.
            new_root.children.append( self.page )
            new_root.children.append( new_child.page )
        #------------------If This Node Is The Root------------------#



        #-----------------------Is Inner Node------------------------#
        else:
            
            #Open the parent node.
            new_root = BNode(self.filename, self.bufferSize)
            new_root.read(self.parent)

            self.diskAccesses += 1
                
            #Adjust child page.
            new_child.page   = file_pages

            #Add a parent to the new child.
            new_child.parent = new_root.page

            #Add the child to the parent.
            new_root.children.append( new_child.page )

            #Keep in a temp variable the middle key.
            if new_root.isFull():
                temp_key = self.keys[mid]
                self.keys.remove( self.keys[mid] )
                recurciveSplit = True
        #-----------------------Is Inner Node------------------------#



        #-----------Place The New Child In The Right Place-----------#
        for i in range( len(new_root.children)-1, 0, -1 ):

            if new_root.children[i] != self.page \
               and new_root.children[i-1] != self.page:

                temp = new_root.children[i]
                new_root.children[i]   = new_root.children[i-1]
                new_root.children[i-1] = temp
                pass

            #Break.
            else:
                break
        #-----------Place The New Child In The Right Place-----------#

            


        #Move middle key to the parent
        #without causing recurcive split.
        if not recurciveSplit:
            new_root.addKey(  self.keys[mid].word, self.keys[mid].page )
            self.keys.remove( self.keys[mid] )

        child = BNode(self.filename, self.bufferSize)

        #Change the parent to this node.
        if len(self.children) > 0:

            for i in range( len(self.children) ):

                if i < len(self.children) // 2 + 1:
                    self.diskAccesses += 2
                    child.read(self.children[i])
                    child.parent = self.page
                    child.write(child.page)



        #Move all the keys and the children after the middle key
        # to the new child.
        while mid != len(self.keys):

            #Move this key to the new child.
            new_child.addKey( self.keys[mid].word, self.keys[mid].page )
            self.keys.remove( self.keys[mid] )

            #Move all the children afrer the middle
            #to the new child.
            if len(self.children) > 0:

                self.diskAccesses += 2

                #Change parent.
                child.read(self.children[mid+1])
                child.parent = new_child.page
                child.write(child.page)

                #Move child.
                new_child.children.append( self.children[mid+1] )
                self.children.remove( self.children[mid+1] )

                #Last child.
                if mid == len(self.keys):

                    self.diskAccesses += 2
                    
                    #Change parent.
                    child.read(self.children[len(self.children)-1])
                    child.parent = new_child.page
                    child.write(child.page)

                    #Move child.
                    new_child.children.append( self.children[len(self.children)-1] )
                    self.children.remove( self.children[len(self.children)-1] )

        #Update the file.
        new_root.write (new_root.page)
        self.write     (self.page)
        new_child.write(new_child.page)

        self.diskAccesses += 1

        #Split the root node recurcivly.
        if recurciveSplit:
            self.diskAccesses += 1
            new_root.addKey(temp_key.word, temp_key.page)
    #================================Split================================#
    




    #===============================Add Key===============================#
    def addKey(self, new_word, new_page):
        '''Add a new key into this node and split it if necessary.'''


        #Add a new key into this node.
        self.keys.append( Key(new_word, new_page) )

        #Sort the keys.
        self.sort()

        #Split this node.
        if len(self.keys) == self.maxKeys:
            self.__split__()

        #Update the file.
        else:
            self.diskAccesses += 1
            self.write(self.page)
    #===============================Add Key===============================#





    #================================Sort================== ===============#
    def sort(self):
        '''Use bubble sort, to sort the keys of this node.'''

        for i in range( 0, len(self.keys) - 1 ):
            for j in range( i+1, len(self.keys) ):

                #Must swap.
                if self.keys[i].word > self.keys[j].word:

                    #Keep i values.
                    temp_word = self.keys[i].word
                    temp_page = self.keys[i].page

                    #Copy j to i.
                    self.keys[i].word = self.keys[j].word
                    self.keys[i].page = self.keys[j].page

                    #Copy i to j.
                    self.keys[j].word = temp_word
                    self.keys[j].page = temp_page
                    pass
    #================================Sort=================================#





    #===============================Write=================================#
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

        #Fill the rest with something.
        for i in range( len(self.keys), self.maxKeys ):
            buffer += str.encode('zzzzzzzzzzzz') + struct.pack('i', -1)

        #-------------------------Keys-------------------------#



        #-----------------------Children-----------------------#
            
        #Add children into the buffer.
        for child in self.children:
            buffer += struct.pack("i", child)

        #Fill the rest with -1.
        for i in range( len(self.children),  self.maxKeys + 1):
            buffer += struct.pack("i", -1)

        #-----------------------Children-----------------------#


        #Add the page.
        buffer += struct.pack("i", self.page)

        #Add the parent.
        buffer += struct.pack("i", self.parent)

        #Fill useless bytes with the null character.
        for i in range(0, self.uselessBytes):
            buffer += str.encode('\0')


        #Write the buffer and return amount of written bytes.
        file.write(buffer)

        #Close the file.
        file.close()

        return 128
    #===============================Write=================================#





    #===============================Read==================================#
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
        for i in range(0, self.maxKeys * 16, 16):

            word = bytes.decode( buffer[i:i+12] )
            page = struct.unpack( 'i', buffer[i+12:i+16] )[0]

            #Append the key into the keys if its not garbage.
            if word != 'zzzzzzzzzzzz' and page != -1:
                self.keys.append( Key(word, page) )
        #-------------------------Keys-------------------------#


        #Where did i finished in keys.
        finished = self.maxKeys * 16


        #-----------------------Children-----------------------#
        for i in range(finished, finished + (self.maxKeys+1)*4, 4):

            child = struct.unpack( 'i', buffer[i:i+4] )[0]

            #Append the child into the children if its not garbage.
            if child != -1:
                self.children.append(child)
        #-----------------------Children-----------------------#

        #Where did i finished in children.
        finished = self.maxKeys * 16 + (self.maxKeys+1)*4

        #Read the page.
        self.page = struct.unpack( 'i', buffer[finished : finished+4] ) [0]

        #Read the parent.
        self.parent = struct.unpack( 'i', buffer[finished + 4 : finished+8] )[0]

        #Close the file.
        file.close()
        
        #Return how many bytes i read.
        return len(buffer)
    #===============================Read==================================#





    #=============================Is Leaf=================================#
    def isLeaf(self):
        '''Return's True if this BNode is a leaf.'''
        return len(self.children) == 0
    #=============================Is Leaf=================================#





    #=============================Is Full=================================#
    def isFull(self):
        '''Return's True if this BNode is full of children.'''
        return len(self.children) == self.maxKeys + 1
    #=============================Is Full=================================#





    #==============================Print==================================#
    def print(self):
        '''This is just for debbuging.'''

        print("Buffer Size\t:",self.bufferSize)
        print("Max Keys\t:",self.maxKeys)
        print("Max Children\t:",self.maxKeys+1)
        print("Useless Bytes\t:",self.uselessBytes)
        print("Current Page\t:",self.page)
        print("Parent Page\t:",self.parent,'\n')

        print("Printing Keys...")
        for i in range( len(self.keys) ):
            print('word['+str(i)+'] =',self.keys[i].word,
                  ', page['+str(i)+'] =',self.keys[i].page)


        print("\nPrinting Children...")
        for i in range( len(self.children) ):
            print("Child["+str(i)+"] =",self.children[i])
    #==============================Print==================================#

                
#********************************BNode Class********************************#  
