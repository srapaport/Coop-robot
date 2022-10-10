from z3 import *
from utilZ3v7 import *

def mainv7(loop_size, nb_robots):
        """
        Calcul of the size of the graph
        """
        n = loop_size*4*2
        if nb_robots%2 == 0:
                disoriented = (factorial(n+(nb_robots//2)-1)//(factorial((nb_robots//2))*factorial(n-1)))*8
        else:
                disoriented = (factorial(n+((nb_robots-1)//2)-1)//(factorial(((nb_robots-1)//2))*factorial(n-1)))*8
        oriented = (factorial(n+(nb_robots-1)-1)//(factorial(nb_robots-1)*factorial(n-1))) - disoriented
        max_loop_size_old = (factorial(8 * loop_size + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * loop_size - 1))
        max_loop_size = (oriented//2) + disoriented
        print("loop_size = ", loop_size, " old = ", max_loop_size_old)

        print("nb_robots = ", nb_robots)
        print("max_loop_size = ", max_loop_size)
        #########################################################################################################################
        """
        k is //TODO
        """
        k = 1
        NotThisSize = [i for i in range(k)]
        MaybeThisSize = []

        p = [ Int('p%s' % i) for i in range(nb_robots) ]
        s = [ Int('s%s' % i) for i in range(nb_robots) ]
        t = [ Int('t%s' % i) for i in range(nb_robots) ]
        while True:

                I = Init(p, s, t, loop_size)

                constI = Init(p, s, t, loop_size)
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
                                tabAnd.append(AsyncPost(loop_size, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSimple))
                                for i in range(k-1):
                                        print("Post %s" % (i+1))
                                        tabAnd.append(AsyncPost(loop_size, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiSimple))
                                tabAnd.append(BouclePerdante_v4_1(loop_size, p, s, t, pk, sk, tk, phiSimple, NotThisSizeBis))
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
                        tmpAndInterpolant.append(AsyncPost(loop_size, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSimple))
                        for i in range(k-1):
                                print("Post %s" % (i+1))
                                tmpAndContext.append(AsyncPost(loop_size, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiSimple))
                        tmpAndContext.append(BouclePerdante_v4_1(loop_size, p, s, t, pk, sk, tk, phiSimple, NotThisSize))
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
                                        if k == max_loop_size:
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
