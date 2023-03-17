from z3 import *

def recur(prefix, suffix, res):
    if len(suffix) == 1:
        res.append(prefix + suffix)
        return 0
    else:
        for i in range(len(suffix)):
            newPrefix = prefix + [suffix[i]]
            suffixBis = suffix[:]
            del suffixBis[i]
            recur(newPrefix, suffixBis, res)

def equiRotation(p, s, t, p_prime, s_prime, t_prime, taille_anneau):
    tabAnd = []
    tabOr = []
    for size in range(taille_anneau):
        tabAndBis = []
        for i in range(len(p)):
            tabAndBis.append(p_prime[i] == (p[i]+size) % taille_anneau)
            tabAndBis.append(Or(And(s[i] != -1, s_prime[i] == (s[i]+size)%taille_anneau), And(s[i] == -1, s_prime[i] == -1)))
            tabAndBis.append(t_prime[i] == t[i])
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return And(tabAnd)

def equiMirror(p, s, t, p_prime, s_prime, t_prime, taille_anneau):
    tabAnd = []
    for i in range(len(p)):
        tabAnd.append(p_prime[i] == (taille_anneau - p[i]) % taille_anneau)
        tabAnd.append(t_prime[i] == t[i])
        tabAnd.append(Or(And(s[i] == -1, s_prime[i] == -1), And(s[i] != -1, s_prime[i] == (taille_anneau - s[i]) % taille_anneau)))
    return And(tabAnd)

def equiOrder(p, s, t, p_prime, s_prime, t_prime):
    tabAnd = []
    init = [i for i in range(len(p))]
    orders = []
    recur([], init, orders)
    tabOr = []
    for o in orders:
        tabAndBis = []
        for i in range(len(p)):
            tabAndBis.append(p_prime[i] == p[o[i]])
            tabAndBis.append(s_prime[i] == s[o[i]])
            tabAndBis.append(t_prime[i] == t[o[i]])
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return And(tabAnd)

def equiAll(p, s, t, p_prime, s_prime, t_prime, taille_anneau):
    tabAnd = []
    tabOr =[]
    prot = [ Int('prot%s' % (i)) for i in range(len(p)) ]
    srot = [ Int('srot%s' % (i)) for i in range(len(p)) ]
    trot = [ Int('trot%s' % (i)) for i in range(len(p)) ]
    tabOr.append(And(equiRotation(p, s, t, prot, srot, trot, taille_anneau), equiOrder(prot, srot, trot, p_prime, s_prime, t_prime)))

    pmir = [ Int('pmir%s' % (i)) for i in range(len(p)) ]
    smir = [ Int('smir%s' % (i)) for i in range(len(p)) ]
    tmir = [ Int('tmir%s' % (i)) for i in range(len(p)) ]
    tabOr.append(And(equiRotation(p, s, t, prot, srot, trot, taille_anneau), equiMirror(prot, srot, trot, pmir, smir, tmir, taille_anneau), equiOrder(pmir, smir, tmir, p_prime, s_prime, t_prime)))

    tabAnd.append(Or(tabOr))
    # return And(tabAnd)
    return Exists(prot, Exists(srot, Exists(trot, Exists(pmir, Exists(smir, Exists(tmir, And(tabAnd)))))))

# nb_robot = 4
# taille_anneau = 6

# p = [ Int('p%s' % (i)) for i in range(nb_robot) ]
# s = [ Int('s%s' % (i)) for i in range(nb_robot) ]
# t = [ Int('t%s' % (i)) for i in range(nb_robot) ]

# p_prime = [ Int('pp%s' % (i)) for i in range(nb_robot) ]
# s_prime = [ Int('sp%s' % (i)) for i in range(nb_robot) ]
# t_prime = [ Int('tp%s' % (i)) for i in range(nb_robot) ]

# sol = Solver()
# # sol.add(Init(p, s, t, taille_anneau))
# sol.add(And(p[0] == 0, p[1] == 2, p[2] == 2, p[3] == 5))
# sol.add(And(s[0] == 1, s[1] == -1, s[2] == -1, s[3] == 4))
# sol.add(And(t[0] == 1, t[1] == 0, t[2] == 0, t[3] == 1))

# sol.add(And(p_prime[0] == 1, p_prime[1] == 5, p_prime[2] == 2, p_prime[3] == 5))
# sol.add(And(s_prime[0] == 0, s_prime[1] == -1, s_prime[2] == 3, s_prime[3] == -1))
# sol.add(And(t_prime[0] == 1, t_prime[1] == 0, t_prime[2] == 1, t_prime[3] == 0))
# # sol.add(p_prime[0] != p[0])
# sol.add(equiAll(p, s, t, p_prime, s_prime, t_prime, taille_anneau))
# c = sol.check()
# print("solver : ", c)
# if c == sat:
#     print(sol.model().sexpr())