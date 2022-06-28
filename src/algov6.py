from z3 import *
from utilZ3v6 import *

taille_anneau = 3
nb_robots = 3
cpt = 0

taille_boucle_max = (factorial(8 * taille_anneau + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * taille_anneau - 1))
print("taille_anneau = ", taille_anneau)
print("nb_robots = ", nb_robots)
print("taille_boucle_max = ", taille_boucle_max)

k = 1

p = [ Int('p%s' % i) for i in range(nb_robots) ]
s = [ Int('s%s' % i) for i in range(nb_robots) ]
t = [ Int('t%s' % i) for i in range(nb_robots) ]

while True:

        I = Init(p, s, t, taille_anneau)

        constI = Init(p, s, t, taille_anneau)
        continuer = True
        pk = []
        sk = []
        tk = []
        for i in range(k):
                pk.append([ Int('kp%s%s' % (i, j)) for j in range(nb_robots) ])
                sk.append([ Int('ks%s%s' % (i, j)) for j in range(nb_robots) ])
                tk.append([ Int('kt%s%s' % (i, j)) for j in range(nb_robots) ])

        while continuer:

                print("boucle pour k = ", k)
                tmpAndInterpolant = []
                tmpAndContext = []

                tmpAndInterpolant.append(I)
                print("Post %s" % 1)
                tmpAndInterpolant.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSM))
                for i in range(k-1):
                        print("Post %s" % (i+1))
                        tmpAndContext.append(AsyncPost(taille_anneau, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiSM))
                tmpAndContext.append(BouclePerdante_v3(taille_anneau, p, s, t, pk, sk, tk, phiSM))
                try:
                        Ip = tree_interpolant(And(Interpolant(And(tmpAndInterpolant)), And(tmpAndContext)))
                except ModelRef as m:
                        if I == constI:
                                print("Stratégie perdante\nk = ", k)
                                print(m.sexpr())
                                exit()
                        k = k + 1
                        print("On augmente k : ", k, "\n")
                        continuer = False
                if continuer:
                        sol = Solver()
                        sol.add(Implies(And(Ip), I))
                        if sol.check() == sat:
                                print("Stratégie gagnante\n")
                                exit()
                        else:
                                I = Or(I, Ip)