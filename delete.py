import sqlite3

def deleteOutputTables(cursor):
    cursor.excecute(SELECT name FROM sqlite_master WHERE type='table';)
    tables = cursor.fetchall()
    deleteTables = [table for table in tables if "output" in table.lower()]
    dropStr = " DROP TABLE IF EXISTS " + newTableName + ";"
    for table in deleteTables:
        cursor.excecute("DROP TABLE IF EXISTS " + table + ";")
