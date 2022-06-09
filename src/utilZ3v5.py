from z3 import *
from math import factorial
"""
soit p0, p1, ..., pk les positions des robots (le numéro de la place sur l'anneau (de 0 à taille de l'anneau -1))

pour une configuration d'un robot on a 
d0, d1, ..., dk la distance de chaque robot à son robot le plus proche dans le sens horaire

Dans l'exemple on se place sur un anneau de taille 5 avec 3 robots :

robot 1 r0 sur la position 1
robot 2 r1 sur la position 2
robot 3 r2 sur la position 3
les positions vacantes sont donc 4 et 0

Le robot r1 regarde les autres robots

On veut donc que ConfigView nous retourne les positions des robots, et
d0 = 1, d1 = 3 et d2 = 1
"""

# taille_anneau = 5       # Taille de l'anneau 
# nb_robots = 3           # Nombre de robot sur l'anneau
# robot_photo = 1         # Position du robot exécutant ConfigView

# distances = [ Int('d%s' % i) for i in range(nb_robots) ]
# list_positions = [ Int('p%s' % i) for i in range(nb_robots) ]

def Init(p, s, t, taille_anneau):
        tmpOr = []
        tmpAnd = []
        for i in range(len(p) - 1):
                tmpOr.append(p[i] != p[i+1])
        tmpAnd.append(Or(tmpOr))
        for i in range(len(s)):
                tmpAnd.append(p[i] >= 0)
                tmpAnd.append(p[i] < taille_anneau)
                tmpAnd.append(s[i] == -1)
                tmpAnd.append(t[i] == 0)
        return And(tmpAnd)


############################ TEST INIT ############################

# taille_anneau = 5       # Taille de l'anneau 
# nb_robots = 3           # Nombre de robot sur l'anneau
# s6 = Solver()

# p = [ Int('p%s' % i) for i in range(nb_robots) ]
# s = [ Int('s%s' % i) for i in range(nb_robots) ]
# t = [ Int('t%s' % i) for i in range(nb_robots) ]

# tabTest6 = Init(p, s, t, taille_anneau)

# s6.add(tabTest6)
# print(s6.check())
# if(s6.check() == sat):
#         print(s6.model().sexpr())

############################ TEST INIT FIN #########################

def ConfigView(taille_anneau, nb_robots, indice_robot, list_positions, distances):
        
        distances_prime = [ Int('dp%s' % i) for i in range(len(distances) - 1) ]
        
        tabAnd = []
        
        # Ligne 1 ConfigView
        # On classe le vecteur de distance temporaire par ordre croissant
        for l in range(len(distances_prime) - 1):
                tabAnd.append(distances_prime[l] <= distances_prime[l+1])

        # Sur la ligne 2 et la ligne 3 on ajoute les assertions permettant d'avoir les
        # distances du robot qui appelle la fonction aux autres robots
        # Ligne 2 ConfigView
        tmpOr = []
        for i in range(len(list_positions)):
                tmpOr = []
                if i != indice_robot:
                        for l in range(len(distances_prime)):
                                tmpOr.append( list_positions[i] ==
                                ( list_positions[indice_robot] + distances_prime[l] ) % taille_anneau )
                        tabAnd.append(Or(tmpOr))

        # Ligne 3 ConfigView
        for l in range(len(distances_prime)):
                tmpOr = []
                for i in range(len(list_positions)):
                        if i != indice_robot:
                                tmpOr.append( list_positions[i] ==
                                ( list_positions[indice_robot] + distances_prime[l] ) % taille_anneau )
                tabAnd.append(Or(tmpOr))

        # Ligne 4 ConfigView
        # On s'assure que d0 est plus grand que 0
        # et que tous les d sont inférieurs à la taille de l'anneau
        tabAnd.append(0 < distances_prime[0])
        for l in range(len(distances_prime)):
                tabAnd.append(distances_prime[l] <= taille_anneau)

        # Ligne 5 ConfigView
        # Construction des distances calculées
        # On fait la soustraction entre les distances pour avoir les distances relatives
        # entre chaque voisin
        tabAnd.append(distances[0] == distances_prime[0])
        for l in range(1, len(distances_prime)):
                tabAnd.append(distances[l] == (distances_prime[l] - distances_prime[l-1]))
        tabAnd.append(distances[-1] == (taille_anneau - distances_prime[-1]))
        
        return Exists(distances_prime, And(tabAnd))

############################ TEST CONFIGVIEW ############################
taille_anneau = 5       # Taille de l'anneau 
nb_robots = 3           # Nombre de robot sur l'anneau
robot_photo = 1         # Position du robot exécutant ConfigView

distances = [ Int('d%s' % i) for i in range(nb_robots) ]
p = [ Int('p%s' % i) for i in range(nb_robots) ]
s = [ Int('s%s' % i) for i in range(nb_robots) ]
t = [ Int('t%s' % i) for i in range(nb_robots) ]

