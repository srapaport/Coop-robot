from z3 import *
from utilZ3v5 import *
from itertools import *

def AllView(distances, allDistances):
    tabAnd = []
    for i in range(len(distances)):
        for j in range(len(distances)):
            tabAnd.append(allDistances[i][j] == distances[(j+i)%len(distances)])
    return And(tabAnd)

def IsRigid(taille_anneau, distances):
    ad = []
    vs = []
    for i in range(len(distances)):
        ad.append([ Int('ird%s%s' % (i,j)) for j in range(len(distances)) ])
        vs.append([ Int('irds%s%s' % (i,j)) for j in range(len(distances)) ])
    tabAnd = []
    tabAnd.append(AllView(distances, ad))
    for i in range(len(distances)):
        tabAnd.append(ViewSym(taille_anneau, ad[i], vs[i]))
    for i in range(len(distances)):
        for j in range(len(distances)):
            tabAnd.append(ad[i][j] != 0)
    for i in range(len(distances)):
        for l in range(len(distances)):
            if l != i:
                tmpOr1 = []
                tmpOr2 = []
                tmpOr3 = []
                tmpOr4 = []
                for j in range(len(distances)):
                    tmpOr1.append(ad[i][j] != ad [l][j])
                    tmpOr2.append(ad[i][j] != vs[l][j])
                    tmpOr3.append(vs[i][j] != ad[l][j])
                    tmpOr4.append(vs[i][j] != vs[l][j])
                tabAnd.append(And(Or(tmpOr1), Or(tmpOr2), Or(tmpOr3), Or(tmpOr4)))
    #return And(tabAnd)
    return Exists([ad[i][j] for i in range(len(distances)) for j in range(len(distances))], Exists([vs[i][j] for i in range(len(distances)) for j in range(len(distances))], And(tabAnd)))

###################### Rigid configuration
# taille_anneau = 12
# distance = [ Int('d%s' % (i)) for i in range(5) ]
# tmpInit = []
# tmpInit.append(And(distance[0] == 3, distance[1] == 3, distance[2] ==  2, distance[3] == 1, distance[4] == 3))
# tab = IsRigid(taille_anneau, distance)
# s = Solver()
# s.add(And(tmpInit))
# s.add(tab)
# c = s.check()
# print("solver : ", c)
# # if c == sat:
# #     print(s.model().sexpr())
######################

def recur(prefix, tab, res):
    if len(tab) == 1:
        res.append(prefix + tab)
        return 0
    else:
        for i in range(len(tab)):
            tmp = prefix + [tab[i]]
            tabBis = []
            for j in range(len(tab)):
                tabBis.append(tab[j])
            del tabBis[i]
            recur(tmp, tabBis, res)

def CodeMaker(taille_anneau, distances, codes, codesSym):
    tabAnd = []
    tabAnd.append(IsRigid(taille_anneau, distances))
    ad = []
    vs = []
    for i in range(len(distances)):
        ad.append([ Int('cmd%s%s' % (i,j)) for j in range(len(distances)) ])
        vs.append([ Int('cmds%s%s' % (i,j)) for j in range(len(distances)) ])
    tabAnd = []
    tabAnd.append(AllView(distances, ad))
    for i in range(len(distances)):
        tabAnd.append(ViewSym(taille_anneau, ad[i], vs[i]))

    dico = dict()
    for i in range(2*len(codes)):
        if i < len(codes):
            dico[codes[i]] = ad[i]
        else:
            dico[codesSym[i-len(codes)]] = vs[i-len(codes)]

    combi = []
    recur([], codes+codesSym, combi)

    tabOr = []
    for o in combi:
        tabAndBis = []
        for i in range(len(o)-1):
            tabAndBis.append(o[i] > o[i+1])
            tabOrBis = []
            for p in range(len(distances)):
                tabAndTer = []
                for q in range(p):
                    tabAndTer.append(dico.get(o[i])[q] == dico.get(o[i+1])[q])
                tabAndTer.append(dico.get(o[i])[p] > dico.get(o[i+1])[p])
                tabOrBis.append(And(tabAndTer))
            tabAndBis.append(Or(tabOrBis))
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    #return And(tabAnd)
    return Exists([ad[i][j] for i in range(len(distances)) for j in range(len(distances))], Exists([vs[i][j] for i in range(len(distances)) for j in range(len(distances))], And(tabAnd)))

###################### CodeMaker
# taille_anneau = 6
# distance = [ Int('d%s' % (i)) for i in range(3) ]
# codes = [ Int('a%s' % (i)) for i in range(3) ]
# codesSym = [ Int('as%s' % (i)) for i in range(3) ]
# p = [ Int('p%s' % (i)) for i in range(3) ]
# s = [ Int('s%s' % (i)) for i in range(3) ]
# t = [ Int('t%s' % (i)) for i in range(3) ]
# tab0 = Init(p, s, t, taille_anneau)
# tab1 = ConfigView(taille_anneau, 3, 0, p, distance)
# tab2 = IsRigid(taille_anneau, distance)
# tab3 = CodeMaker(taille_anneau, distance, codes, codesSym)
# s = Solver()
# s.add(tab0)
# s.add(tab1)
# s.add(tab2)
# s.add(tab3)
# c = s.check()
# print("solver : ", c)
# if c == sat:
#     print(s.model().sexpr())
######################

def FindMax(distances, Max):
    tabAnd = []
    for i in range(len(distances)):
        tabAnd.append(Max >= distances[i])
    tabOr = []
    for i in range(len(distances)):
        tabOr.append(Max == distances[i])
    tabAnd.append(Or(tabOr))
    return And(tabAnd)

###################### FindMax
# taille_anneau = 6
# distance = [ Int('d%s' % (i)) for i in range(3) ]
# codes = [ Int('a%s' % (i)) for i in range(3) ]
# codesSym = [ Int('as%s' % (i)) for i in range(3) ]
# p = [ Int('p%s' % (i)) for i in range(3) ]
# s = [ Int('s%s' % (i)) for i in range(3) ]
# t = [ Int('t%s' % (i)) for i in range(3) ]
# tab0 = Init(p, s, t, taille_anneau)
# tab1 = ConfigView(taille_anneau, 3, 0, p, distance)
# tab2 = IsRigid(taille_anneau, distance)
# max = Int('Max')
# tab3 = FindMax(distance, max)
# s = Solver()
# s.add(tab0)
# s.add(tab1)
# s.add(tab2)
# s.add(tab3)
# c = s.check()
# print("solver : ", c)
# if c == sat:
#     print(s.model().sexpr())
######################

def FindM(ad, vs, codes, codesSym, Max, M):
    dico = dict()
    for i in range(2*len(codes)):
        if i < len(codes):
            dico[codes[i]] = ad[i]
        else:
            dico[codesSym[i-len(codes)]] = vs[i-len(codes)]
    
    tabAnd = []
    for i in range(len(ad)):
        tabAnd.append(Or(ad[i][0] == Max, ad[i][-1] == Max))
    return And(tabAnd)

distance = [ Int('d%s' % (i)) for i in range(3) ]
ad = []
vs = []
for i in range(len(distance)):
    ad.append([ Int('cmd%s%s' % (i,j)) for j in range(len(distance)) ])
    vs.append([ Int('cmds%s%s' % (i,j)) for j in range(len(distance)) ])
max = Int('Max')
m = Int('M')
tab0 = FindM(ad, vs, [], [], max, m)