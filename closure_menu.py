import sqlite3
import sys
from bcnf import *
from threenf import *
import computations


def getFDTables():
    while(True):
        fdTableNames = raw_input("Please specify the FD tables you would like to use (seperated by commas): ")
        if fdTableNames.upper() == 'Q': return fdTableNames
        return fdTableNames

def unionFDLists(fd1, fd2):
    '''
    Computes the union of two lists of tuples of sets (FDs)
    '''
    return [x for x in fd1 if x not in fd2]+[x for x in fd2]

def computeClosures(attributes,FDs):
    '''
    Computes closure of the individual attributes in a list over the specified FDs
    '''
    for a in attributes:
        print "Closure of",a,"..."
        print [x for x in computations.closure(set(a),FDs)], "\n"

def closureStory(tables, cursor):
    print("Enter Q at anytime to quit")
    while(True):
        attributes = raw_input("Please specify the set Attributes (seperated by commas): ")
        if attributes.upper() == 'Q': return
        else:
            attributes = set(attributes.split(','))
            fdTableNames = getFDTables()
            if fdTableNames.upper() == 'Q': return
            fdTableNames = fdTableNames.split(',')
            print

            fdDataUnion = []
            for tableName in fdTableNames:
                fds = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('%'+tableName+'%',))
                fds = fds.fetchone()
                fds = cursor.execute("SELECT * FROM {0};".format(fds[0]))
                fds = computations.createFDList(fds)
                fdDataUnion = unionFDLists(fdDataUnion, fds)

            computeClosures(attributes,fdDataUnion)
            print("\nEnter Q at anytime to quit")
    return
