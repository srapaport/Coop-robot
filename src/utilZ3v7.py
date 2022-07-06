from z3 import *
from rigid_util import phiR
from odd_util import phiON
from math import factorial

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


def InitSM(p, s, t, taille_anneau):
        """
        Initialise la configuration passée en paramètre
        La configuration comportera une multiplicité et ne sera pas gagnante
        """
        tmpOr = []
        tmpAnd = []
        for i in range(len(p)):
                tmpOr.append(p[i] != p[(i+1)%len(p)])
        tmpAnd.append(Or(tmpOr)) # pas de configuration gagnante initialement
        tmpOr = []
        for i in range(len(s)):
                tmpAnd.append(p[i] >= 0)
                tmpAnd.append(p[i] < taille_anneau)
                tmpAnd.append(s[i] == -1)
                tmpAnd.append(t[i] == 0)
        
        for i in range(len(p)):
                tmpAndbis = []
                tmpAndbis.append(p[i] == p[(i+1)%len(p)])
                tmpOrbis = []
                for j in range(len(p)):
                        if((j != i) and (j != ((i+1)%len(p)))):
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

def AllView(distances, allDistances):
    tabAnd = []
    for i in range(len(distances)):
        for j in range(len(distances)):
            tabAnd.append(allDistances[i][j] == distances[(j+i)%len(distances)])
    return And(tabAnd)

def InitRigid(p, s, t, taille_anneau):
        """
        Initialise la configuration passée en paramètre
        La configuration sera rigide
        """
        tabAnd = []
        for i in range(len(p)):
                tabAnd.append(p[i] != p[(i+1)%len(p)])
                tabAnd.append(And(p[i] >= 0, p[i] < taille_anneau))
                tabAnd.append(s[i] == -1)
                tabAnd.append(t[i] == 0)
        dist = [ Int('IRd%s' % i) for i in range(len(p))]
        tabAnd.append(ConfigView(taille_anneau, len(p), 0, p, dist))
        ad = []
        vs = []
        for i in range(len(p)):
                ad.append([ Int('IRad%s%s' % (i,j)) for j in range(len(p)) ])
                vs.append([ Int('IRvs%s%s' % (i,j)) for j in range(len(p)) ])
        tabAnd.append(AllView(dist, ad))
        for i in range(len(p)):
                tabAnd.append(ViewSym(taille_anneau, ad[i], vs[i]))
        for i in range(len(ad)):
                for j in range(len(ad[i])):
                        tabAnd.append(ad[i][j] != 0)
        for i in range(len(ad)):
                for l in range(len(ad)):
                        if l != i:
                                tmpOr1 = []
                                tmpOr2 = []
                                tmpOr3 = []
                                tmpOr4 = []
                                for j in range(len(ad[i])):
                                        tmpOr1.append(ad[i][j] != ad [l][j])
                                        tmpOr2.append(ad[i][j] != vs[l][j])
                                        tmpOr3.append(vs[i][j] != ad[l][j])
                                        tmpOr4.append(vs[i][j] != vs[l][j])
                                tabAnd.append(And(Or(tmpOr1), Or(tmpOr2), Or(tmpOr3), Or(tmpOr4)))
        # return And(tabAnd)
        return Exists(dist,
                Exists([ad[i][j] for i in range(len(p)) for j in range(len(p))],
                Exists([vs[i][j] for i in range(len(p)) for j in range(len(p))], And(tabAnd))))

def ConfigView(taille_anneau, nb_robots, indice_robot, list_positions, distances):
        
        distances_prime = [ Int('cvdp%s' % i) for i in range(len(distances) - 1) ]
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

def ViewSym(taille_anneau, distances, distances_prime):

        tabAnd = []

        tabAnd.append(distances[0] != 0)
        tabAnd.append(distances_prime[0] != 0)
        tmpAddition = Sum([i for i in distances])
        tabAnd.append(tmpAddition == taille_anneau)

        tmpAddition = Sum([i for i in distances_prime])
        tabAnd.append(tmpAddition == taille_anneau)

        ######## Ajout suite au résultat ci-dessous
        for i in range(len(distances)):
                tabAnd.append(And(distances[i] >= 0, distances[i] <= taille_anneau))
                tabAnd.append(And(distances_prime[i] >= 0, distances_prime[i] <= taille_anneau))
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

def phiSimple(taille_anneau, distances):
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

def phiSM(taille_anneau, distances):
        """
        Strategie est vrai s'il n'y a qu'une seule multiplicité, 
        le robot se déplace vers cette dernière
        """
        tabAnd = []
        tabOr = []
        for i in range(len(distances)):
                tabAndBis = []
                tabAndBis.append(distances[i] == 0)
                for j in range(len(distances)):
                        if j != i:
                                tabAndBis.append(Or(distances[j] > 0, And(distances[j] == 0, distances[j-1] == 0)))
                tabOr.append(And(tabAndBis))
        tabAnd.append(Or(tabOr))
        tabAnd.append(distances[-1] != 0)
        tabOr = []
        tabOr.append(And(distances[1] == 0, distances[-2] == 0, distances[0] <= distances[-1]))
        tabOr.append(And(distances[1] == 0, distances[-2] != 0))
        tabAnd.append(Or(tabOr))
        return And(tabAnd)

