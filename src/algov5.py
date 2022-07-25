from z3 import *
from utilZ3v7 import *

def mainv5(taille_anneau, nb_robots):
        taille_boucle_max = (factorial(8 * taille_anneau + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * taille_anneau - 1))
        print("taille_anneau = ", taille_anneau)
        print("nb_robots = ", nb_robots)
        print("taille_boucle_max = ", taille_boucle_max)

        k = 1

        p = [ Int('p%s' % i) for i in range(nb_robots) ]
        s = [ Int('s%s' % i) for i in range(nb_robots) ]
        t = [ Int('t%s' % i) for i in range(nb_robots) ]
        while True:
                taille_boucle = (2*nb_robots) - 2
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
                        print("boucle pour k = %s\n" % k)
                        tmpAndInterpolant = []
                        tmpAndContext = []

                        tmpAndInterpolant.append(I)
                        tmpAndInterpolant.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiUltimate))

                        if k > 1:
                                for i in range(1, k):
                                        print("Pass before %s" % i)
                                        tmpAndContext.append(AsyncPost(taille_anneau, nb_robots, pk[i-1], sk[i-1], tk[i-1], pk[i], sk[i], tk[i], phiUltimate))
                                        print("Pass after %s" % i)

                        while (not satisfiable) or (taille_boucle < taille_boucle_max):
                                # tmpAndContextBis = []
                                taille_boucle = taille_boucle + 1
                                # tmpAndContextBis.append(BouclePerdante_v5(taille_anneau, pk[-1], sk[-1], tk[-1], taille_boucle, phiUltimate))
                                #tmpAndContext.append(And(tmpAndContextBis))
                                #print("tmpAndContext : ", tmpAndContext)
                                #print("tmpAndInterpolant : ",tmpAndInterpolant)
                                print("Test pour taille_boucle = ", taille_boucle)
                                try:
                                        if len(tmpAndContext) == 0:
                                                Ip = tree_interpolant(And(Interpolant(And(tmpAndInterpolant)), BouclePerdante_v5(taille_anneau, pk[-1], sk[-1], tk[-1], taille_boucle, phiUltimate)))
                                        else:
                                                Ip = tree_interpolant(And(Interpolant(And(tmpAndInterpolant)), And(tmpAndContext, BouclePerdante_v5(taille_anneau, pk[-1], sk[-1], tk[-1], taille_boucle, phiUltimate))))
                                        print("Unsat pour taille_boucle = ", taille_boucle)
                                except ModelRef as m:
                                        print("Sat --> Boucle perdante pour taille_boucle = ", taille_boucle)
                                        satisfiable = True
                                        if I == constI:
                                                print("Stratégie perdante\nk = ", k, " | taille_boucle = ", taille_boucle)
                                                print(m.sexpr())
                                                exit()
                                        k = k + 1
                                        continuer = False
                        sol = Solver()
                        sol.add(And(And(Ip), Not(I)))
                        if sol.check() == unsat:
                                print("Stratégie gagnante\n")
                                exit()
                        else:
                                I = Or(I, Ip)