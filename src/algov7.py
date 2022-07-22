from z3 import *
from utilZ3v7 import *
import sys

if len(sys.argv) < 3:
        print("Pas assez d'argument")
        exit()

taille_anneau = int(sys.argv[1])
nb_robots = int(sys.argv[2])

taille_boucle_max = (factorial(8 * taille_anneau + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * taille_anneau - 1))
print("taille_anneau = ", taille_anneau)
print("nb_robots = ", nb_robots)
print("taille_boucle_max = ", taille_boucle_max)

k = (2*nb_robots) - 1 # On considère qu'initialement tous les s sont à -1 et tous les t à 0
NotThisSize = [i for i in range(k)]
MaybeThisSize = []

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

                if len(MaybeThisSize) > 0:
                        NotThisSizeBis = [i for i in range(k)]
                        for elem in MaybeThisSize:
                                NotThisSizeBis.remove(elem)
                        tabAnd = []
                        tabAnd.append(I)
                        tabAnd.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSimple))
                        for i in range(k-1):
                                print("Post %s" % (i+1))
                                tabAnd.append(AsyncPost(taille_anneau, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiSimple))
                        tabAnd.append(BouclePerdante_v4_1(taille_anneau, p, s, t, pk, sk, tk, phiSimple, NotThisSizeBis))
                        solBis = Solver()
                        solBis.add(And(tabAnd))
                        if solBis.check() == sat:
                                print("Stratégie perdante, elem = ", elem,"\nk = ", k)
                                print(m.sexpr())
                                exit()
                        else:
                                print("Pas de boucle perdante de taille : ", elem," pour k = ", k)


                print("boucle pour k = ", k)
                tmpAndInterpolant = []
                tmpAndContext = []

                tmpAndInterpolant.append(I)
                print("Post Init")
                tmpAndInterpolant.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSimple))
                for i in range(k-1):
                        print("Post %s" % (i+1))
                        tmpAndContext.append(AsyncPost(taille_anneau, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiSimple))
                tmpAndContext.append(BouclePerdante_v4_1(taille_anneau, p, s, t, pk, sk, tk, phiSimple, NotThisSize))
                try:
                        Ip = tree_interpolant(And(Interpolant(And(tmpAndInterpolant)), And(tmpAndContext)))
                except ModelRef as m:
                        if I == constI:
                                print("Stratégie perdante\nk = ", k)
                                print(m.sexpr())
                                exit()
                        MaybeThisSize.append(k)
                        k = k + 1
                        print("On augmente k : ", k, "\n")
                        continuer = False
                if continuer:
                        sol = Solver()
                        sol.add(And(And(Ip), Not(I)))
                        if sol.check() == unsat:
                                print("And(And(Ip), Not(I)) UNSAT")
                                if k == taille_boucle_max:
                                        print("Stratégie gagnante\n")
                                        exit()
                                else:
                                        print("Pas de boucle perdante de taille : ", k, " | On augmente k")
                                        NotThisSize.append(k)
                                        k = k + 1
                                        continuer = False
                        else:
                                print("And(And(Ip), Not(I)) SAT")
                                I = Or(I, And(Ip))