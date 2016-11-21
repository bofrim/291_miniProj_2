import sqlite3
import sys
import menu
import bcnf
import threenf
import normalization_menu
import equivalence_menu
import closure_menu
from computations import *


# sqlite> SELECT * FROM Input_FDS_R1;
# LHS|RHS
# A,B,H|C,K
# A|D
# C|E
# B,G,H|F
# F|A,D
# E|F
# B,H|E

# sqlite> select * from Input_R1;
# A|B|C|D|E|F|G|H|K
# 245|19|193|735|273|B245H|O94J1U|129.0|2451.0
# 1739|93|933|5217|1013|B1739H|Y21LP1|187.0|17391.0
# 502|27|273|1506|353|B502H|JV4FI0|186.0|5022.0
# 1124|73|733|3372|813|B1124H|XIHXZW|154.0|11242.0
# 1293|66|663|3879|743|B1293H|ZROPW1|196.0|12936.0
# 1428|94|943|4284|1023|B1428H|M6DSAJ|152.0|14288.0
# 469|46|463|1407|543|B469H|415ZMN|102.0|4692.0
# 516|41|413|1548|493|B516H|9IAVU1|126.0|5166.0
# 469|37|373|1407|453|B469H|F1FKEK|127.0|4699.0
# 72|7|73|216|153|B72H|X06VUG|104.0|728.0

# STEP 1: Synthesize a 3NF schema for the given input table, using the algorithm presented in class and described in the textbook.

# STEP 2: Decompose the given input table into BCNF according the BCNF decomposition algorithm presented in class and described in the textbook. At the end it should be indicated if the resulting BCNF decomposition is dependency preserving.

# STEP 3: For each of the resulting new schemas, create tables similar to the input format, one for the data, and one for the the functional dependencies that hold on the new relation. The naming convention for the new schemas, which you must follow, is the following: each name of a data table has to start with 'Output_' followed by the name of the corresponding input table (without the 'Input_' prefix), followed by an underscore '_', followed by the concatenation of the attributes in the new table. For instance, if one of the tables in the decomposition of 'Input_R1' has only the attributes B, H, C, K, then the name of that table should be 'Output_R1_BHCK'. For each new data table, also include in the create table command the primary key constraint that can be derived from the way the decomposition was done. In addition, you must also create a table to store the functional dependencies of the new data table. The name of this table must start with 'Output_FDs_' followed by the corresponding data output table name (without the 'Output_' prefix). In the example where the new data table is called 'Output_R1_BHCK', the corresponding table for the functional dependencies must be called 'Output_FDS_R1_BHCK' and must have two columns named 'LHS', and 'RHS' storing the functional dependencies in the same way as in the input.

# STEP 4: After a decomposition of a schema into 3NF or BCNF, the user should have the option to decompose the original table instance according to the schema decomposition, i.e., fill the new data tables according to the decomposition, using the data in the input data table.  For instance, given the example input table Input_R1 (with the rows shown above) and a new output table Output_R1_BHCK, the content of Output_R1_BHCK should be as following:

# B|H|C|K
# 19|129.0|193|2451.0
# 93|187.0|933|17391.0
# 27|186.0|273|5022.0
# 73|154.0|733|11242.0
# 66|196.0|663|12936.0
# 94|152.0|943|14288.0
# 46|102.0|463|4692.0
# 41|126.0|413|5166.0
# 37|127.0|373|4699.0
# 7|104.0|73|728.0

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
    connection = menu.getDataBaseConnection()
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM SQLITE_MASTER WHERE type = 'table';")
    tables = createDict(tables)


    normalization_menu.normalizationStory(tables, cursor)
