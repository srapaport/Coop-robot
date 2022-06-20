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
    return And(tabAnd)
    #return Exists(ad, Exists(vs, And(tabAnd)))

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
# if c == sat:
#     s.model().sexpr()
######################

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
    tabOr = []
    tabAndBis = []
    for x in range(2*len(distances)):
        for y in range(2*len(distances)):
            if x != y:
                if x < len(distances):
                    if y < len(distances):
                        tabAndBis.append(codes[x] > codes[y])
                    else:
                        tabAndBis.append(codes[x] > codesSym[y-len(distances)])
                else:
                    if y < len(distances):
                        tabAndBis.append(codesSym[x-len(distances)] > codes[y])
                    else:
                        tabAndBis.append(codesSym[x-len(distances)] > codesSym[y-len(distances)])
                tabOrBis = []
                for p in range(len(distances)):
                    tabAndTer = []
                    for q in range(p):
                        if x < len(distances):
                            if y < len(distances):
                                tabAndTer.append(ad[x][q] == ad[y][q])
                            else:
                                tabAndTer.append(ad[x][q] == vs[y-len(distances)][q])
                        else:
                            if y < len(distances):
                                tabAndTer.append(vs[x-len(distances)][q] == ad[y][q])
                            else:
                                tabAndTer.append(vs[x-len(distances)][q] == vs[y-len(distances)][q])
                    if x < len(distances):
                        if y < len(distances):
                            tabAndTer.append(ad[x][p] == ad[y][p])
                        else:
                            tabAndTer.append(ad[x][p] == vs[y-len(distances)][p])
                    else:
                        if y < len(distances):
                            tabAndTer.append(vs[x-len(distances)][p] == ad[y][p])
                        else:
                            tabAndTer.append(vs[x-len(distances)][p] == vs[y-len(distances)][p])
                    tabOrBis.append(And(tabAndTer))
                tabAndBis.append(Or(tabOrBis))
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return And(tabAnd)
                





# taille_anneau = 12
# distance = [ Int('d%s' % (i)) for i in range(5) ]
# codes = [ Int('a%s' % (i)) for i in range(5) ]
# codesSym = [ Int('as%s' % (i)) for i in range(5) ]
# tab = CodeMaker(taille_anneau, distance, codes, codesSym)

tab1 = ['a0', 'a1', 'a2', 'a3']
tab2 = ([ Int('A%s' % (j)) for j in range(4) ])
def recur(prefix, tab):
    if len(tab) == 1:
        print(prefix + tab)
        return 0
    else:
        for i in range(len(tab)):
            # print("i = ", i,"\ntab = ", tab)
            tmp = prefix + [tab[i]]
            tabBis = []
            for j in range(len(tab)):
                tabBis.append(tab[j])
            del tabBis[i]
            # print("tab après del tabBis : ", tab)
            # print("tmp = ", tmp," | tabBis = ", tabBis)
            recur(tmp, tabBis)
recur([], tab2)

# tmp = (combinations(tab, len(tab)))
# for i in list(tmp):
#     print(i)
