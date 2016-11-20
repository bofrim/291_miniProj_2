import computations
import copy

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

def decompose(thing, offendingIndex):
    print "thing from decompose"
    print thing
    
    BCNFThing = [None,None]
    NONBCNFThing = [None,None]
    
    BCNFThing[0] = thing[1][offendingIndex][0] | thing[1][offendingIndex][1]
    print("BCNFThing[0]")
    print(BCNFThing[0])
    NONBCNFThing[0] = thing[0] - thing[1][offendingIndex][1]
    print("NONBCNFThing[0]")
    print(NONBCNFThing[0])
    BCNFThing[1] = []
    NONBCNFThing[1] = []
    # now resolve the functional dependancies

    # the BCNF one first, find all fds that involve only the attributes in BCNFThing
    for fd in thing[1]:
        allInvolvedInFD = fd[0] | fd[1]
        if(allInvolvedInFD == BCNFThing[0]):
            if len(fd[1]) > 0:
                BCNFThing[1].append(fd)

    # now the non-BCNF one, dont add FDs whose LHS has items from the offending FDs LHS
    for fd in thing[1]:
        if(bool(fd[0] & thing[1][offendingIndex][1])): # there is some overlap between the offending Fds RHS and the new fds LHS
            continue
        else: # remove items from the offending fds RHS then add
            newFd = (fd[0], fd[1] - thing[1][offendingIndex][1])
            if len(newFd[1]) > 0:
                NONBCNFThing[1].append(newFd)
    return ((BCNFThing[0],BCNFThing[1]),(NONBCNFThing[0],NONBCNFThing[1]))



def decomposition(S):
    finalSet = []

    while len(S) != 0:
        print("first S")
        print(S)
        for element in S:
            offendingFdIndex = inBCNF(element)
            print("offendingFdIndex: " + str(offendingFdIndex))
            if(offendingFdIndex != -1 ):
                # first return element will be in BCNF the second wont be
                newThings =  decompose(element, offendingFdIndex) 
                print("newThings[0]")
                print(newThings[0])
                print("newThings[1]")
                print(newThings[1])
                finalSet.append(newThings[0])
                S.append(newThings[1])
                S.remove(element)
            else:
                finalSet.append(element)
                S.remove(element)
        print("finalset")
        print(finalSet)
        print("S")
        print(S)
        raw_input()

    return finalSet

print decomposition([(inputR,inputFD)])

                