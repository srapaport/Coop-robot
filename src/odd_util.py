from z3 import *
from utilZ3v7 import *
from rigid_util import *
import math

def IsOdd(distances):
    tabAnd = []
    tabAnd.append( ( (len(distances) + 1) % 2 ) == 0 )
    tabAnd.append(len(distances) > 2)
    return And(tabAnd)

def IsPeriodic(distances):
    tabAnd = []
    tabOr = []
    borne_sup_p = math.floor(len(distances)/3)
    d_prime = []
    for p in range(1, borne_sup_p + 1, 2):
        d_prime.append([ Int('IsOdd_d_prime%s%s' % (p, i)) for i in range(p) ])
        print(d_prime)
        print("p : ", p)
        tabAndBis = []
        for i in range(len(distances)):
            print("d_prime[", i%p,"] == dist[",i,"]")
            tabAndBis.append(d_prime[-1][i%p] == distances[i])
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return Exists( [d_prime[i][j] for i in range(len(d_prime)) for j in range(len(d_prime[i]))], And(tabAnd))

###################### Odd Non Periodic configuration
# distances = [ Int('d%s' % (i)) for i in range(3) ]
# tab0 = IsOdd(distances)
# tab = IsPeriodic(distances)
# sol = Solver()
# sol.add(And(distances[0] == 1, distances[1] == 1, distances[2] == 1))
# #sol.add(And(distances[0] == 3, distances[1] == 2, distances[2] == 1, distances[3] == 3, distances[4] == 2, distances[5] == 1, distances[6] == 3, distances[7] == 2, distances[8] == 1))
# sol.add(Not(tab))
# c = sol.check()
# print("solver : ", c)
# if c == sat:
#     print(sol.model().sexpr())
# for i in range(2,40,2):
#     sol = Solver()
#     sol.add(IsOddNonPeriodic([ Int('d%s' % (j)) for j in range(i) ]))
#     print("solver ",i," : ", sol.check())
######################

def phiON(taille_anneau, distance):
    tabAnd = []
    ad = []
    vs = []
    for i in range(len(distance)):
        ad.append([ Int('phiONad%s%s' % (i,j)) for j in range(len(distance)) ])
        vs.append([ Int('phiONvs%s%s' % (i,j)) for j in range(len(distance)) ])
    tabAnd.append(AllView(distance, ad))
    for i in range(len(distance)):
        tabAnd.append(ViewSym(taille_anneau, ad[i], vs[i]))
    tabAnd.append(Not(IsRigid(ad, vs)))
    tabAnd.append(IsOdd(distance))
    tabAnd.append(Not(IsPeriodic(distance)))
    for i in range(len(distance)):
        tabAnd.append(distance[i] != 0)
        tabAnd.append(distance[i] == vs[0][i])
    return And(tabAnd)

###################### phiON
# taille_anneau = 12
# distances = [ Int('d%s' % (i)) for i in range(5) ]
# sol = Solver()
# sol.add(And(distances[0] == 2, distances[1] == 2, distances[2] == 4, distances[3] == 2, distances[4] == 2))
# tab0 = phiON(taille_anneau, distances)
# sol.add(tab0)
# c = sol.check()
# print("solver : ", c)
# if c == sat:
#     print(sol.model().sexpr())
######################