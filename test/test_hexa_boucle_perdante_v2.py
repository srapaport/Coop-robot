from z3 import *
from utilZ3v5 import *

taille_anneau = 5       # Taille de l'anneau 
nb_robots = 3           # Nombre de robot sur l'anneau

taille_boucle_max = (factorial(8 * taille_anneau + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * taille_anneau - 1))

p = [ Int('p%s' % i) for i in range(nb_robots) ]
s = [ Int('s%s' % i) for i in range(nb_robots) ]
t = [ Int('t%s' % i) for i in range(nb_robots) ]

solv1 = Solver()

tabInit = InitSM(p, s, t, taille_anneau)

for i in range(1, taille_boucle_max):
        solv1 = Solver()
        print("Main appelle BouclePerdante de taille : ", i)
        tabBP1 = BouclePerdante_v2(taille_anneau, p, s, t, i, phiSM)
        solv1.add(tabInit)
        solv1.add(tabBP1)
        c = solv1.check()
        print("solv1 : ", c)
        if(c == sat):
                print("model :\n",solv1.model().sexpr())
                break;