sol = Solver()

tabInit = Init(p, s, t, taille_anneau)
print("Init : \n", tabInit)
tabTest = ConfigView(taille_anneau, nb_robots, robot_photo, p, distances)
print("ConfigView : \n", tabTest)

sol.add(tabInit)
sol.add(tabTest)
print("Solveur : \n", sol.check())
if(sol.check() == sat):
        print(sol.model().sexpr())

############################ TEST CONFIGVIEW FIN #########################

def ViewSym(taille_anneau, nb_robots, distances, distances_prime):

        tabAnd = []

        tabAnd.append(distances[0] != 0)
        tabAnd.append(distances_prime[0] != 0)

        tmpAddition = Sum([i for i in distances])
        tabAnd.append(tmpAddition == taille_anneau)

        tmpAddition = Sum([i for i in distances_prime])
        tabAnd.append(tmpAddition == taille_anneau)

        ######## Ajout suite au résultat ci-dessous
        for i in range(len(distances)):
                tabAnd.append(distances[i] > 0)
                tabAnd.append(distances_prime[i] > 0)
        ########
        
        tmpOr = []
        tmpAnd = []

        for j in range(len(distances)):
                tmpAnd = []
                for l in range(j+1, len(distances)):
                        tmpAnd.append(And(distances[l] == 0, distances_prime[l] == 0))
                for l in range(j+1):
                        tmpAnd.append(distances_prime[l] == distances[j-l])
                tmpOr.append(And(tmpAnd))
        tabAnd.append(Or(tmpOr))

        return And(tabAnd)

############################ TEST VIEWSYM ############################

############################ TEST VIEWSYM FIN #########################

# def phi(distances):
#         """
#         Le robot se déplace vers le robot le plus proche, si les robots sont à équidistances
#         alors le robot reste sur place
#         """

#         ## Pas sûr que cela fonctionne
#         tabAnd = []
#         tabOr = []
#         for i in range(1, len(distances)):
#                 tabOr.append(distances[i] != 0) # Pour ne pas bouger si la tour est construite
#         tabAnd.append(Or(tabOr))
#         tabAnd.append(distances[0] < distances[-1])

#         return And(tabAnd)

def phi(distances):
        """
        Le robot se déplace vers le robot le plus proche, si les robots sont à équidistances
        alors le robot reste sur place
        """
        tabAnd = []
        tabOr = []
        for i in range(1, len(distances)):
                tabOr.append(distances[i] != 0) # Pour ne pas bouger si la tour est construite
        tabAnd.append(Or(tabOr))
        #tabAnd.append(Or(distances[0] < distances[-1], distances[0] == distances[-1]))
        tabAnd.append(distances[0] < distances[-1])

        return And(tabAnd)

# def phi(distances):
#         return False

def Move(taille_anneau, nb_robots, indice_robot, list_positions, pp, phi):
        distances = [ Int('d%s' % i) for i in range(nb_robots) ]
        distances_prime = [ Int('dp%s' % i) for i in range(nb_robots) ]
        
        tabAnd = []
        
        # Appel de ConfigView           ## Ligne 2 Move
        tmp = ConfigView(taille_anneau, nb_robots, indice_robot, list_positions, distances)
        tabAnd.append(tmp)

        # Appel de ViewSym              ## Ligne 3 Move
        tmp = ViewSym(taille_anneau, nb_robots, distances, distances_prime)
        tabAnd.append(tmp)
        tmpOr = []

        tmpPhi1 = phi(distances)
        tmpOr.append(And(tmpPhi1, Or( And( list_positions[indice_robot] < (taille_anneau -1), pp == (list_positions[indice_robot] + 1)), And( list_positions[indice_robot] == (taille_anneau - 1), pp == 0))))

        tmpPhi2 = phi(distances_prime)
        tmpOr.append(And(tmpPhi2, Or( And( list_positions[indice_robot] > 0, pp == (list_positions[indice_robot] - 1)), And( list_positions[indice_robot] == 0, pp == (taille_anneau - 1)))))

        tmpOr.append(And(Not(tmpPhi1), Not(tmpPhi2), pp == list_positions[indice_robot]))

        tabAnd.append(Or(tmpOr))

        return Exists(distances, Exists(distances_prime, And(tabAnd)))

############################ TEST MOVE ############################

# s3 = Solver()

# pp = Int('sp1')

# tabTest3 = Move(taille_anneau, nb_robots, 1, list_positions, pp, phi)
# #print(tabTest3)

# s3.add(tabTest3)
# print(s3.check())
# if(s3.check() == sat):
#         print(s3.model())

"""
"""

############################ TEST MOVE FIN #########################

