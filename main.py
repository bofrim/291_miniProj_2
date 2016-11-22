import sqlite3
import sys
import menu
import bcnf
import threenf
import normalization_menu
import equivalence_menu
import closure_menu
from computations import *

AttrTypes = {}

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

# def getAttributeTypes(tables):
#     for r in tables:


if __name__ == "__main__":
    connection = menu.getDataBaseConnection()
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE type = 'table';")
    tables = createDict(tables)

    print("\nConnected to Database!")
    choice = ""
    while(True):
        print("\n1. Normalize a Table (N)\n2. Test Closure on a Set of Attributes (C)\n3. Test Equivalency of Sets of Functional Dependencies (E)\n4. Quit Application (Q)")
        choice = raw_input("What would you like to do: ")
        if choice.upper() == 'N': normalization_menu.normalizationStory(tables, cursor)
        elif choice.upper() == 'C': closure_menu.closureStory(cursor)
        elif choice.upper() == 'E': equivalence_menu.equivalenceStory(tables, cursor)
        elif choice.upper() == 'Q': sys.exit(0)
