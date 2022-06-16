from z3 import *
from utilZ3v5 import *

taille_anneau = 5       # Taille de l'anneau 
nb_robots = 3           # Nombre de robot sur l'anneau

p = [ Int('p%s' % i) for i in range(nb_robots) ]
s = [ Int('s%s' % i) for i in range(nb_robots) ]
t = [ Int('t%s' % i) for i in range(nb_robots) ]

p_prime = [ Int('pp%s' % i) for i in range(nb_robots) ]
s_prime = [ Int('sp%s' % i) for i in range(nb_robots) ]
t_prime = [ Int('tp%s' % i) for i in range(nb_robots) ]

p_prime2 = [ Int('pp2%s' % i) for i in range(nb_robots) ]
s_prime2 = [ Int('sp2%s' % i) for i in range(nb_robots) ]
t_prime2 = [ Int('tp2%s' % i) for i in range(nb_robots) ]

p_prime3 = [ Int('pp3%s' % i) for i in range(nb_robots) ]
s_prime3 = [ Int('sp3%s' % i) for i in range(nb_robots) ]
t_prime3 = [ Int('tp3%s' % i) for i in range(nb_robots) ]

# d0 = [ Int('d%s' % i) for i in range(nb_robots) ]
# d0_prime = [ Int('dp%s' % i) for i in range(nb_robots) ]
# d1 = [ Int('d%s' % i) for i in range(nb_robots) ]
# d2 = [ Int('d%s' % i) for i in range(nb_robots) ]

solv1 = Solver()

tabInit = InitSM(p, s, t, taille_anneau)
# solv1.add(tabInit)
# tabConfig1 = ConfigView(taille_anneau, nb_robots, 0, p, d0)
# solv1.add(tabConfig1)
# tabViewSym1 = ViewSym(taille_anneau, nb_robots, d0, d0_prime)
# solv1.add(tabViewSym1)

# next_position = Int('next')
# tabMove1 = Move(taille_anneau, nb_robots, 0, p, next_position, phiSM)
# solv1.add(tabMove1)

# tabPhiSM1 = phiSM(d0)
# solv1.add(tabPhiSM1)

# tabAP1 = AsyncPost(taille_anneau, nb_robots, p, s, t, p_prime, s_prime, t_prime, phiSM)
# solv1.add(tabAP1)
# tabAP2 = AsyncPost(taille_anneau, nb_robots, p_prime, s_prime, t_prime, p_prime2, s_prime2, t_prime2, phiSM)
# solv1.add(tabAP2)
# tabAP3 = AsyncPost(taille_anneau, nb_robots, p_prime2, s_prime2, t_prime2, p_prime3, s_prime3, t_prime3, phiSM)
# solv1.add(tabAP3)

# tabBP1 = BouclePerdante_v2(taille_anneau, p, s, t, 1, phiSM)
# solv1.add(tabBP1)

# tabBP1 = BouclePerdante_v2(taille_anneau, p, s, t, 2, phiSM)
# solv1.add(tabBP1)

# tabBP1 = BouclePerdante_v2(taille_anneau, p, s, t, 4, phiSM)
# solv1.add(tabBP1)

for i in range(2, 3):
        solv1 = Solver()
        print("Main appelle BouclePerdante de taille : ", i, "\n")
        tabBP1 = BouclePerdante(taille_anneau, p, s, t, i, phiSM)
        solv1.add(tabInit)
        solv1.add(tabBP1)
        c = solv1.check()
        print("solv1 : ", c)
        if(c == sat):
                print("model :\n",solv1.model().sexpr())
                break;


# c = solv1.check()
# print("solv1 : ", c)
# if(c == sat):
#         print("model :\n",solv1.model())

# tabPhiSM2 = phiSM(d1)
# tabConfig2 = ConfigView(taille_anneau, nb_robots, 1, p, d1)
# solv2 = Solver()
# solv2.add(tabInit)
# solv2.add(tabConfig2)
# solv2.add(tabPhiSM2)

# print("solv2 : ",solv2.check())
# if(solv2.check() == sat):
#         print("model :\n",solv2.model())

# tabConfig3 = ConfigView(taille_anneau, nb_robots, 2, p, d2)
# tabPhiSM3 = phiSM(d2)
# solv3 = Solver()
# solv3.add(tabInit)
# solv3.add(tabConfig3)
# solv3.add(tabPhiSM3)

# print("solv3 : ",solv3.check())
# if(solv3.check() == sat):
#         print("model :\n",solv3.model())