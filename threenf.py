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
    superkey = computations.getKeyFromFDs(set(attributes),fdList)
    print("Superkey")
    print(superkey)
    print

    minCover = minimal_cover(fdList)
    print("Min Cover")
    print(minCover)
    print
    partitions = partitionMinCover(minCover)
    print("Partitions")
    print(partitions)
    print

    newAttributes = set()
    schemas = createSchemas(partitions)
    print("Schemas")
    for schema in schemas:
        print(schema)
        print
        for guy in schema[0]:
            newAttributes.add(guy)

    newAttributes = list(newAttributes)
    print("New Attributes")
    print(newAttributes)
    print

    lostAttributes = [x for x in attributes if x not in newAttributes]
    if lostAttributes:
        schemas.append(tuple((superkey.union(set(lostAttributes)),[])))
        print("Schemas NEW")
        for schema in schemas:
            print(schema)
            print
        return ([schema[0] for schema in schemas],[schema[1] for schema in schemas]);


    for schema in schemas:
        if schema[0] == superkey: return ([schema[0] for schema in schemas],[schema[1] for schema in schemas]);

    schemas.append(tuple((superkey,[])))
    return ([schema[0] for schema in schemas],[schema[1] for schema in schemas]);

def minimal_cover(FDs):
    # 1. Make RHS of each FD into a single attribute
    # 2. Eliminate redundant attributes from LHS.
    # 3. Delete redundant FDs
    #
    # Assume FDs is a list of tupes of sets. The list is a list of
    #   functional dependencies, the tupes represent each funcitional
    #   dependency, the sets are the LHS and the RHS:
    # [({LHS1}, {RHS1}), ({LHS2}, {RHS2}), ..., ({LHSn}, {RHSn})]
    FDs = break_up_RHS(FDs)
    FDs = simplify_LHS(FDs)
    FDs = remove_redundant_FDs(FDs)
    return FDs

def break_up_RHS(FDs):
    new_FDs = []
    for FD in FDs:
        for attribute in FD[1]:
            new_FDs.append((FD[0], set([attribute])))
    return new_FDs

def simplify_LHS(FDs):
    original_FDs = copy.deepcopy(FDs)
    for FD in original_FDs:
        # Iterate over each attribute of the LHS, and compute the closuer with the attribute removed, if the closure does not change, remove it from the LHS
        og_RHS = FD[1]
        for attribute in FD[0]:
            LHS = FD[0]
            remove_attribute = set([attribute])
            close = computations.closure(copy.deepcopy(LHS-remove_attribute), copy.deepcopy(FDs))
            if close.issuperset(og_RHS):
                original_FDs[FDs.index(FD)] = tuple(((FD[0]-set(attribute)).copy(), FD[1]))
    return original_FDs

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
            if (l[0][0] == LHS):
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
    return schemas
