import algov5
import algov7
import algov7_v2
import sys

if len(sys.argv) != 5:
    """
    Control check on the number of arguments
    """
    print("Not enough arguments !")
    print("Usage : python3 main.py <algorithm> <number of robots> <ring size>")
    exit(1)

"""
Control check on the type of the first argument
"""
try:
    algo = int(sys.argv[1])
except ValueError as v:
    print("First argument must be an integer <algorithm>\nTry 5 or 7")
    exit(1)

"""
Control check on the type of the second argument
"""
try:
    nb_robots = int(sys.argv[2])
except ValueError as v:
    print("Second argument must be an integer <number of robots>")
    exit(1)

"""
Control check on the type of the third argument
"""
try:
    taille_anneau = int(sys.argv[3])
except ValueError as v:
    print("Third argument must be an integer <ring size>")
    exit(1)

"""
Redirection toward the requested algorithm
"""
if algo == 5:
    algov5.mainv5(taille_anneau, nb_robots)
elif algo == 7:
    algov7.mainv7(taille_anneau, nb_robots)
elif algo == 8:
    algov7_v2.mainv7(taille_anneau, nb_robots, sys.argv[4])
else:
    print("Unknown algorithm, try 5 or 7")
    exit(1)