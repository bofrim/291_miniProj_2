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

def partitionMinCover(minCover):
    '''
    Partition the Minimal Cover into sets such that the LHS of each attribute
    in the set are the same

    param: list of tuples of sets
    i.e. minCover = [({},{}),({},{}), ... ,({},{})]

    return: set of lists of tuples of sets
    i.e. { [ ({U1 LHS1},{U1 RHS1}),({U1 LHS2},{U1 RHS2}) ],  [({U2 LHS},{U2 RHS})], ... ,[({Un LHS},{Un RHS})]}
    '''
    ret = []
    had = []
    for relation in minCover:
        LHS = relation[0]
        if LHS not in had:
            ret.append([relation])
            had.append(LHS)
            continue
        for l in ret:
            if (l[0][0] is LHS):
                l.append(relation)
                break;
        had.append(LHS)
    return ret
