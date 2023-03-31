from z3 import *
from utilZ3v7 import *

def graph_size(ring_size, nb_robots):
        n = ring_size*4*2
        if nb_robots%2 == 0:
                disoriented = (factorial(n+(nb_robots//2)-1)//(factorial((nb_robots//2))*factorial(n-1)))*8
        else:
                disoriented = (factorial(n+((nb_robots-1)//2)-1)//(factorial(((nb_robots-1)//2))*factorial(n-1)))*8
        oriented = (factorial(n+(nb_robots-1)-1)//(factorial(nb_robots-1)*factorial(n-1))) - disoriented
        max_loop_size_old = (factorial(8 * ring_size + nb_robots -1)) // (factorial(nb_robots) * factorial(8 * ring_size - 1))
        print("ring_size = ", ring_size, " old = ", max_loop_size_old)
        return (oriented//2) + disoriented

def interpolant_test_results(maybeThisSize, Initialization, k, ring_size, nb_robots, p, s, t, pk, sk, tk, phi):
        if len(maybeThisSize) > 0:
                NotThisSizeBis = [i for i in range(k)]
                for elem in maybeThisSize:
                        NotThisSizeBis.remove(elem)
                tabAnd = []
                tabAnd.append(Initialization)
                tabAnd.append(AsyncPost(ring_size, nb_robots, p, s, t, pk[0], sk[0], tk[0], phi))
                for i in range(k-1):
                        print("Post %s" % (i+1))
                        tabAnd.append(AsyncPost(ring_size, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phi))
                tabAnd.append(BouclePerdante_v4(ring_size, p, s, t, pk, sk, tk, phi, NotThisSizeBis))
                solBis = Solver()
                solBis.add(And(tabAnd))
                if solBis.check() == sat:
                        print("Stratégie perdante, elem = ", elem,"\nk = ", k)
                        exit()
                else:
                        print("Pas de boucle perdante de taille : ", elem," pour k = ", k)

def build_context(context, k, ring_size, nb_robots, p, s, t, pk, sk, tk, phi, notThisSize):
        for i in range(k-1):
                print("Post %s" % (i+1))
                context.append(AsyncPost(ring_size, nb_robots, pk[i], sk[i], tk[i], pk[i+1], sk[i+1], tk[i+1], phi))
        context.append(BouclePerdante_v4(ring_size, p, s, t, pk, sk, tk, phi, notThisSize))

def build_interpolant(interpolant, context, keepGoing, maybeThisSize, firstInit, currentInit, k):
        try:
                Ip = tree_interpolant(And(Interpolant(And(interpolant)), And(context)))
                return Ip, keepGoing, k
        except ModelRef as m:
                if currentInit == firstInit:
                        print("Stratégie perdante\nk = ", k)
                        print(m.sexpr())
                        exit()
                maybeThisSize.append(k)
                print("On augmente k : ", k, "\n")
                return Ip, False, k + 1
        
def check_solver(currentInterpolant, currentInit, keepGoing, max_loop_size, notThisSize, k):
        if keepGoing:
                sol = Solver()
                sol.add(And(And(currentInterpolant), Not(currentInit)))
                
                if sol.check() != unsat:
                        print("And(And(Ip), Not(I)) SAT")
                        return Or(currentInit, And(currentInterpolant)), keepGoing, k
                
                print("And(And(Ip), Not(I)) UNSAT")
                if k == max_loop_size:
                        print("Stratégie gagnante\n")
                        exit()
                else:
                        print("Pas de boucle perdante de taille : ", k, " | On augmente k")
                        notThisSize.append(k)
                        return And(), False, k + 1
                        

def mainv7(ring_size, nb_robots, fun):
        phi = globals()[fun]
        max_loop_size = graph_size(ring_size, nb_robots)

        print("nb_robots = ", nb_robots)
        print("max_loop_size = ", max_loop_size)

        k = 1
        NotThisSize = [i for i in range(k)]
        MaybeThisSize = []

        p = [ Int('p%s' % i) for i in range(nb_robots) ]
        s = [ Int('s%s' % i) for i in range(nb_robots) ]
        t = [ Int('t%s' % i) for i in range(nb_robots) ]

        while True:

                I = Init(p, s, t, ring_size)

                constI = Init(p, s, t, ring_size)
                keepGoing = True

                pk = []
                sk = []
                tk = []
                for i in range(k):
                        pk.append([ Int('kp%s%s' % (i, j)) for j in range(nb_robots) ])
                        sk.append([ Int('ks%s%s' % (i, j)) for j in range(nb_robots) ])
                        tk.append([ Int('kt%s%s' % (i, j)) for j in range(nb_robots) ])

                while keepGoing:

                        interpolant_test_results(MaybeThisSize, I, k, ring_size, nb_robots, p, s, t, pk, sk, tk, phi)

                        print("boucle pour k = ", k)

                        # temporary arrays that will contain assertations
                        """
                        tmpAndInterpolant will contain all the assertations for the interpolant
                        tmpAndContext will contain all the assertions for the context
                        """
                        tmpAndInterpolant = []
                        tmpAndContext = []

                        # Init has to be true and is part of the interpolant
                        tmpAndInterpolant.append(I)
                        print("Post Init")
                        # The first AsyncPost has to be true and is part of the interpolant
                        tmpAndInterpolant.append(AsyncPost(ring_size, nb_robots, p, s, t, pk[0], sk[0], tk[0], phi))

                        build_context(tmpAndContext, k, ring_size, nb_robots, p, s, t, pk, sk, tk, phi, NotThisSize)

                        Ip, keepGoing, k = build_interpolant(tmpAndInterpolant, tmpAndContext, keepGoing, MaybeThisSize, I, constI, k)

                        I, keepGoing, k = check_solver(Ip, I, keepGoing, max_loop_size, NotThisSize, k)
