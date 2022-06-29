from z3 import *
from utilZ3v5 import *
from itertools import *

def AllView(distances, allDistances):
    tabAnd = []
    for i in range(len(distances)):
        for j in range(len(distances)):
            tabAnd.append(allDistances[i][j] == distances[(j+i)%len(distances)])
    return And(tabAnd)

def IsRigid(ad, vs):
    tabAnd = []
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
    #return And(tabAnd)
    return Exists([ad[i][j] for i in range(len(ad)) for j in range(len(ad[0]))], Exists([vs[i][j] for i in range(len(vs)) for j in range(len(vs[0]))], And(tabAnd)))

###################### Rigid configuration
# taille_anneau = 12
# distance = [ Int('d%s' % (i)) for i in range(5) ]
# tmpInit = []
# tmpInit.append(And(distance[0] == 3, distance[1] == 3, distance[2] ==  3, distance[3] == 2, distance[4] == 1))
# s = Solver()
# ad = []
# vs = []
# for i in range(len(distance)):
#     ad.append([ Int('ird%s%s' % (i,j)) for j in range(len(distance)) ])
#     vs.append([ Int('irds%s%s' % (i,j)) for j in range(len(distance)) ])
# s.add(AllView(distance, ad))
# for i in range(len(distance)):
#     s.add(ViewSym(taille_anneau, ad[i], vs[i]))

# tab = IsRigid(ad, vs)

# s.add(And(tmpInit))
# s.add(tab)
# c = s.check()
# print("solver : ", c)
# if c == sat:
#     print(s.model().sexpr())
######################

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

def AllCode(allDistances, allDistancesSym, alphas, betas, alphas_prime, betas_prime):
    tabAnd = []
    for i in range(len(alphas)):
        tabAnd.append(And(alphas_prime[i] < betas_prime[i], Or(alphas_prime[i] == alphas[i], alphas_prime[i] == betas[i]), Or(betas_prime[i] == alphas[i], betas_prime[i] == betas[i])))
        tabAnd.append(And(alphas[i] > 0, alphas_prime[i] > 0, betas[i] > 0, betas_prime[i] > 0, alphas[i] <= (2*len(alphas)), betas[i] <= (2*len(alphas)), alphas_prime[i] <= (2*len(alphas)), betas_prime[i] <= (2*len(alphas))))
    
    dico = dict()
    for i in range(2*len(alphas)):
        if i < len(alphas):
            dico[alphas[i]] = allDistances[i]
        else:
            dico[betas[i-len(alphas)]] = allDistancesSym[i-len(alphas)]
    
    combi = []
    recur([], alphas + betas, combi)

    tabOr = []
    for o in combi:
        tabAndBis = []
        for i in range(len(o)-1):
            tabAndBis.append(o[i] < o[i+1])
            tabOrBis = []
            for p in range(len(alphas)):
                tabAndTer = []
                for q in range(p):
                    tabAndTer.append(dico.get(o[i])[q] == dico.get(o[i+1])[q])
                tabAndTer.append(dico.get(o[i])[p] > dico.get(o[i+1])[p])
                tabOrBis.append(And(tabAndTer))
            tabAndBis.append(Or(tabOrBis))
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))

    return And(tabAnd)

def CodeMaker(ad, vs, codes):
    tabAnd = []
    tabAnd.append(IsRigid(ad, vs))

    alphas = [ Int('alpha%s' % (j)) for j in range(len(ad)) ]
    betas = [ Int('beta%s' % (j)) for j in range(len(ad)) ]
    alphas_p = [ Int('alpha_prime%s' % (j)) for j in range(len(ad)) ]
    betas_p = [ Int('beta_prime%s' % (j)) for j in range(len(ad)) ]
    tabAnd.append(AllCode(ad, vs, alphas, betas, alphas_p, betas_p))
    for i in range(len(ad)):
        tabAnd.append(And(codes[i] > 0, codes[i] <= len(codes)))
        for j in range(len(ad)):
            if i != j:
                tabAnd.append(Or(And(codes[i] > codes[j], alphas_p[j] > alphas_p[i]), And(codes[i] < codes[j], alphas_p[j] < alphas_p[i])))
                tabAnd.append(codes[i] != codes[j])
    #return And(tabAnd)
    return Exists(alphas, Exists(betas, Exists(alphas_p, Exists(betas_p,
        And(tabAnd)))))

