from Source_Files.BTree.b_node import BNode

class BTree:

    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-Constructor-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
    def __init__(self, filename, bufferSize):

        #Error messanger.
        self.error = ''

        #Buffer size.
        self.bufferSize = bufferSize

        #Filename.
        self.filename   = filename
            
        #Create the root node.
        root = BNode(filename, bufferSize)

        #Set the root page.
        root.page = 0

        #Create the file.
        self.__openFile__(filename)

        #Write the root at the first page.
        root.write(0)

        self.diskAccesses = 0

        self.totalInserts = 0
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
    def insert(self, new_word, new_page):
        '''Insert a key into the tree.'''

        #Read the root node from the file.
        current = BNode(self.filename, self.bufferSize)
        current.read(0)

        #------------Find A Leaf Node To Insert The Key------------#
        while not current.isLeaf():

            #Go through all keys.
            for i in range( len(current.keys) ):

                #Go left from this key.
                if new_word < current.keys[i].word.replace(' ', ''):
                    current.read( current.children[i] )
                    self.diskAccesses += 1
                    break

                #Go right from this key.
                elif new_word > current.keys[i].word.replace(' ', '') \
                     and i == len(current.keys) - 1:
                    current.read( current.children[i+1] )
                    self.diskAccesses += 1
                    break

                #Do not and the same word twice.
                elif new_word == current.keys[i].word.replace(' ', ''):
                    return current.keys[i]
        #------------Find A Leaf Node To Insert The Key------------#

        #Do not and the same word twice (Last check).     
        for i in range( len(current.keys) ):
            if current.keys[i].word.replace(' ', '') == new_word:
                return current.keys[i]
        
        #Add the key into the current node.
        current.addKey(new_word, new_page)

        self.diskAccesses += current.diskAccesses

        self.totalInserts += 1
        return None
    #===============================Insert================================#





    #===============================Search================================#
    def search(self, new_word):
        '''Searches for a key inside the tree.'''

        #Read the root node from the file.
        current = BNode(self.filename, self.bufferSize)
        current.read(0)

        #------------Find A Leaf Node To Insert The Key------------#
        while True:

            #Go through all keys.
            for i in range( len(current.keys) ):

                #Key found.
                if current.keys[i].word.replace(' ', '') == new_word:
                    return current.keys[i]

                #Go left from this key.
                elif new_word < current.keys[i].word.replace(' ', '') \
                     and not current.isLeaf():
                    current.read( current.children[i] )
                    break

                #Go right from this key.
                elif new_word > current.keys[i].word.replace(' ', '') \
                     and i == len(current.keys) - 1 \
                     and not current.isLeaf():
                    current.read( current.children[i+1] )
                    break

                #Keep going on the keys.
                elif new_word > current.keys[i].word.replace(' ', '') \
                     and i != len(current.keys) - 1:
                    continue

                #Not found.
                else:return None

                
        #------------Find A Leaf Node To Insert The Key------------#
    #===============================Search================================#





    #==============================Preorder===============================#
    def __preorder__(self, node, page):
        '''Just for debugging.'''

        #Return statement.
        if page == -1:
            return

        #Read the page.
        node.read(page)

        #Print information.
        print("===============|Page: "+str(page)+"|===============")
        node.print()
        print("===============|Page: "+str(page)+"|===============\n\n")

        #Go to other children.
        for child in node.children:
            self.__preorder__(node, child)



    def preorder(self):
        '''Just for debugging.'''

        #Start the preorder method.
        self.__preorder__( BNode(self.filename, self.bufferSize), 0 )
    #==============================Preorder===============================#
