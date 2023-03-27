import numpy as np
import re

PATH = '/home/solal/Documents/Stage_lip6/Coop-robot/test/clean_log_algov7_6_3.txt'
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


ring_size = 6

# Vérification de la taille de l'anneau et du nombre de robots
nb_robots = len(p[0])
assert nb_robots == len(s[0]) == len(t[0]), "Les tableaux p, s et t doivent avoir la même taille"
assert all(0 <= position < ring_size for position in p[0]), "Les positions doivent être des entiers compris entre 0 et la taille de l'anneau - 1"

# Affichage de la configuration
def config_visualization(ring_size, p, s, t):
	for i in range(nb_robots):
		position = p[i]
		direction = s[i]
		bit_equite = t[i]

		# Création de la chaîne de caractères représentant la configuration
		config_str = " " * ring_size
		config_str = config_str[:position] + str(i) + config_str[position+1:]
		if direction != -1:
			if direction > position:
				arrow_char = ">"
			elif direction < position:
				arrow_char = "<"
			else:
				arrow_char = "="
			#arrow_char = ">" if direction > position else "<"
			arrow_pos = direction if direction > position else direction + ring_size
			config_str = config_str[:arrow_pos] + arrow_char + config_str[arrow_pos+1:]

		# Affichage de la configuration
		print(f"Configuration du robot {i} : {config_str} \t(bit d'équité={bit_equite})")

for nb_configs in range(len(p)-1):
	config_visualization(ring_size, p[nb_configs], s[nb_configs], t[nb_configs])
	print("\n")