###################### CodeMaker
# taille_anneau = 6
# distance = [ Int('d%s' % (i)) for i in range(3) ]
# codes = [ Int('a%s' % (i)) for i in range(3) ]
# p = [ Int('p%s' % (i)) for i in range(3) ]
# s = [ Int('s%s' % (i)) for i in range(3) ]
# t = [ Int('t%s' % (i)) for i in range(3) ]

# sol = Solver()
# ad = []
# vs = []
# for i in range(len(distance)):
#     ad.append([ Int('ird%s%s' % (i,j)) for j in range(len(distance)) ])
#     vs.append([ Int('irds%s%s' % (i,j)) for j in range(len(distance)) ])
# sol.add(AllView(distance, ad))
# for i in range(len(distance)):
#     sol.add(ViewSym(taille_anneau, ad[i], vs[i]))

# tab0 = Init(p, s, t, taille_anneau)
# tab1 = ConfigView(taille_anneau, 3, 0, p, distance)
# tab3 = CodeMaker(ad, vs, codes)

# sol.add(tab0)
# sol.add(tab1)
# sol.add(tab3)
# c = sol.check()
# print("solver : ", c)
# if c == sat:
#     print(sol.model().sexpr())
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

# p = [ Int('p%s' % (i)) for i in range(3) ]
# s = [ Int('s%s' % (i)) for i in range(3) ]
# t = [ Int('t%s' % (i)) for i in range(3) ]

# sol = Solver()
# ad = []
# vs = []
# for i in range(len(distance)):
#     ad.append([ Int('ird%s%s' % (i,j)) for j in range(len(distance)) ])
#     vs.append([ Int('irds%s%s' % (i,j)) for j in range(len(distance)) ])
# sol.add(AllView(distance, ad))
# for i in range(len(distance)):
#     sol.add(ViewSym(taille_anneau, ad[i], vs[i]))

# tab0 = Init(p, s, t, taille_anneau)
# tab1 = ConfigView(taille_anneau, 3, 0, p, distance)
# tab2 = IsRigid(ad, vs)
# max = Int('Max')
# tab3 = FindMax(distance, max)

# sol.add(tab0)
# sol.add(tab1)
# sol.add(tab2)
# sol.add(tab3)
# c = sol.check()
# print("solver : ", c)
# if c == sat:
#     print(sol.model().sexpr())
######################

def FindM(ad, codes, Max, M):
    tabAnd = []
    tabOr = []
    for i in range(len(ad)):
        tabAndBis = []
        for j in range(len(ad)):
            tabAndBis.append(Or(And(codes[i] >= codes[j], Or(ad[j][0] == Max, ad[j][-1] == Max)), And(ad[j][0] < Max, ad[j][-1] < Max)))
        tabAndBis.append(M == i)
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return And(tabAnd)

###################### FindM
# taille_anneau = 6
# nb_robot = 3
# distance = [ Int('d%s' % (i)) for i in range(nb_robot) ]
# codes = [ Int('a%s' % (i)) for i in range(nb_robot) ]

# p = [ Int('p%s' % (i)) for i in range(nb_robot) ]
# s = [ Int('s%s' % (i)) for i in range(nb_robot) ]
# t = [ Int('t%s' % (i)) for i in range(nb_robot) ]

# tab0 = Init(p, s, t, taille_anneau)
# tab1 = ConfigView(taille_anneau, nb_robot, 0, p, distance)
# print("ok1")
# sol = Solver()
# ad = []
# vs = []
# for i in range(len(distance)):
#     ad.append([ Int('testd%s%s' % (i,j)) for j in range(len(distance)) ])
#     vs.append([ Int('testds%s%s' % (i,j)) for j in range(len(distance)) ])
# sol.add(AllView(distance, ad))
# for i in range(len(distance)):
#     sol.add(ViewSym(taille_anneau, ad[i], vs[i]))
# print("ok2")
# max = Int('Max')
# tab3 = FindMax(distance, max)
# print("CA VA")
# tab2 = CodeMaker(ad, vs, codes)
# print("C est chaud")
# m = Int('M')
# tab4 = FindM(ad, codes, max, m)
# print("on va check")
# sol.add(tab0)
# sol.add(tab1)
# sol.add(tab2)
# sol.add(tab3)
# sol.add(tab4)
# c = sol.check()
# print("solver : ", c)
# if c == sat:
#     print(sol.model().sexpr())
######################

