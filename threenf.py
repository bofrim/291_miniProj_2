import sqlite3
import sys
import computations
import copy

def threenf(attributes, fdList):
    '''
    Synthesize relation into 3NF

    STEP 1
    minCover = minimal_cover(attributes, FDs)
    STEP 2
    partions = partitionMinCover(minCover)
    STEP 3
    schemas = createSchemas(partitions)
    STEP 4
    if there is no superkey of the original relation in the schemas,
    add it as Ro = (superkey, {})

    Output tables are [schema[0] for schema in schemas]
    Output FDs are [schema[1] for schema in schemas]

    return: ( [Ouput relations], [Ouput FDs] )

    '''
    # superkey of original relation
    superkey = computations.getKeyFromFDs(fdList)
    print(superkey)

    minCover = minimal_cover(attributes, fdList)
    print(minCover)
    partions = partitionMinCover(minCover)
    print(partitions)
    schemas = createSchemas(partitions)
    print(schemas)

    for schema in schemas:
        if superkey == schema[0]:
            # found the superkey, we gooooood
            return ([schema[0] for schema in schemas],[schema[1] for schema in schemas]);
    # oh no we didn't find the superkey

    return ([schema[0] for schema in schemas],[schema[1] for schema in schemas]);

def minimal_cover(attributes, FDs):
    # 1. Make RHS of each FD into a single attribute
    # 2. Eliminate redundant attributes from LHS.
    # 3. Delete redundant FDs
    #
    # Assume FDs is a list of tupes of sets. The list is a list of
    #   functional dependencies, the tupes represent each funcitional
    #   dependency, the sets are the LHS and the RHS:
    # [({LHS1}, {RHS1}), ({LHS2}, {RHS2}), ..., ({LHSn}, {RHSn})]
    pass

def break_up_RHS(FDs):
    new_FDs = []
    for FD in FDs:
        for attribute in FD[1]:
            new_FDs.append((FD[0], set([attribute])))
    return new_FDs

def simplify_LHS(FDs):
    for FD in FDs:
        # Iterate over each attribute of the LHS, and compute the closuer with the attribute removed, if the closure does not change, remove it from the LHS
        og_RHS = FD[1]
        for attribute in FD[0]:
            if computations.closure(FD[0]-set([attribute]), FDs).issuperset(og_RHS):
                FDs[FDs.index(FD)] = tuple(((FD[0]-set(attribute)).copy(), FD[1]))
    return FDs

def remove_redundant_FDs(FDs):
    original_FDs = copy.deepcopy(FDs)
    for FD in original_FDs:
        FDs_withoutFD = copy.deepcopy(original_FDs)
        FDs_withoutFD.remove(FD)
        closure_temp = computations.closure(copy.deepcopy(FD[0]), copy.deepcopy(FDs_withoutFD))
        if FD[1].issubset(closure_temp):
            FDs.remove(FD)
    return FDs


def partitionMinCover(minCover):
    '''
    Step 2 of Synthesizing 3NF

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
                break;
        had.append(LHS)
    return partitions

def createSchemas(partitions):
    '''
    Step 3 of Synthesizing 3NF

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

    # check if relation (Ro, {}) is needed in the created schema
    # this guarantees losslesness

    return schemas
