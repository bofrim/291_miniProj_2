import sqlite3
import sys
from bcnf import *
from threenf import *

def getDataBaseConnection():
    db = raw_input("Enter the name of your data base: ")
    if db == "q":
        sys.exit(0)
    return sqlite3.connect('MiniProject2-InputExample.db')

def closureStory():
    print('Enter q at any point to return to menu...')
    attributes = raw_input("Enter Attributes Contained in the Set: ")
    if (attributes == "q"):
        return
    fdTables = raw_input("From the list above, choose which FD Tables to use: ")
