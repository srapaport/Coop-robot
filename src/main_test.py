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

# d0 = [ Int('d%s' % i) for i in range(nb_robots) ]
# d1 = [ Int('d%s' % i) for i in range(nb_robots) ]
# d2 = [ Int('d%s' % i) for i in range(nb_robots) ]

tabInit = InitSM(p, s, t, taille_anneau)
# tabPhiSM1 = phiSM(d0)
tabAP1 = AsyncPost(taille_anneau, nb_robots, p, s, t, p_prime, s_prime, t_prime, phiSM)
solv1 = Solver()
solv1.add(tabInit)
solv1.add(tabAP1)
# solv1.add(tabPhiSM1)
c = solv1.check()
print("solv1 : ", c)
if(c == sat):
        print("model :\n",solv1.model())

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