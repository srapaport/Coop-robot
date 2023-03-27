import numpy as np
import re

PATH = '/home/solal/Documents/Stage_lip6/Coop-robot/test/new_log.txt'
nb_loop = 6
nb_robots = 3
# Ouvrir le fichier de log
with open(PATH, 'r') as f:
	lines = f.readlines()

# Initialiser les tableaux p, s et t
p = np.zeros((nb_loop, nb_robots), int)
s = np.zeros((nb_loop, nb_robots), int)
t = np.zeros((nb_loop, nb_robots), int)

# Parcourir les lignes du fichier
for line in lines:
	name, value = line.strip().split(' = ')
	var_type, index = name[1], name[2:]
	if len(index) > 1:
		i, j = int(index[0]), int(index[1])
	if var_type == 'p':
		p[i+1][j] = int(value)
	elif var_type == 's':
		s[i+1][j] = int(value)
	elif var_type == 't':
		t[i+1][j] = int(value)
	elif len(re.findall(r"^[pst]", name)) > 0:
		matches = re.findall(r"^([pst])([0-9]) = (.*)$", line)
		if matches[0][0] == 'p':
			p[0][int(matches[0][1])] = int(matches[0][2])
		elif matches[0][0] == 's':
			s[0][int(matches[0][1])] = int(matches[0][2])
		elif matches[0][0] == 't':
			t[0][int(matches[0][1])] = int(matches[0][2])


# Afficher les tableaux
print('p =', p)
print('s =', s)
print('t =', t)