def AsyncPost(taille_anneau, nb_robots, p, s, t, p_prime, s_prime, t_prime, phi):
        
        tabAnd = []
        tmpOr_i1k = []
        
        ######## Ajout assertions pour encadrer p s et t
        for i in range(len(p)):
                tabAnd.append(And(p[i] < taille_anneau, p[i] >= 0))
                tabAnd.append(Or(s[i] == -1, And(s[i] >= 0, s[i] < taille_anneau)))
                tabAnd.append(Or(t[i] == 0, t[i] == 1))
        ########

        for i in range(nb_robots):
                tmpAnd = []
                tmpOr = []
                for j in range(nb_robots):
                        if j != i:
                                # Ligne 1 AsyncPost
                                tmpAnd.append(And(p_prime[j] == p[j], s_prime[j] == s[j]))
                # Ligne 2 AsyncPost
                tmpOr.append(And(s[i] == -1, Move(taille_anneau, nb_robots, i, p, s_prime[i], phi), p_prime[i] == p[i]))
                # Ligne 3 AsyncPost
                tmpOr.append(And(s[i] != -1, p_prime[i] == s[i], s_prime[i] == -1))
                tmpAnd.append(Or(tmpOr))

                tmpAndBis = []
                tmpOr = []

                for j in range(nb_robots):
                        if j != i:
                                tmpAndBis.append(t[j] == 1)
                for j in range(nb_robots):
                        tmpAndBis.append(t_prime[j] == 0)
                # Ligne 4 AsyncPost avant le V (ou)
                tmpOr.append(And(tmpAndBis)) 

                tmpAndBis = []
                tmpOrBis = []

                for j in range(nb_robots):
                        if j != i:
                                tmpOrBis.append(t[j] == 0)
                tmpAndBis.append(Or(tmpOrBis))
                tmpAndBis.append(t_prime[i] == 1)
                for j in range(nb_robots):
                        if j != i:
                                tmpAndBis.append(t_prime[j] == t[j])
                tmpOr.append(And(tmpAndBis))
                tmpAnd.append(Or(tmpOr))
                tmpOr_i1k.append(And(tmpAnd))
        tabAnd.append(Or(tmpOr_i1k))
        return And(tabAnd)

############################ TEST ASYNCPOST ############################

# taille_anneau = 5       # Taille de l'anneau 
# nb_robots = 3           # Nombre de robot sur l'anneau
# robot_photo = 1         # Position du robot exécutant ConfigView

# distances = [ Int('d%s' % i) for i in range(nb_robots) ]
# list_positions = [ Int('p%s' % i) for i in range(nb_robots) ]

# p = [ Int('p%s' % i) for i in range(nb_robots) ]
# s = [ Int('s%s' % i) for i in range(nb_robots) ]
# t = [ Int('t%s' % i) for i in range(nb_robots) ]
# p_prime = [ Int('pp%s' % i) for i in range(nb_robots) ]
# s_prime = [ Int('sp%s' % i) for i in range(nb_robots) ]
# t_prime = [ Int('tp%s' % i) for i in range(nb_robots) ]
# s4 = Solver()

# #tabTest4 = AsyncPost(taille_anneau, nb_robots, p, s, t, p_prime, s_prime, t_prime, phi)
# #print(tabTest4)
# s4.add(Init(p, s, t))
# s4.add(AsyncPost(taille_anneau, nb_robots, p, s, t, p_prime, s_prime, t_prime, phi))
# print(s4.check())
# if(s4.check() == sat):
#         print(s4.model())

"""
[tp2 = 0,
 p1 = 2,
 p0 = 0,
 sp2 = -1,
 tp1 = 0,
 tp0 = 1,
 p2 = 3,
 sp1 = -1,
 sp0 = 0,
 pp0 = 0,
 pp2 = 3,
 pp1 = 2,
 t2 = 0,
 s2 = -1,
 t1 = 0,
 s1 = -1,
 t0 = 0,
 s0 = -1]

C0:
p0: 0   s0: -1  t0: 0
p1: 2   s1: -1  t1: 0
p2: 3   s2: -1  t2: 0

C1:

"""

"""
sat
[pp0 = 1,
s1 = -1,
p1 = 4,
sp2 = -1,
t2 = 1,
s2 = -1,
t1 = 0,
pp2 = 3,
p0 = 1,
s0 = -1,
tp0 = 0,
sp0 = -1,
tp1 = 0,
tp2 = 0,
pp1 = 4,
t0 = 1,
p2 = 3,
sp1 = 0]

c0 : 
        p0 = 1          s0 = -1         t0 = 1
        p1 = 4          s1 = -1         t1 = 0
        p2 = 3          s2 = -1         t2 = 1
c1 :
        pp0 = 1         sp0 = -1        tp0 = 0
        pp1 = 4         sp1 = 0         tp1 = 0
        pp2 = 3         sp2 = -1        tp2 = 0

"""

