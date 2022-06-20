from z3 import *
from utilZ3v5 import *

taille_anneau = 5
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
        taille_boucle = 0
        satisfiable = False

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
                print("Boucle pour k = %s\n" % k)
                tmpAndInterpolant = []
                tmpAndContext = []

                tabAnd = []

                tmpAndInterpolant.append(I)
                tabAnd.append(I)
                tmp = AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSM)
                tmpAndInterpolant.append(tmp)
                tabAnd.append(tmp)

                if k > 1:
                        for i in range(1, k):
                                print("Pass Post before %s" % i)
                                tmp = AsyncPost(taille_anneau, nb_robots, pk[i-1], sk[i-1], tk[i-1], pk[i], sk[i], tk[i], phiSM)
                                tmpAndContext.append(tmp)
                                tabAnd.append(tmp)
                                print("Pass Post after %s" % i)

                while (not satisfiable) or (taille_boucle < taille_boucle_max):
                        tmpAndContextBis_v1 = []
                        tmpAndContextBis_v2 = []
                        taille_boucle = taille_boucle + 1
                        tmpAndContextBis_v1.append(BouclePerdante(taille_anneau, pk[-1], sk[-1], tk[-1], taille_boucle, phiSM))
                        tmpAndContext.append(And(tmpAndContextBis_v1))
                        tmpAndContextBis_v2.append(BouclePerdante_v2(taille_anneau, pk[-1], sk[-1], tk[-1], taille_boucle, phiSM))
                        tabAnd.append(And(tmpAndContextBis_v2))
                        print("Test pour taille_boucle = ", taille_boucle)
                        solvBP = Solver()
                        solvBP.add(And(tabAnd))
                        checkSolvBP = solvBP.check()
                        if checkSolvBP != sat:
                                print("BouclePerdante est unsat pour taille_boucle = ", taille_boucle)
                                if taille_boucle < taille_boucle_max:
                                        del tmpAndContext[-1]
                                        del tabAnd[-1]
                                else:
                                        try:
                                                Ip = tree_interpolant(And(Interpolant(And(tmpAndInterpolant)), And(tmpAndContext)))
                                                print("Interpolant est unsat pour taille_boucle = ", taille_boucle)
                                                solvImplies = Solver()
                                                solvImplies.add(Implies(And(Ip), I))
                                                if solvImplies.check() == sat:
                                                        print("Stratégie gagnante\n")
                                                        exit()
                                                else:
                                                        I = Or(I, And(Ip))
                                        except ModelRef as m:
                                                print("Interpolant est satisfiable --> Boucle perdante pour taille_boucle = ", taille_boucle)
                                                print("Ne devrait pas arriver")
                                                exit()
                        else:
                                print("BouclePerdante est satisfiable --> ", taille_boucle)
                                satisfiable = True
                                if I == constI:
                                        print("Stratégie perdante")
                                        #print(solvBP.model().sexpr())
                                        exit()
                                else:
                                        k = k + 1
                                        continuer = False
################
"""
Note :

algov3 l59 --> Renvoie unsat alors que dans utilZ3v3 renvoie sat pour taille_anneau = 4, nb_robot = 2

Boucle perdante --> trop long de créer les taille_boucle boucle et de les concaténer dans un Or

"""