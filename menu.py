import sqlite3
import sys
from bcnf import *
from threenf import *

def getDataBaseConnection():
    db = raw_input("Enter the name of your data base: ")
    if db == "q":
        sys.exit(0)
    return sqlite3.connect('MiniProject2-InputExample.db')

def getTableChoice(tables):
    print "***********************************"
    for table in tables.keys():
        print table
    choice = raw_input("From the list above which table would you like to normalize? ")
    while choice not in table:
        if choice == "q":
            sys.exit(0)
        choice = raw_input("From the list above which table would you like to normalize? ")
    return choice

def getNormalizationType(fdList):
    while(True):
        choice = raw_input("Do you want 'BCNF' or '3NF': ")
        if choice.upper() == "BCNF":
            return bcnf(fdList)
        if choice.upper() == "3NF":
            return threenf(fdList)
        if db == "q":
            sys.exit(0)
