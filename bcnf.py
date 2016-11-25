import sqlite3
import sys
import computations
import copy


# constants
ATTRIBUTES = 0
FDS = 1
LHS = 0
RHS = 1
BCNF = 0
NON_BCNF = 1

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

# determine if a funtional dependancy is trivial
def isTrivial(fd):
    return fd[RHS].issubset(fd[LHS])


# return -1 if in BCNF eles return the index of the offending fd
def inBCNF(schema):
    # get the key for the schema
    minKey = computations.getKeyFromFDs(schema[ATTRIBUTES],schema[FDS])
    # loop throught the functional dependancies
    i = 0
    for fd in schema[FDS]:
        #is in BCNF only if FD is trivial or if the dependant is a superkey of the relation
        if(isTrivial(fd) == False and minKey.issubset(fd[LHS]) == False):
            return i
        i += 1

    return -1

# partition the input schema into a BCNF partition and a non-BCNF partition
def decompose(schema, offendingFD):

    bcnfPartition = [{},[]]
    nonBcnfPartition = [{},[]]

    # the attributes in the bcnf partition are those involved in the offending fd
    bcnfPartition[ATTRIBUTES] = schema[FDS][offendingFD][LHS] | schema[FDS][offendingFD][RHS]
    # the attriburts in the non-bcnf partition are those in the input schema minus the RHS of the offendingFD
    nonBcnfPartition[ATTRIBUTES] = schema[ATTRIBUTES] - schema[FDS][offendingFD][RHS]

    # now resolve the functional dependancies
    # the BCNF one first, find all fds that involve only the attributes in bcnfPartition
    for fd in schema[FDS]:
        if(fd[LHS].issubset(bcnfPartition[ATTRIBUTES])):
            # remove attributes that are not part of bcnfPartition[ATTRIBUTES] from RHS
            fdToAdd = (copy.deepcopy(fd[LHS]), fd[RHS] & bcnfPartition[ATTRIBUTES])
            if len(fdToAdd[RHS]) > 0:
                bcnfPartition[FDS].append(fdToAdd)


    # now the non-BCNF one, dont add FDs whose LHS has items from the offending FDs LHS
    for fd in schema[FDS]:
        if(bool(fd[LHS] & schema[FDS][offendingFD][RHS])): # there is some overlap between the offending Fds RHS and the new fds LHS
            continue
        else: # remove items from the offending fds RHS then add
            newFd = (fd[LHS], fd[RHS] - schema[FDS][offendingFD][RHS])
            if len(newFd[RHS]) > 0:
                nonBcnfPartition[FDS].append(newFd)
    # print ((bcnfPartition[ATTRIBUTES],bcnfPartition[FDS]),(nonBcnfPartition[ATTRIBUTES],nonBcnfPartition[FDS]))
    return ((bcnfPartition[ATTRIBUTES],bcnfPartition[FDS]),(nonBcnfPartition[ATTRIBUTES],nonBcnfPartition[FDS]))



def convertToBCNF(nonBcnfRelations):
    bcnfRelations = []

    while len(nonBcnfRelations) != 0:
        for relation in nonBcnfRelations:
            offendingFdIndex = inBCNF(relation)

            if(offendingFdIndex != -1 ):

                partitions =  decompose(relation, offendingFdIndex)
                bcnfRelations.append(partitions[BCNF])
                nonBcnfRelations.append(partitions[NON_BCNF])
                nonBcnfRelations.remove(relation)
            else:
                bcnfRelations.append(relation)
                nonBcnfRelations.remove(relation)

    return bcnfRelations


if __name__ == '__main__':
    # TEST 1
    inputR = {'A','B','C','D','E','F','G','H'}

    inputFD = []
    inputFD.append(({'A','B','H'},{'C'}))
    inputFD.append(({'A'},{'D','E'}))
    # inputFD.append(({'C'},{'E'}))
    inputFD.append(({'B','G','H'},{'F'}))
    inputFD.append(({'F'},{'A','D','H'}))
    # inputFD.append(({'E'},{'F'}))
    inputFD.append(({'B','H'},{'E','G'}))

    print convertToBCNF([(inputR,inputFD)])

    # TEST 2
    inputR2 = {'A','B','C','D','E','F','G','H','K'}

    inputFD2 = []
    inputFD2.append(({'A','B','H'},{'C','K'}))
    inputFD2.append(({'A'},{'D'}))
    inputFD2.append(({'C'},{'E'}))
    inputFD2.append(({'B','G','H'},{'F'}))
    inputFD2.append(({'F'},{'A','D'}))
    inputFD2.append(({'E'},{'F'}))
    inputFD2.append(({'B','H'},{'E'}))

    decomposition =  convertToBCNF([(inputR2,inputFD2)])
    print decomposition
    print "dependancy preserving"
    print computations.isDependancyPreserving([(inputR2,inputFD2)],decomposition)

    print "test create table logic"

    # computations.createTablesFromDecomposition(decomposition)
    computations.createNewFilledTables(decomposition,"R1","MiniProject2-InputExample.db")
