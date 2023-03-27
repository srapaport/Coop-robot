import sys
import re
import numpy as np

args = sys.argv

if len(args) != 5:
    print("usage : python3 visualization.py <log_file> <ring_size> <nb_robots> <loop_size>")
    exit(1)

PATH = args[1]
ring_size = int(args[2])
nb_robots = int(args[3])
loop_size = int(args[4])

def clean_log(path):
    regex_file_name = r"^.*/([^/]+)$"
    matches_file_name = re.findall(regex_file_name, path)
    new_file_name = 'clean_' + matches_file_name[0]

    new_log = open(new_file_name, 'w')

    with open(path, 'r') as f:
        logs = f.read()

    regex = r"define-fun ([^! ]+) \(\) Int\n  \(?([ \-\d]+)\]?\)"
    matches = re.findall(regex, logs)

    # Display the extracted values
    for match in matches:
        variable = match[0]
        value = match[1].replace(' ', '')
        #print(f"{variable} = {value}")
        new_log.write(f"{variable} = {value}\n")
    new_log.close()

def arrays_initialization(path, nb_robots):
    with open(path, 'r') as f:
        lines = f.readlines()

    # Initialiser les tableaux p, s et t
    p = np.zeros((loop_size, nb_robots), int)
    s = np.zeros((loop_size, nb_robots), int)
    t = np.zeros((loop_size, nb_robots), int)

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
    return p, s, t

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

clean_log(PATH)
p, s, t = arrays_initialization(PATH, nb_robots)
for nb_configs in range(loop_size):
	config_visualization(ring_size, p[nb_configs], s[nb_configs], t[nb_configs])
	print("\n")