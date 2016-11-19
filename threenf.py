import sqlite3
import sys

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
