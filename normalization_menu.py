import sqlite3
import sys
import bcnf
import threenf
import computations


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

def normalize(attributes, fdList):
    while(True):
        choice = raw_input("Do you want 'BCNF' or '3NF': ")
        if choice.upper() == "BCNF":
            return bcnf.convertToBCNF([(set(attributes),fdList)])
        if choice.upper() == "3NF":
            return threenf.convertToThreeNF(attributes, fdList)
        if choice.upper() == "Q":
            return "Q"


def normalizationStory(tables, cursor):
    tableChoice = getTableChoice(tables)
    if tableChoice.upper() == 'Q': return

    # get a list of the functional dependencies
    fdTableName = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('%'+tables[tableChoice]+'%',))
    fdTableName = fdTableName.fetchone()
    fdData = cursor.execute("SELECT * FROM {0};".format(fdTableName[0]))
    fdList = computations.createFDList(fdData)

    # get a list of the attributes
    attribTableName = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('Input_'+tableChoice+'%',))
    attribTableName = attribTableName.fetchone()
    attribData = cursor.execute("SELECT * FROM {0};".format(attribTableName[0]))
    attributes = [description[0] for description in attribData.description]
    print("Original Attributes")
    print(attributes)
    print
    decomposition = normalize(attributes,fdList)
    if decomposition == 'Q': return

    # create new data tables from decomposition
    # computations.createTablesFromDecomposition(schemas);

    while(True):
        choice = raw_input("Normalization Complete...\nWould you like to commit these changes? (y/n): ")
        if choice.upper()  == 'N': return

    # fill the new data tables according to the decomposition, using the data in the input data table
    computations.createNewTables(decomposition)

    return
