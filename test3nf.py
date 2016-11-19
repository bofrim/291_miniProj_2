import sqlite3
import sys
import threenf

example = [({1, 2, 3}, {2, 3, 4, 5}), ({1}, {1}), ({}, {6}), ({3}, {})]
expected = [({1, 2, 3}, {2}), ({1, 2, 3}, {3}), ({1, 2, 3}, {4}), ({1, 2, 3}, {5}), ({1}, {1}), ({}, {6})]

test = threenf.break_up_RHS(example)
if test == expected: print "Passed"

# T = {ABH -> CK, A -> D, C -> E, BGH -> F, F -> AD, E -> F, BH -> E}
example2 = [({'A', 'B', 'H'}, {'C', 'K'}), ({'A'}, {'D'}), ({'C'}, {'E'}), ({'B', 'G', 'H'}, {'F'}), ({'F'}, {'A', 'D'}), ({'E'}, {'F'}), ({'B', 'H'}, {'E'})]
expected2 = [({'B', 'H'}, {'C'}), ({'B', 'H'}, {'K'}), ({'A'}, {'D'}), ({'C'}, {'E'}), ({'B', 'H'}, {'F'}), ({'F'}, {'A'}), ({'F'}, {'D'}), ({'E'}, {'F'}), ({'B', 'H'}, {'E'})]


test2 = threenf.break_up_RHS(example2)
test2Simple = threenf.simplify_LHS(test2)
print test2Simple
print expected2
