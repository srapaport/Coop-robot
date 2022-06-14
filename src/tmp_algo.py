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

        I = InitSM(p, s, t, taille_anneau)

        constI = InitSM(p, s, t, taille_anneau)
        continuer = True
        pk = []
        sk = []
        tk = []
        for i in range(k):
                pk.append([ Int('fp%s%s' % (i, j)) for j in range(nb_robots) ])
                sk.append([ Int('fs%s%s' % (i, j)) for j in range(nb_robots) ])
                tk.append([ Int('ft%s%s' % (i, j)) for j in range(nb_robots) ])

        while continuer:
                print("boucle pour k = %s\n" % k)
                tmpAndInterpolant = []
                tmpAndContext = []
                ########### Pas d'interpolant !!!!
                tmpAndInterpolant.append(I)
                tmpAndInterpolant.append(AsyncPost(taille_anneau, nb_robots, p, s, t, pk[0], sk[0], tk[0], phiSM))
                while (not satisfiable) or (taille_boucle < taille_boucle_max):
                        tmpAndContextBis = []
                        taille_boucle = taille_boucle + 1
                        tmpAndContextBis.append(BouclePerdante(taille_anneau, pk[-1], sk[-1], tk[-1], taille_boucle, phiSM))
                        tmpAndContext.append(And(tmpAndContextBis))
                        print("Test pour taille_boucle = ", taille_boucle)
                        sol = Solver()
                        sol.add(And(tmpAndInterpolant))
                        sol.add(And(tmpAndContext))
                        if sol.check() != sat:
                                print("Solver est unsat pour taille_boucle = ", taille_boucle)
                                if taille_boucle < taille_boucle_max:
                                        print("On augmente taille_boucle\nTaille tmpAndContext --> ", len(tmpAndContext))
                                        del tmpAndContext[-1] # On retire tmpAndContextBis
                                        sol = Solver()
                        else:
                                print("Solver est satisfiable --> Boucle perdante pour taille_boucle = ", taille_boucle)
                                satisfiable = True
                                if I == constI:
                                        print("Stratégie perdante\nk = ", k, " | taille_boucle = ", taille_boucle)
                                        exit()
                                k = k + 1
                                continuer = False
                
                print("Stratégie gagnante\n")
                exit()
################
"""
Note :

algov3 l59 --> Renvoie unsat alors que dans utilZ3v3 renvoie sat pour taille_anneau = 4, nb_robot = 2

Boucle perdante --> trop long de créer les taille_boucle boucle et de les concaténer dans un Or

"""