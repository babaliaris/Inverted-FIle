from Source_Files.database import Database

#Create a database object.
database = Database(128)

while True:

    print("\n==============|Main Menu|==============")
    print("Author: Nikolaos Bampaliaris, 2014030006\n")
    print("1) Create Database")
    print("2) Navigate")
    print("3) Exit")
    print("==============|Main Menu|==============\n")

    choose = input("Choose: ")

    if choose == '1':

        print("\n")

        #Get buffer size.
        befferSize = int(input("Give Btree buffer size: "))

        #Buffer size is not acceptable.
        if befferSize < 128:
            print("\nMinimum buffer size is 128.")
            input("Press ENTER to continue...")
            continue

        #Create database object.
        database = Database(befferSize)

        print("\nInsert all the input files inside the")
        print("folder:", '"Files Input"', ', before continue.\n')
        input('Press ENTER to continue...')
        print('\n\n..........Creating database..........')
        database.create()

        #Error creating database.
        if database.error != '':
            print(database.error)
            print('')

        #Created successfully
        else:
            print('\n\nDatabase created successfully.')
            print("You are ready to navigate!\n")

        input('Press ENTER to continue...')

    elif choose == '2':
        print("\n")

        if database.created:
            word = input("Give a word: ")
            database.navigate(word)
            pass

        else:
            print("Database has not been created.")
            input("Press ENTER to continue...")

    elif choose == '3':
        break

    
