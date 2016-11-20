import computations
import copy

# constants
ATTRIBUTES = 0 
FDS = 1
LHS = 0
RHS = 1
BCNF = 0
NON_BCNF = 1


inputR = {'A','B','C','D','E','F','G','H'}

inputFD = []
inputFD.append(({'A','B','H'},{'C'}))
inputFD.append(({'A'},{'D','E'}))
# inputFD.append(({'C'},{'E'}))
inputFD.append(({'B','G','H'},{'F'}))
inputFD.append(({'F'},{'A','D','H'}))
# inputFD.append(({'E'},{'F'}))
inputFD.append(({'B','H'},{'E','G'}))

print "Before find key"
print inputFD
otherFD = copy.deepcopy(inputFD)
print computations.getKeyFromFDs(otherFD)
print "after find key"
print inputFD
# Start with a decomposition which is 
# decomp = [(inputR,inputFD)]

# method that determines if the decomposition violates BCNF

def isTrivial(fd):
    return fd[1].issubset(fd[0])


# return -1 if in BCNF eles return the index of the offending fd
def inBCNF(decomp):
    # get the key for the decomp
    minKey = computations.getKeyFromFDs(copy.deepcopy(decomp[1]))
    # loop throught the functional dependancies
    i = 0
    for fd in decomp[1]:
        #is in BCNF only if FD is trivial or if the dependant is a superkey of the relation
        if(isTrivial(fd) == False and minKey.issubset(fd[0]) == False):
            return i
        i += 1

    return -1

def decompose(schema, offendingFD):
    # print "schema from decompose"
    # print schema

    
    bcnfPartition = [{},[]]
    nonBcnfPartition = [{},[]]
    
    bcnfPartition[ATTRIBUTES] = schema[FDS][offendingFD][LHS] | schema[FDS][offendingFD][RHS]
    # print("bcnfPartition[0]")
    # print(bcnfPartition[0])
    nonBcnfPartition[ATTRIBUTES] = schema[ATTRIBUTES] - schema[FDS][offendingFD][RHS]
    # print("nonBcnfPartition[0]")
    # print(nonBcnfPartition[0])
    # now resolve the functional dependancies

    # the BCNF one first, find all fds that involve only the attributes in bcnfPartition
    for fd in schema[FDS]:
        if(fd[LHS].issubset(bcnfPartition[ATTRIBUTES])):
            # remove attributes that are not part of bcnfPartition[ATTRIBUTES] from RHS
            fdToAdd = (copy.deepcopy(fd[LHS]), fd[RHS] & bcnfPartition[ATTRIBUTES])
            if len(fdToAdd[RHS]) > 0:
                bcnfPartition[FDS].append(fdToAdd)

        # if(allInvolvedInFD == bcnfPartition[ATTRIBUTES]):
        #     if len(fd[RHS]) > 0:
        #         bcnfPartition[FDS].append(fd)

    # now the non-BCNF one, dont add FDs whose LHS has items from the offending FDs LHS
    for fd in schema[FDS]:
        if(bool(fd[LHS] & schema[FDS][offendingFD][RHS])): # there is some overlap between the offending Fds RHS and the new fds LHS
            continue
        else: # remove items from the offending fds RHS then add
            newFd = (fd[LHS], fd[RHS] - schema[FDS][offendingFD][RHS])
            if len(newFd[RHS]) > 0:
                nonBcnfPartition[FDS].append(newFd)
    return ((bcnfPartition[ATTRIBUTES],bcnfPartition[FDS]),(nonBcnfPartition[ATTRIBUTES],nonBcnfPartition[FDS]))



def convertToBCNF(nonBcnfRelations):
    bcnfRelations = []

    while len(nonBcnfRelations) != 0:
        # print("first nonBcnfRelations")
        # print(nonBcnfRelations)
        for relation in nonBcnfRelations:
            offendingFdIndex = inBCNF(relation)
            # print("offendingFdIndex: " + str(offendingFdIndex))
            if(offendingFdIndex != -1 ):
                # first return relation will be in BCNF the second wont be
                partitions =  decompose(relation, offendingFdIndex) 
                # print("partitions[BCNF]")
                # print(partitions[BCNF])
                # print("partitions[1]")
                # print(partitions[NON_BCNF])
                bcnfRelations.append(partitions[BCNF])
                nonBcnfRelations.append(partitions[NON_BCNF])
                nonBcnfRelations.remove(relation)
            else:
                bcnfRelations.append(relation)
                nonBcnfRelations.remove(relation)
        # print("bcnfRelations")
        # print(bcnfRelations)
        # print("nonBcnfRelations")
        # print(nonBcnfRelations)
        # raw_input()

    return bcnfRelations

print convertToBCNF([(inputR,inputFD)])

                