def phiUltime(taille_anneau, distances):
        return And(Or(phiSM(taille_anneau, distances), phiR(taille_anneau, distances), phiON(taille_anneau, distances)))

def Move(taille_anneau, nb_robots, indice_robot, list_positions, pp, phi):
        distances = [ Int('md%s' % i) for i in range(nb_robots) ]
        distances_prime = [ Int('mdp%s' % i) for i in range(nb_robots) ]
        
        tabAnd = []
        
        # Appel de ConfigView           ## Ligne 2 Move
        tmp = ConfigView(taille_anneau, nb_robots, indice_robot, list_positions, distances)
        tabAnd.append(tmp)

        # Appel de ViewSym              ## Ligne 3 Move
        tmp = ViewSym(taille_anneau, distances, distances_prime)
        tabAnd.append(tmp)
        tmpOr = []

        tmpPhi1 = phi(taille_anneau, distances)
        tmpOr.append(And(tmpPhi1, Or( And( list_positions[indice_robot] < (taille_anneau - 1), pp == (list_positions[indice_robot] + 1)), And( list_positions[indice_robot] == (taille_anneau - 1), pp == 0))))

        tmpPhi2 = phi(taille_anneau, distances_prime)
        tmpOr.append(And(tmpPhi2, Or( And( list_positions[indice_robot] > 0, pp == (list_positions[indice_robot] - 1)), And( list_positions[indice_robot] == 0, pp == (taille_anneau - 1)))))

        tmpOr.append(And(Not(tmpPhi1), Not(tmpPhi2), pp == list_positions[indice_robot]))

        tabAnd.append(Or(tmpOr))
        #return And(tabAnd)
        return Exists(distances, Exists(distances_prime, And(tabAnd)))

def AsyncPost(taille_anneau, nb_robots, p, s, t, p_prime, s_prime, t_prime, function_phi):
        
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
                tmpOr.append(And(s[i] == -1, Move(taille_anneau, nb_robots, i, p, s_prime[i], function_phi), p_prime[i] == p[i]))
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

def BouclePerdante_v3(taille_anneau, p_init, s_init, t_init, pk, sk, tk, function_phi):

        print("Construction BouclePerdante, len(pk) = ", len(pk))
        tabAnd = []
        tabOrPost = []
        print("OU")
        print("Post de ", pk[-1], " à ", p_init)
        tabOrPost.append(AsyncPost(taille_anneau, len(pk[0]), pk[-1], sk[-1], tk[-1], p_init, s_init, t_init, function_phi))
        for i in range(len(pk)):
                tabOrPost.append(AsyncPost(taille_anneau, len(pk[0]), pk[-1], sk[-1], tk[-1], pk[i], sk[i], tk[i], function_phi))
                print("Post de ", pk[-1], " à ", pk[i])
        tabAnd.append(Or(tabOrPost))
        print("FIN OU")
        ############################
        for i in range(len(pk)):
                tmpOr = []
                for j in range(len(pk[i])):
                        tmpOr.append(pk[i][j] != pk[i][(j+1)%len(pk[0])]) # On vérifie qu'aucune des configurations de transition n'est une configuration gagnante
                tabAnd.append(Or(tmpOr))

        tmpOr = []
        for i in range(len(pk)):
                tmpAnd = []
                for j in range(len(pk[i])):
                        tmpAnd.append(tk[i][j] == 0) # On vérifie qu'au moins une configuration a tous ces t à 0
                tmpOr.append(And(tmpAnd))
        tabAnd.append(Or(tmpOr))
        return And(tabAnd)

def BouclePerdante_v4(taille_anneau, p_init, s_init, t_init, pk, sk, tk, function_phi, NotThisSize):
        
        print("Construction BouclePerdante, len(pk) = ", len(pk))
        tabAnd = []
        tabOrPost = []
        print("DEBUT OU")
        print("Post de ", pk[-1], " à ", p_init)
        tabOrPost.append(AsyncPost(taille_anneau, len(pk[0]), pk[-1], sk[-1], tk[-1], p_init, s_init, t_init, function_phi))
        for i in range(len(pk) - 1):
                taille_boucle = len(pk) - (i+1)
                if taille_boucle in NotThisSize:
                        print("On ne cherche pas de boucle de taille : ", taille_boucle)
                else:
                        tabOrPost.append(AsyncPost(taille_anneau, len(pk[0]), pk[-1], sk[-1], tk[-1], pk[i], sk[i], tk[i], function_phi))
                        print("Post de ", pk[-1], " à ", pk[i])
        tabAnd.append(Or(tabOrPost))
        print("FIN OU")
        ############################
        for i in range(len(pk)):
                tmpOr = []
                for j in range(len(pk[i])):
                        tmpOr.append(pk[i][j] != pk[i][(j+1)%len(pk[0])]) # On vérifie qu'aucune des configurations de transition n'est une configuration gagnante
                tabAnd.append(Or(tmpOr))

        tmpOr = []
        for i in range(len(pk)):
                tmpAnd = []
                for j in range(len(pk[i])):
                        tmpAnd.append(tk[i][j] == 0) # On vérifie qu'au moins une configuration a tous ces t à 0
                tmpOr.append(And(tmpAnd))
        tabAnd.append(Or(tmpOr))
        return And(tabAnd)

