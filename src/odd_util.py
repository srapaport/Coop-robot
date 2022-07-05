from z3 import *
from utilZ3v7 import *

def IsOddNonPeriodic(distances):
    tabAnd = []
    tabAnd.append( ( (len(distances) + 1) % 2 ) == 0 )
    tabOr = []
    d_prime = [ Int('IsOdd_d_prime%s' % (i)) for i in range(len(distances)) ]
    for p in range(2, int(((len(distances)-1)/2) + 1 ) ):
        tabAndBis = []
        for i in range(len(distances)):
            tabAndBis.append(d_prime[i%p] == distances[i])
        tabAndBis.append(distances[-1] != d_prime[-1])
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return And(tabAnd)

###################### Odd Non Periodic configuration
distances = [ Int('d%s' % (i)) for i in range(9) ]
tab = IsOddNonPeriodic(distances)
sol = Solver()
sol.add(And(distances[0] == 2, distances[1] == 2, distances[2] == 1, distances[3] == 2, distances[2] == 1,))
sol.add(tab)
c = sol.check()
print("solver : ", c)
if c == sat:
    print(sol.model().sexpr())
######################