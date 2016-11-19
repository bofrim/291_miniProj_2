import computations

inputR = {'A','B','C','D','E','F','G','H','K'}

inputFD = []
inputFD.append(({'A','B','H'},{'C','K'}))
inputFD.append(({'A'},{'D'}))
inputFD.append(({'C'},{'E'}))
inputFD.append(({'B','G','H'},{'F'}))
inputFD.append(({'F'},{'A','D'}))
inputFD.append(({'E'},{'F'}))
inputFD.append(({'B','H'},{'E'}))

print computations.getKeyFromFDs(inputFD)


# Start with a decomposition which is 
# decomp = [(inputR,inputFD)]

# method that determines if the decomposition violates BCNF




# def inBCNF(decomp):
    #is in BCNF only if FD is trivial or if the dependant is a superkey of the relation
