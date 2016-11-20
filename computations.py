import sqlite3
import sys

def closure(X, FDs):
    # Take a set of attributes, X, and an array of tuples of sets, FDs, representing all of the functional dependencies for the table: conpute the closure of X
    closure = X
    old = {}
    while(old != closure):
        old = closure.copy()
        for FD in FDs:
            if FD[0].issubset(closure):
                closure |= FD[1]
    return closure


def createFDList(fdData):
    fdList = []
    for relation in fdData:
        LHS = relation[0]
        ls = set(str(LHS).split(','))
        RHS = relation[1]
        rs = set(str(RHS).split(','))
        fdList.append((ls,rs))
    return fdList

def getKeyFromFDs(fds):
    #get a set of all attributes
    superKey = set()
    for fd in fds:
        superKey |= fd[0] | fd[1]

    #check for all fds if the LHS is in the key and an element of the RHS is also in the key
    #remove the RHS from the key
    for fd in fds:
        if fd[0].issubset(superKey):
            RHSClosure = closure(fd[1],fds)
            RHSClosureMinusLHS = RHSClosure - fd[0]
            superKey -= RHSClosureMinusLHS
    return superKey
