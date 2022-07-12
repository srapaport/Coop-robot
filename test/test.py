from z3 import *
import sys
sys.path.insert(0, '../src')
from utilZ3v7 import *

taille_anneau = 3
nb_robot  = 2

p = [ Int('p%s' % (i)) for i in range(nb_robot) ]
s = [ Int('s%s' % (i)) for i in range(nb_robot) ]
t = [ Int('t%s' % (i)) for i in range(nb_robot) ]

p2 = [ Int('p2%s' % (i)) for i in range(nb_robot) ]
s2 = [ Int('s2%s' % (i)) for i in range(nb_robot) ]
t2 = [ Int('t2%s' % (i)) for i in range(nb_robot) ]

tab0 = []
tab1 = []
tab0.append(Init(p, s, t, taille_anneau))
tab0.append(AsyncPost(taille_anneau, nb_robot, p, s, t, p2, s2, t2, phiSimple))
for i in range(3, 10):
    tab1.append(BouclePerdante(taille_anneau, p2, s2, t2, i, phiSimple))
    sol = Solver()
    sol.add(tab0)
    sol.add(tab1)
    c = sol.check()
    if c == sat:
        print("test1")
        print("model : ", sol.model().sexpr())
        exit()
    else:
        print("test2")
        print("solver : ", c)
        del tab1[-1]


# try:
#     Ip = tree_interpolant(And(Interpolant(And(tab0)), And(tab1)))
#     print(Ip)
# except ModelRef as m:
#     print("Interpolant est satisfiable --> Boucle perdante pour taille_boucle = 5")
#     print(m.sexpr())