def FindN(ad, codes, Max, M, N):
    tabAnd = []
    tabOrN = []
    tabOrN.append(And(ad[M][0] == Max, ad[M][-1] == Max,
        Or(And(N == (M+1)%len(codes), codes[(M+1)%len(codes)] > codes[(M-1)%len(codes)] ),
            And(N == (M-1)%len(codes), codes[(M-1)%len(codes)] > codes[(M+1)%len(codes)] ) )) )
    tabOrN.append(And(ad[M][0] == Max, ad[M][-1] != Max, N == (M+1)%len(codes)))
    tabOrN.append(And(ad[M][0] != Max, ad[M][-1] == Max, N == (M-1)%len(codes)))
    tabAnd.append(Or(tabOrN))
    return And(tabAnd)

def FindMN(ad, codes, Max, M, N):
    tabAnd = []
    tabOr = []
    for i in range(len(ad)):
        tabAndBis = []
        for j in range(len(ad)):
            tabAndBis.append(Or(And(codes[i] >= codes[j], Or(ad[j][0] == Max, ad[j][-1] == Max)), And(ad[j][0] < Max, ad[j][-1] < Max)))
        tabAndBis.append(M == i)
        tabOrN = []
        tabOrN.append(And(ad[i][0] == Max, ad[i][-1] == Max,
            Or(And(N == (i+1)%len(codes), codes[(i+1)%len(codes)] > codes[(i-1)%len(codes)] ),
                And(N == (i-1)%len(codes), codes[(i-1)%len(codes)] > codes[(i+1)%len(codes)] ) )) )
        tabOrN.append(And(ad[i][0] == Max, ad[i][-1] != Max, N == (i+1)%len(codes)))
        tabOrN.append(And(ad[i][0] != Max, ad[i][-1] == Max, N == (i-1)%len(codes)))
        tabAndBis.append(Or(tabOrN))
        tabOr.append(And(tabAndBis))
    tabAnd.append(Or(tabOr))
    return And(tabAnd)

###################### FindN
taille_anneau = 7
nb_robot = 4
distance = [ Int('d%s' % (i)) for i in range(nb_robot) ]
codes = [ Int('a%s' % (i)) for i in range(nb_robot) ]

p = [ Int('p%s' % (i)) for i in range(nb_robot) ]
s = [ Int('s%s' % (i)) for i in range(nb_robot) ]
t = [ Int('t%s' % (i)) for i in range(nb_robot) ]

tab0 = Init(p, s, t, taille_anneau)
tab1 = ConfigView(taille_anneau, nb_robot, 0, p, distance)
print("ok1")
sol = Solver()
ad = []
vs = []
for i in range(len(distance)):
    ad.append([ Int('testd%s%s' % (i,j)) for j in range(len(distance)) ])
    vs.append([ Int('testds%s%s' % (i,j)) for j in range(len(distance)) ])
sol.add(AllView(distance, ad))
for i in range(len(distance)):
    sol.add(ViewSym(taille_anneau, ad[i], vs[i]))
print("ok2")
max = Int('Max')
tab3 = FindMax(distance, max)
print("CA VA")
tab2 = CodeMaker(ad, vs, codes)
print("C est chaud")
m = Int('M')
n = Int('N')
tab4 = FindMN(ad, codes, max, m, n)
print("on va check")
sol.add(tab0)
sol.add(tab1)
sol.add(tab2)
sol.add(tab3)
sol.add(tab4)
c = sol.check()
print("solver : ", c)
if c == sat:
    print(sol.model().sexpr())
######################