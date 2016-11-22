import sqlite3
import sys
from bcnf import *
from threenf import *
from computations import *

def getTableNames():
    print
    print "You will need to provide two sets of dependencies to test equivalence for."
    print "(Use a space to separate the table names)"
    F1_names = raw_input("Please enter the names of tables that make up the first set: ")
    F2_names = raw_input("Please enter the names of tables that make up the second set: ")
    return (F1_names, F2_names)

def getFDUnion(table_names, cursor):
    #TODO Test this method with a database
    listOf_FDs = []
    for fdTableName in table_names.split().strip():
        fdTableName = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('%'+tables[tableChoice]+'%',))
        fdTableName = fdTableName.fetchone()
        fdData = cursor.execute("SELECT * FROM {0};".format(fdTableName[0]))
        fdList = createFDList(fdData)
        list_FDs.append(fdList)
    return listOf_FDs


def equivalenceStory(tables, cursor):
    F1_names, F2_names = getTableNames()

    # get a list of the functional dependencies
    F1 = getFDUnion(F1_names, cursor)
    F2 = getFDUnion(F2_names, cursor)
    #TODO check the equivalence of F1 over F2
    #TODO chenk the equivalence of F2 over F1



def test_get_table_names():
    F1_names, F2_names = getTableNames()
    print F1_names
    print F2_names
