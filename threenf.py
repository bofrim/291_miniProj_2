import sqlite3
import sys
import computations

def threenf(fdLIst):
    return 0;

def mininal_cover(attributes, FDs):
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
