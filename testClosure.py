def compute_closure(X, FDs):
    # Take a set of attributes, X, and an array of tuples of sets, FDs, representing all of the functional dependencies for the table: conpute the closure of X
    closure = X
    old = {}
    while(old != closure):
        old = closure.copy()
        for FD in FDs:
            if FD[0].issubset(closure):
                closure |= FD[1]
    return closure


FDs = [({'A','B'},{'C'}),({'C'},{'E'}),({'A','D'},{'F'}),({'C'},{'D'}), ({'C'},{'G'}), ({'C', 'E', 'D', 'G'},{'H'})]
print "The closure for {C} is: "
print compute_closure({'C'}, FDs)
print "The closure for {A,D} is: "
print compute_closure({'A', 'D'}, FDs)
print "The closure for {A,B} is: "
print compute_closure({'A', 'B'}, FDs)
print "Fin"
