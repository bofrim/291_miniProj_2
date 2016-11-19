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
