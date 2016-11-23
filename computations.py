import sqlite3
import copy
import sys
import main

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
    print "decomposition"
    print decomposition

    originalCpy = copy.deepcopy(original)
    origninalFDClosure = []
    for schema in originalCpy:
        for FD in schema[1]:
            origninalFDClosure.append((FD[0],closure(copy.deepcopy(FD[0]),copy.deepcopy(schema[1]))))

    # print "Original FD closure"
    # print origninalFDClosure

    # get a union of all functional dependancies in the decomposition
    decomopsitionFDs = []
    for schema in decomposition:
        for FD in schema[1]:
            decomopsitionFDs.append(FD)

    # print "Unioned FDs"
    # print decomopsitionFDs

    # now get the closure of the union
    decompositionFDClosure = []
    for FD in decomopsitionFDs:
        decompositionFDClosure.append((FD[0],closure(copy.deepcopy(FD[0]),copy.deepcopy(decomopsitionFDs))))

    # print "Unioned FDs closure"
    # print decompositionFDClosure

    #now do a comparison
    #check that all the original fds are in the decomposition
    # this works because all fds in the decomposition must be in the original
    for FD in origninalFDClosure:
        if not FD in decompositionFDClosure:
            return False
    return True

def createTablesFromDecomposition(decomposition):s

    db_file_path="./MiniProject2-InputExample.db"
    conn = sqlite3.connect(db_file_path)

    c = conn.cursor()

    for schema in decomposition:
        #create a table for each schema
        involvedAttributeString = ""
        for attr in schema[0]:
            involvedAttributeString += attr
        tableName = "Output_R1_" + involvedAttributeString
        # print "name of new table: " + tableName
        # Create table
        columnNames = ""

        #generate the create column stirng
        attrCount = 0
        for attr in schema[0]:
            columnNames += " " + attr + ""
            columnNames += " "
            columnNames += main.AttrTypes[attr] # TO DO: actually get the types
            if (attrCount < len(schema[0]) - 1):
                columnNames += ","
            attrCount += 1

        #gernerate the create primary key string
        attrCount = 0
        primaryKeySet = getKeyFromFDs(schema[0],schema[1])
        # primaryKeyStr = ",".join(primaryKeySet)
        primaryKeyStr = ""
        for keyAttr in primaryKeySet:
            primaryKeyStr += "`" + keyAttr + "`"
            if (attrCount < len(primaryKeySet) - 1):
                primaryKeyStr += ","
            attrCount += 1


        dropTableStr = " DROP TABLE IF EXISTS " + tableName + ";"
        createTableStr = ' CREATE TABLE ' + tableName + ' (' + columnNames + ', ' + 'PRIMARY KEY (' + primaryKeyStr + ')' + '); '
        c.execute(dropTableStr)
        c.execute(createTableStr)

        # now make a fd table
        fdTableName = "Output_FDS_R1_" + involvedAttributeString
        createFDTableStr = ' CREATE TABLE ' + fdTableName + ' ( `LHS` TEXT, `RHS` TEXT ); '
        dropFDTableStr = " DROP TABLE IF EXISTS " + fdTableName + ";"
        c.execute(dropFDTableStr)
        c.execute(createFDTableStr)

        # add funtional dependancies
        for fd in schema[1]:
            LHS = ",".join(fd[0])
            RHS = ",".join(fd[1])

            # print LHS + " | " + RHS
            insertStatement = 'INSERT INTO ' + fdTableName + ' VALUES ("'+ LHS +'", "'+ RHS +'")'
            # print insertStatement
            c.execute( insertStatement)
        conn.commit()

def makeSelect(attrList):
    return ", ".join(attrList)

def makePrimaryKeyStr(primaryKeySet):
    return ", ".join(["`"+keyAttr+"`" for keyAttr in primaryKeySet])


def createNewFilledTables(decomposition, originalTableNameAbreviation, originalDataBaseName):
    raw_input("Get rid of hardcoded DB name")
    raw_input("TODO: Ensure the naming convention for the database here is consistant with the original input.\n (include .db?")
    db_file_path="./" + "MiniProject2-InputExample" + ".db"
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    for tableInfo in decomposition:
        attributes = decomposition[0]
        attributeStr = "".join(attributes)
        oldTableName = "Input_" + originalTableNameAbreviation + "_" + attributeStr
        newTableName = "Output_" + originalTableNameAbreviation + "_" + attributeStr
        superKey = getKeyFromFDs(schema[0],schema[1])
        createNewEmptyTables(attributes, newTableName, oldTableName, superKey, c)
        createFilledFDTable()

def fillTable(attributes, newTableName, oldTableName, cursor):
    selectParameterStr = makeSelect(attributes)
    insertStr = "INSERT INTO " + newTableName + " (SELECT " + selectParameterStr + " FROM " + oldTableName + ");"
    cursor.execute(insertStr)

def createNewEmptyTables(attributes, newTableName, oldTableName, superKey, cursor):
    dropStr = " DROP TABLE IF EXISTS " + newTableName + ";"
    cursor.execute(dropStr)
    createTableStr = "CREATE TABLE "+ newTableName +"("
    for attribute in attributes:
        createTableStr += attribute +" "+ typeOfAttribute(attribute) +", "
    createTableStr += " PRIMARY KEY (" + makePrimaryKeyStr(superKey) + "));"
    cursor.execute(createTableStr)
    fillTable(attributes, newTableName, oldTableName, superKey, cursor)

def createFilledFDTable(attributes, FDset, oldTableName, cursor):
    originalTableNameAbreviation = oldTabelName[6:]
    attributeStr = "".join(attributes)
    newTableName = "Output_FDS_" + originalTableNameAbreviation + "_ "+attributeStr
    createTableStr = "CREATE TABLE "+ newTableName +" ( LHS TEXT, RHS TEXT );"
    cursor.execute(createTableStr)
    for FD in FDset:
        insertStr = "INSERT INTO " + newTableName + " (LHS, RHS) VALUES (" + makeSelect(FD[0]), makeSelect(FD[1]) + ");"
    pass
