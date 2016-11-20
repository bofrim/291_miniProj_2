import sqlite3
import sys
import threenf
import computations
import copy

# example = [({1, 2, 3}, {2, 3, 4, 5}), ({1}, {1}), (set(), {6}), ({3}, set())]
# expected = [({1, 2, 3}, {2}), ({1, 2, 3}, {3}), ({1, 2, 3}, {4}), ({1, 2, 3}, {5}), ({1}, {1}), (set(), {6})]
# expected2 = [[({1, 2, 3}, {2}), ({1, 2, 3}, {3}), ({1, 2, 3}, {4}), ({1, 2, 3}, {5})], [({1}, {1})], [(set(), {6})]]
# expected3 = [({1,2,3,4,5},[({1, 2, 3}, {2}), ({1, 2, 3}, {3}), ({1, 2, 3}, {4}), ({1, 2, 3}, {5})]),({1},[({1}, {1})]),({6},[(set(), {6})])]
#
# test = threenf.break_up_RHS(example)
# print "Output (top) and expected output (bottom):"
# print test
# print
# print expected
# if test == expected: print "Passed"
# print
#
# test = threenf.partitionMinCover(test)
# print "Output (top) and expected output (bottom):"
# print test
# print
# print expected2
# if test == expected2: print "Passed"
# print
#
# test = threenf.createSchemas(test)
# print "Output (top) and expected output (bottom):"
# print test
# print
# print expected3
# if test == expected3: print "Passed"
# print
# if test == expected: print "Passed"

# # T = {ABH -> CK, A -> D, C -> E, BGH -> F, F -> AD, E -> F, BH -> E}
example2 = [({'A', 'B', 'H'}, {'C', 'K'}), ({'A'}, {'D'}), ({'C'}, {'E'}), ({'B', 'G', 'H'}, {'F'}), ({'F'}, {'A', 'D'}), ({'E'}, {'F'}), ({'B', 'H'}, {'E'})]
expected2 = [({'B', 'H'}, {'C'}), ({'B', 'H'}, {'K'}), ({'A'}, {'D'}), ({'C'}, {'E'}), ({'B', 'H'}, {'F'}), ({'F'}, {'A'}), ({'F'}, {'D'}), ({'E'}, {'F'}), ({'B', 'H'}, {'E'})]


test2 = threenf.break_up_RHS(example2)
test2Simple = threenf.simplify_LHS(test2)
print test2Simple
print
print expected2

print "*****************************************"
print

removalTest = [({'A', 'B'}, {'C'}), ({'A', 'B'}, {'D'}), ({'C'}, {'D'})]
expect = [({'A', 'B'}, {'C'}), ({'C'}, {'D'})]

testRemove = threenf.remove_redundant_FDs(copy.deepcopy(removalTest))

print "*****************************************"
print
print " Input: " + str(removalTest)
print "Output: " + str(testRemove)
print "Expect: " + str(expect)
