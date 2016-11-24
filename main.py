import sqlite3
import sys
import menu
import normalization_menu
import equivalence_menu
import closure_menu
import ColumnTypes
from ColumnTypes import ColumnTypes



def getAttrTypes(createTableStr):
    AttrTypes = {}
    openBracketI = createTableStr.find('(')
    closedBracketI = createTableStr.find(')')
    data = createTableStr[openBracketI + 1:closedBracketI]
    data = data.replace("\n", "")
    print data
    attrItems = data.split(",")
    print attrItems
    typeDict = dict()
    for attrWithType in attrItems:
        attrWithType = attrWithType.strip()
        itemTypePairs = attrWithType.split(" ")
        AttrTypes[itemTypePairs[0]] = itemTypePairs[1].rstrip()
    return AttrTypes

def deleteOutputTables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print tables
    deleteTables = [table[0] for table in tables if "output" in table[0].lower()]
    for table in deleteTables:
        cursor.execute("DROP TABLE IF EXISTS " + table + ";")


def createDict(tables):
    names = []
    fds = []
    for r in tables:
        r = str(r)[9:]
        r = r.strip('\',)')
        if 'FDs' in str(r): fds.append(r)
        if 'FDs' not in str(r): names.append(r)


    d = {}
    for n in names:
        for f in fds:
            if n in f: d[n] = f
    return d




if __name__ == "__main__":
    connInfo = menu.getDataBaseConnection()
    connection = connInfo[0]
    dbName = connInfo[1]
    cursor = connection.cursor()
    deleteOutputTables(cursor)
    connection.commit()
    cursor.execute("SELECT * FROM SQLITE_MASTER;")
    tableData = cursor.fetchall()
    # get the types fro each attribite
    for data in tableData:
        tableName = data[1]
        if("fds" not in tableName.lower() and "input" in tableName.lower()):
            print "data[4]"
            print data[4]
            ColumnTypes.setTypes(getAttrTypes(data[4]))

    tables = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE type = 'table';")

    tables = createDict(tables)

    print("\nConnected to Database!")
    choice = ""
    while(True):
        print("\n1. Normalize a Table (N)\n2. Test Closure on a Set of Attributes (C)\n3. Test Equivalency of Sets of Functional Dependencies (E)\n4. Quit Application (Q)")
        choice = raw_input("What would you like to do: ")
        if choice.upper() == 'N': normalization_menu.normalizationStory(dbName, tables, cursor)
        elif choice.upper() == 'C': closure_menu.closureStory(cursor)
        elif choice.upper() == 'E': equivalence_menu.equivalenceStory(tables, cursor)
        elif choice.upper() == 'Q': sys.exit(0)
