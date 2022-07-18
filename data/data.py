import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d 
import numpy as np
import pandas as pd

data = pd.read_csv('./data/data-phiR24/data-timev2.csv', sep=';')


algov5 = data.loc[(data['algo'] == 5) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov7 = data.loc[(data['algo'] == 7) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]

algov5r2 = data.loc[(data['algo'] == 5) & (data['nb robots'] == 2) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov5r3 = data.loc[(data['algo'] == 5) & (data['nb robots'] == 3) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov5r4 = data.loc[(data['algo'] == 5) & (data['nb robots'] == 4) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov5r5 = data.loc[(data['algo'] == 5) & (data['nb robots'] == 5) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]

algov7r2 = data.loc[(data['algo'] == 7) & (data['nb robots'] == 2) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov7r3 = data.loc[(data['algo'] == 7) & (data['nb robots'] == 3) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov7r4 = data.loc[(data['algo'] == 7) & (data['nb robots'] == 4) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]
algov7r5 = data.loc[(data['algo'] == 7) & (data['nb robots'] == 5) & ((data['error'] == 0) | (data['error'] == 3) | (data['error'] == 2))]

######################## 2D

fig, ax = plt.subplots()
ax.plot(algov5r5.sort_values(by = 'taille anneau')['taille anneau'], algov5r5.sort_values(by = 'taille anneau')['time elapsed'], color='blue', label='algov5r5')
ax.plot(algov7r5.sort_values(by = 'taille anneau')['taille anneau'], algov7r5.sort_values(by = 'taille anneau')['time elapsed'], color='red', label='algov7r5')

ax.set(xlabel='taille anneau', ylabel='time elapsed', title='Time elapsed per size of the ring for 5 robots')
ax.grid()
ax.legend()
fig.savefig("./data/data-phiR24/compar_phiR24_5.png")
plt.show()

######################## 3D

# algov5err = data.loc[(data['algo'] == 5) & ((data['error'] == 0) | (data['error'] == 3))]
# algov7err = data.loc[(data['algo'] == 7) & ((data['error'] == 0) | (data['error'] == 3))]

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
# ax = plt.subplot(111, projection='3d')

# ax.scatter(algov5['taille anneau'], algov5['nb robots'], algov5['time elapsed'], label='algo5', marker='d', color='yellow', linewidths=20)
# #ax.scatter(algov5err['taille anneau'], algov5err['nb robots'], algov5err['time elapsed'], label='algo5err', marker='d', color='orange', linewidths=20)
# ax.scatter(algov7['taille anneau'], algov7['nb robots'], algov7['time elapsed'], label='algo7', marker='d', color='green', linewidths=10)
# #ax.scatter(algov7err['taille anneau'], algov7err['nb robots'], algov7err['time elapsed'], label='algo7err', marker='d', color='purple', linewidths=10)


# plt.title("Elapsed time depending on ring size and robot number", fontsize=20)
# ax.set_xlabel('Taille anneau', fontsize=20)
# ax.set_ylabel('Nb Robots', fontsize=20)
# ax.set_zlabel('Time', fontsize=20)
# ax.legend(fontsize=20)
# plt.tight_layout()
# # plt.savefig('./data/graphe-time')
# plt.show()