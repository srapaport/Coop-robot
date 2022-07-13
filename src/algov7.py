from z3 import *
from utilZ3v7 import *
import sys
from timeout_after import *

if len(sys.argv) < 4:
        print("Pas assez d'argument")
        exit()

def main():

        taille_anneau = int(sys.argv[1])
        nb_robots = int(sys.argv[2])
        to = int(sys.argv[3])

        taille_boucle_max = (factorial(8 * taille_anneau + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * taille_anneau - 1))
        print("taille_anneau = ", taille_anneau)
        print("nb_robots = ", nb_robots)
        print("taille_boucle_max = ", taille_boucle_max)

        k = (2*nb_robots) - 1 # On considère qu'initialement tous les s sont à -1 et tous les t à 0
        #k = 1
        NotThisSize = [i for i in range(k)]
        MaybeThisSize = []

        p = [ Int('p%s' % i) for i in range(nb_robots) ]
        s = [ Int('s%s' % i) for i in range(nb_robots) ]
        t = [ Int('t%s' % i) for i in range(nb_robots) ]
        try:
                with TimeoutAfter(timeout=to, exception=TimeoutError):
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
                                                tabAnd.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiON))
                                                for i in range(k-1):
                                                        print("Post %s" % (i+1))
                                                        tabAnd.append(AsyncPost(taille_anneau, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiON))
                                                tabAnd.append(BouclePerdante_v4(taille_anneau, p, s, t, pk, sk, tk, phiON, NotThisSizeBis))
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
                                        tmpAndInterpolant.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiON))
                                        for i in range(k-1):
                                                print("Post %s" % (i+1))
                                                tmpAndContext.append(AsyncPost(taille_anneau, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phiON))
                                        tmpAndContext.append(BouclePerdante_v4(taille_anneau, p, s, t, pk, sk, tk, phiON, NotThisSize))
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
        except TimeoutError:
                print("Timeout reached ! --> ", to)
                exit()

thr = threading.Thread(target = main)
thr.start()
thr.join()
"""
                Erreur pour InitSM + phiON avec taille anneau 3 et nb robot 3

Traceback (most recent call last):
  File "algov7.py", line 69, in <module>
    Ip = tree_interpolant(And(Interpolant(And(tmpAndInterpolant)), And(tmpAndContext)))
  File "/usr/lib/python3.8/site-packages/z3/z3.py", line 8297, in tree_interpolant
    res = Z3_compute_interpolant(ctx.ref(),f.as_ast(),p.params,ptr,mptr)
  File "/usr/lib/python3.8/site-packages/z3/z3core.py", line 4074, in Z3_compute_interpolant
    _elems.Check(a0)
  File "/usr/lib/python3.8/site-packages/z3/z3core.py", line 1336, in Check
    raise self.Exception(self.get_error_message(ctx, err))
z3.z3types.Z3Exception: b'interpolation failure'

"""