import sqlite3
import sys
from bcnf import *
from threenf import *
from computations import *
import copy

def getTableNames():
    print
    raw_input("Make it so you can enter output tables ******************")
    print "You will need to provide two sets of dependencies to test equivalence for."
    print "(Use a comma to separate the table names)"
    F1_names = raw_input("Please enter the names of tables that make up the first set: ")
    if str(F1_names.upper()) == "Q": return (-1,-1)

    F2_names = raw_input("Please enter the names of tables that make up the second set: ")
    if F2_names.upper == "Q": return (-1, -1)
    F1_names = [x.strip() for x in F1_names.split(',')]
    F2_names = [x.strip() for x in F2_names.split(',')]
    return (F1_names, F2_names)

def unionFDLists(fd1, fd2):
    return [x for x in fd1 if x not in fd2]+[x for x in fd2]

def getFDUnion(fdTableNames, cursor, tables):
    #TODO Test this method with a database
    fdDataUnion = []
    for tableName in fdTableNames:
        fds = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('%'+tableName+'%',))
        fds = fds.fetchone()
        fds = cursor.execute("SELECT * FROM {0};".format(fds[0]))
        fds = computations.createFDList(fds)
        fdDataUnion = unionFDLists(fdDataUnion, fds)
    return fdDataUnion

def checkEquivalence(F1, F2):
    for fd in F1:
        if not fd[1].issubset(closure(copy.deepcopy(fd[0]), copy.deepcopy(F2))):
            # print "______________________________________"
            # print "The violating closure was: element(" + str(fd[0]) + ", " + str(fd[1]) + ") on closure: " + str(closure(copy.deepcopy(fd[0]), copy.deepcopy(F2)))
            # raw_input("______________________________________")
            return False
    return True

def equivalenceStory(tables, cursor):
    F1_names, F2_names = getTableNames()
    if F1_names == -1 or F2_names == -1:
        print "Returning to main menu..."
        print
        return

    # get a list of the functional dependencies
    F1 = getFDUnion(F1_names, cursor, tables)
    F2 = getFDUnion(F2_names, cursor, tables)
    # raw_input("DBug: ____"+str(F1)+"____")
    # raw_input("DBug: ____"+str(F1)+"____")
    if checkEquivalence(F1, F2) and checkEquivalence(F2, F1):
        print
        print "The sets of functional dependancies are equivalent!"
        return
    print
    print "The sets of functional dependancies are not equivalent :("



def test_get_table_names():
    F1_names, F2_names = getTableNames()
    print F1_names
    print F2_names
