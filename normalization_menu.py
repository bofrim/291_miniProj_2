import sqlite3
import sys
from bcnf import *
from threenf import *
from computations import *


def getTableChoice(tables):
    print("\nTables:")
    for table in tables.keys():
        print table
    print("\nEnter Q at anytime to quit")
    choice = " "
    while choice not in table:
        choice = raw_input("From the list above which table would you like to normalize? ")
        if choice == "q" or choice == '\n':
            return 'Q'
    return choice

def getNormalizationType(attributes, fdList):
    while(True):
        choice = raw_input("Do you want 'BCNF' or '3NF': ")
        if choice.upper() == "BCNF":
            return bcnf(fdList)
        if choice.upper() == "3NF":
            return threenf(attributes, fdList)
        if db == "q":
            return db

def normalizationStory(tables, cursor):
    tableChoice = getTableChoice(tables)
    if tableChoice.upper() == 'Q': return

    # get a list of the functional dependencies
    fdTableName = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('%'+tables[tableChoice]+'%',))
    fdTableName = fdTableName.fetchone()
    fdData = cursor.execute("SELECT * FROM {0};".format(fdTableName[0]))
    fdList = createFDList(fdData)

    # get a list of the attributes
    attribTableName = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('Input_'+tableChoice+'%',))
    attribTableName = attribTableName.fetchone()
    attribData = cursor.execute("SELECT * FROM {0};".format(attribTableName[0]))
    attributes = [description[0] for description in attribData.description]
    print("Original Attributes")
    print(attributes)
    print

    getNormalizationType(attributes,fdList)
    return
