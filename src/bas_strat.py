from z3 import *
from math import factorial

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
# taille_anneau = 5       # Taille de l'anneau 
# nb_robots = 3           # Nombre de robot sur l'anneau
# robot_photo = 1         # Position du robot exécutant ConfigView

# distances = [ Int('d%s' % i) for i in range(nb_robots) ]
# p = [ Int('p%s' % i) for i in range(nb_robots) ]
# s = [ Int('s%s' % i) for i in range(nb_robots) ]
# t = [ Int('t%s' % i) for i in range(nb_robots) ]

# sol = Solver()

# tabInit = Init(p, s, t, taille_anneau)
# print("Init : \n", tabInit)
# tabTest = ConfigView(taille_anneau, nb_robots, robot_photo, p, distances)
# print("ConfigView : \n", tabTest)

# sol.add(tabInit)
# sol.add(tabTest)
# print("Solveur : \n", sol.check())
# if(sol.check() == sat):
#         print(sol.model()) # patch sans Exception sur ModelRef
#         # print(sol.model().sexpr()) # patch avec Exception sur ModelRef 

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

def InitSM(p, s, t, taille_anneau):
        tmpOr = []
        tmpAnd = []
        for i in range(len(p) - 1):
                tmpOr.append(p[i] != p[i+1])
        tmpAnd.append(Or(tmpOr)) # pas de configuration gagnante initialement
        tmpOr = []
        for i in range(len(s)):
                tmpAnd.append(p[i] >= 0)
                tmpAnd.append(p[i] < taille_anneau)
                tmpAnd.append(s[i] == -1)
                tmpAnd.append(t[i] == 0)
        
        for i in range(len(p)-1):
                tmpAndbis = []
                tmpAndbis.append(p[i] == p[i+1])
                tmpOrbis = []
                for j in range(len(p)):
                        if((j != i) and (j != (i+1))):
                                tmpOrbis.append(p[j] == p[i])
                                tmpAndter=[]
                                for h in range(len(p)):
                                        if h !=j:
                                                tmpAndter.append(p[h] != p[j])
                                tmpOrbis.append(And(tmpAndter))
                tmpAndbis.append(Or(tmpOrbis))
                tmpOr.append(And(tmpAndbis))
        tmpAnd.append(Or(tmpOr))
        return And(tmpAnd)

############################ TEST INIT ############################

# taille_anneau = 5       # Taille de l'anneau 
# nb_robots = 3           # Nombre de robot sur l'anneau
# s6 = Solver()

# p = [ Int('p%s' % i) for i in range(nb_robots) ]
# s = [ Int('s%s' % i) for i in range(nb_robots) ]
# t = [ Int('t%s' % i) for i in range(nb_robots) ]

# tabTest6 = InitSM(p, s, t, taille_anneau)
# print("tabTest6 :\n", tabTest6)

# s6.add(tabTest6)
# print(s6.check())
# if(s6.check() == sat):
#         print("model :\n",s6.model())

############################ TEST INIT FIN #########################

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