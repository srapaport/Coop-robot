import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d 
import numpy as np
import pandas as pd

data = pd.read_csv('./data/data-phiSimple/data-timev2.csv', sep=';')

algov5 = data.loc[(data['algo'] == 5) & (data['error'] == 0)]
algov7 = data.loc[(data['algo'] == 7) & (data['error'] == 0)]
algov5err = data.loc[(data['algo'] == 5) & (data['error'] == 1)]
algov7err = data.loc[(data['algo'] == 7) & (data['error'] == 1)]

# fig = plt.figure()
# ax = fig.gca(projection='3d')
ax = plt.subplot(111, projection='3d')

ax.scatter(algov5['taille anneau'], algov5['nb robots'], algov5['time elapsed'], label='algo5', marker='d', color='yellow', linewidths=20)
ax.scatter(algov5err['taille anneau'], algov5err['nb robots'], algov5err['time elapsed'], label='algo5err', marker='d', color='orange', linewidths=20)
ax.scatter(algov7['taille anneau'], algov7['nb robots'], algov7['time elapsed'], label='algo7', marker='d', color='green', linewidths=10)
ax.scatter(algov7err['taille anneau'], algov7err['nb robots'], algov7err['time elapsed'], label='algo7err', marker='d', color='purple', linewidths=10)


plt.title("Elapsed time depending on ring size and robot number", fontsize=20)
ax.set_xlabel('Taille anneau', fontsize=20)
ax.set_ylabel('Nb Robots', fontsize=20)
ax.set_zlabel('Time', fontsize=20)
ax.legend(fontsize=20)
plt.tight_layout()
# plt.savefig('./data/graphe-time')
plt.show()