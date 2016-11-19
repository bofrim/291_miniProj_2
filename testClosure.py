import computations


FDs = [({'A','B'},{'C'}),({'C'},{'E'}),({'A','D'},{'F'}),({'C'},{'D'}), ({'C'},{'G'}), ({'C', 'E', 'D', 'G'},{'H'})]
print "The closure for {C} is: "
print computations.closure({'C'}, FDs)
print "The closure for {A,D} is: "
print computations.closure({'A', 'D'}, FDs)
print "The closure for {A,B} is: "
print computations.closure({'A', 'B'}, FDs)
print "Fin"
