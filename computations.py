import sqlite3
import copy
import sys
from ColumnTypes import ColumnTypes

def closure(X, FDs):
    # Take a set of attributes, X, and an array of tuples of sets, FDs, representing all of the functional dependencies for the table: conpute the closure of X
    temp_FDs = copyFDs(FDs)
    closure = X
    old = {}
    while(old != closure):
        old = closure.copy()
        for FD in temp_FDs:
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

    return: list of lists of tuples of sets
            list of Funtional Dependencies
    i.e. [ [ ({U1 LHS1},{U1 RHS1}),({U1 LHS2},{U1 RHS2}) ],  [({U2 LHS},{U2 RHS})], ... ,[({Un LHS},{Un RHS})] ]
    '''
    partitions = []
    had = []
    for relation in minCover:
        LHS = relation[0]
        if LHS not in had:
            partitions.append([relation])
            had.append(LHS)
            continue
        for l in partitions:
            if (l[0][0] is LHS):
                l.append(relation)
                break
        had.append(LHS)
    return partitions

def createSchemas(partitions):
    '''
    Creates a schema for each list of dependencies with equal LHS's

    param:  list of functional dependencies

    return: list of schemas (tuples of attributes and functional dependencies)
    '''
    schemas = []
    for fdList in partitions:
        attributes = set()
        attributes |= fdList[0][0]
        # add the rest of the attributes
        for dep in fdList:
            attributes |= dep[1]
        schemas.append((attributes,fdList))
    return schemas

def getKeyFromFDs(attributes,fds):
    #get a set of all attributes
    superKey = copy.deepcopy(attributes)
    localfds = copy.deepcopy(fds)

    #check for all fds if the LHS is in the key and an element of the RHS is also in the key
    #remove the RHS from the key
    for fd in localfds:
        if fd[0].issubset(superKey):
            RHSClosure = closure(fd[1],localfds)
            RHSClosureMinusLHS = RHSClosure - fd[0]
            superKey -= RHSClosureMinusLHS
    return superKey

def copyFDs(FDs):
    new_FDs = list()
    for FD in FDs:
        new_FDs.append(tuple((FD[0], FD[1])))
    return new_FDs

# is dependancy preserving if the closure of the decomposed functional dependacies is the
# same as the closure of the original functional dependancies
def isDependancyPreserving(original, decomposition):
    originalCpy = copy.deepcopy(original)
    origninalFDClosure = []
    for schema in originalCpy:
        for FD in schema[1]:
            origninalFDClosure.append((FD[0],closure(copy.deepcopy(FD[0]),copy.deepcopy(schema[1]))))
    # get a union of all functional dependancies in the decomposition
    decomopsitionFDs = []
    for schema in decomposition:
        for FD in schema[1]:
            decomopsitionFDs.append(FD)
    # now get the closure of the union
    decompositionFDClosure = []
    for FD in decomopsitionFDs:
        decompositionFDClosure.append((FD[0],closure(copy.deepcopy(FD[0]),copy.deepcopy(decomopsitionFDs))))
    #now do a comparison
    #check that all the original fds are in the decomposition
    # this works because all fds in the decomposition must be in the original
    for FD in origninalFDClosure:
        if not FD in decompositionFDClosure:
            return False
    return True


def makeSelect(attrList):
    return ",".join(attrList)

def makePrimaryKeyStr(primaryKeySet):
    return ",".join([keyAttr for keyAttr in primaryKeySet])


def createNewFilledTables(connection, decomposition, originalTableNameAbreviation):
    c = connection.cursor()
    print()
    for tableInfo in decomposition:
        attributes = tableInfo[0]
        print attributes
        attributeStr = "".join(attributes)
        oldTableName = "Input_" + originalTableNameAbreviation
        newTableName = "Output_" + originalTableNameAbreviation + "_" + attributeStr
        superKey = getKeyFromFDs(tableInfo[0],tableInfo[1])
        print "superKey"
        print superKey
        createAndFillTable(attributes, newTableName, oldTableName, superKey, c)
        createFilledFDTable(attributes, tableInfo[1], oldTableName, c)

def fillTable(attributes, newTableName, oldTableName, cursor):
    selectParameterStr = makeSelect(attributes)
    insertStr = "INSERT INTO " + newTableName + " SELECT DISTINCT " + selectParameterStr + " FROM " + oldTableName + ";"
    print("input string")
    print insertStr
    cursor.execute(insertStr)

def createAndFillTable(attributes, newTableName, oldTableName, superKey, cursor):
    createTableStr = "CREATE TABLE "+ newTableName +"("
    for attribute in attributes:
        createTableStr += attribute +" "+ ColumnTypes.getType(attribute) + ", "
    createTableStr += " PRIMARY KEY (" + makePrimaryKeyStr(superKey) + "));"
    print createTableStr
    cursor.execute(createTableStr)
    fillTable(attributes, newTableName, oldTableName, cursor)

def createFilledFDTable(attributes, FDset, oldTableName, cursor):
    originalTableNameAbreviation = oldTableName[6:]
    attributeStr = "".join(attributes)
    newTableName = "Output_FDS_" + originalTableNameAbreviation + "_"+attributeStr
    createTableStr = "CREATE TABLE "+ newTableName +" ( LHS TEXT, RHS TEXT );"
    cursor.execute(createTableStr)
    # print "************************FDS****************************"
    # print FDset
    for FD in FDset:
        # print FD[0]
        # print FD[1]
        # print makeSelect(FD[0])
        # print makeSelect(FD[1])
        insertStr = "INSERT INTO " + newTableName + " (LHS, RHS) VALUES ('" + makeSelect(FD[0]) + "','" + makeSelect(FD[1]) + "');"
        print insertStr
        cursor.execute(insertStr)
    
