import algov5
import algov7
import sys

if len(sys.argv) < 4:
    """
    Control check on the number of arguments
    """
    print("Not enough arguments !")
    print("Usage : main.py <algorithm> <number of robots> <ring size>")
    exit()

"""
Control check on the type of the first argument
"""
try:
    algo = int(sys.argv[1])
except ValueError as v:
    print("First argument must be an integer <algorithm>\nTry 5 or 7")
    exit()

"""
Control check on the type of the second argument
"""
try:
    nb_robots = int(sys.argv[2])
except ValueError as v:
    print("Second argument must be an integer <number of robots>")
    exit()

"""
Control check on the type of the third argument
"""
try:
    taille_anneau = int(sys.argv[3])
except ValueError as v:
    print("Third argument must be an integer <ring size>")
    exit()

"""
Redirection toward the requested algorithm
"""
if algo == 5:
    algov5.mainv5(taille_anneau, nb_robots)
elif algo == 7:
    algov7.mainv7(taille_anneau, nb_robots)
else:
    print("Unknown algorithm, try 5 or 7")
    exit()