############################ TEST ASYNCPOST FIN #########################

def BouclePerdante(taille_anneau, pk, sk, tk, taille_boucle, phi):
        #taille_boucle = 10
        #TODO
        ## On fixe les tailles des tableaux pour enlever les append
        ## On stocke toutes les tailles de boucle perdante et on les test dans l'interpolant
        ## On Test les configurations symétriques pour limiter les tailles de boucles perdantes
        #TODO
        #mainTmpOr = [[] for i in range(300)]
        mainTmpOr = []
        cp = [None] * taille_boucle
        cs = [None] * taille_boucle
        ct = [None] * taille_boucle
        for i in range(taille_boucle):
                cp[i] = [ Int('p%s%s' % (i, j)) for j in range(len(pk)) ]
                cs[i] = [ Int('s%s%s' % (i, j)) for j in range(len(sk)) ]
                ct[i] = [ Int('t%s%s' % (i, j)) for j in range(len(tk)) ]
        
        for x in range(taille_boucle):
                print("Construction de la boucle de taille : ", x)
        
                tmpAnd = []
                tmpAndbis = []
                tmpOr = []
                tmpOrbis = []

                tmpAnd.append(AsyncPost(taille_anneau, len(pk), pk, sk, tk, cp[0], cs[0], ct[0], phi))
                for i in range(x - 1):
                        tmpAnd.append(AsyncPost(taille_anneau, len(pk), cp[i], cs[i], ct[i], cp[i+1], cs[i+1], ct[i+1], phi))
                tmpAnd.append(AsyncPost(taille_anneau, len(pk), cp[-1], cs[-1], ct[-1], pk, sk, tk, phi))
                ############################
                for j in range(len(pk) - 1):
                        tmpOr.append(pk[j] != pk[j+1]) # On vérifie qu'aucune des configurations de transition n'est une configuration gagnante
                tmpAnd.append(Or(tmpOr))

                for i in range(x):
                        tmpOr = []
                        for j in range(len(pk) - 1):
                                tmpOr.append(cp[i][j] != cp[i][j+1]) # On vérifie qu'aucune des configurations de transition n'est une configuration gagnante
                        tmpAnd.append(Or(tmpOr))
                ############ Partie avec aucune config gagnante longue mais ok

                for j in range(len(pk)):
                        tmpAndbis.append(tk[j] == 0) # On vérifie qu'au moins une configuration a tous ces t à 0
                tmpOrbis.append(And(tmpAndbis))

                for i in range(x):
                        tmpAndbis = []
                        for j in range(len(pk)):
                                tmpAndbis.append(ct[i][j] == 0) # On vérifie qu'au moins une configuration a tous ces t à 0
                        tmpOrbis.append(And(tmpAndbis))
                
                tmpAnd.append(Or(tmpOrbis))
                ############ Partie avec une config avec tous les t à 0
                ###########################
                mainTmpOr.append(And(tmpAnd))
        #return And(Or(mainTmpOr))
        return Exists([cp[i][j] for i in range(taille_boucle) for j in range(len(pk))], Exists([cs[i][j] for i in range(taille_boucle) for j in range(len(pk))], Exists([ct[i][j] for i in range(taille_boucle) for j in range(len(pk))], And(Or(mainTmpOr)))))

############################ TEST BOUCLEPERDANTE ############################

# taille_anneau = 4      # Taille de l'anneau 
# nb_robots = 2           # Nombre de robot sur l'anneau

# s5 = Solver()

# p = [ Int('p%s' % i) for i in range(nb_robots) ]
# s = [ Int('s%s' % i) for i in range(nb_robots) ]
# t = [ Int('t%s' % i) for i in range(nb_robots) ]


# # print(tabTest5)
# # s5.add(And(p[0] == 0, p[1] == 2, p[2] == 3))
# # s5.add(Init(p, s, t))
# tabTest5 = BouclePerdante(taille_anneau, p, s, t, phi)
# s5.add(tabTest5)
# print(s5.check())
# if(s5.check() == sat): # sat pour taille_boucle = 1
#         print(s5.model().sexpr())

############################ TEST BOUCLEPERDANTE FIN #########################



"""
taille_anneau = 5
nb_robot = 3

Nombre de configurations possibles pour 1 robot :
taille_anneau x 4 x 2

Pour avoir la taille du graphe on regarde la taille de l'ensemble comprenant les combinaisons
de configurations possibles avec remise

On selectionne nb_robot configurations parmi (taille_anneau x 4 x 2) configurations

(8 x taille_anneau + nb_robot - 1) !
--------------------------------------
nb_robot ! x (8 x taille_anneau - 1) !

Avec notre configuration on a :
11 480

"""