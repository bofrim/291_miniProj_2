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

def createFDUnions(fdTableNames,cursor):
    '''
    Takes a list of FD table names and computes the union of their functional dependencies
    '''
    for name in fdTableNames:
        if 'FDS' not in name:
            fdTableNames.remove(name)
    fdDataUnion = []
    for tableName in fdTableNames:
        fds = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE NAME LIKE ?;", ('%'+tableName+'%',))
        fds = fds.fetchone()
        if fds:
            fds = cursor.execute("SELECT * FROM {0};".format(fds[0]))
            fds = computations.createFDList(fds)
            fdDataUnion = unionFDLists(fdDataUnion, fds)
    return fdDataUnion

def printUnion(union):
    print 'Union of FD Tables: '
    for u in union:
        print [a for a in u[0]],'|',[a for a in u[1]]
    print

def computeClosures(attributes,FDs):
    '''
    Computes closure of the individual attributes in a list over the specified FDs
    '''
    for a in attributes:
        print "Closure of",a,"..."
        print [x for x in computations.closure(set(a),FDs)], "\n"

def closureStory(cursor):
    '''
    - Asks user for set of Attributes and FD Table Names
    - Computes the union of the FD Tables
    - Computes the closure of each Attribute over the union of the
      specified FD Tables
    - Prints closures
    '''
    print
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
            fdDataUnion = createFDUnions(fdTableNames, cursor)
            printUnion(fdDataUnion)
            computeClosures(attributes,fdDataUnion)
            print("\nEnter Q at anytime to quit")
    return

# if __name__ == '__main__':
#     pass
