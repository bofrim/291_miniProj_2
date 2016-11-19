import sqlite3
import sys
import threenf
import computations

example = [({1, 2, 3}, {2, 3, 4, 5}), ({1}, {1}), ({}, {6}), ({3}, {})]
expected = [({1, 2, 3}, {2}), ({1, 2, 3}, {3}), ({1, 2, 3}, {4}), ({1, 2, 3}, {5}), ({1}, {1}), ({}, {6})]
expected2 = [[({1, 2, 3}, {2}), ({1, 2, 3}, {3}), ({1, 2, 3}, {4}), ({1, 2, 3}, {5})], [({1}, {1})], [({}, {6})]]

test = threenf.break_up_RHS(example)
print "Output (top) and expected output (bottom):"
print test
print
print expected
if test == expected: print "Passed"
print

test = computations.partitionMinCover(test)
print "Output (top) and expected output (bottom):"
print test
print
print expected2
if test == expected2: print "Passed"
print
