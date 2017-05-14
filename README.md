# Inverted-File

### What it is?
This project is a program which take's text files as input and create's a data base. Then you can ask the database for a specific word and it will answer you the names of the files where this word exists and in which position this word is inside the file.

### Requirements?
You will need only python (it might run in python 2.7 but i'm not sure, haven't test it). Better use the latest version of python (tested in python 3.6)

### How to use?
There is a directory with the name "Files Input". Inside there go and put all the text files you want to use. The database will read all the files inside the "Files Input" directory in order to create the database. PLEASE do not put anything else inside this directory ( binary files like microsoft office word files, video files etc) because the program will crash, use only basic txt files!!!

**Also make sure that the maximum characters of the filenames (without counting the .txt extension) is 8 and not more!!!
Even if you forget to do this the program will not crash, but it will tell you to rename the filenames.**

After including the text files, just run main.py and follow the user interface guide.
