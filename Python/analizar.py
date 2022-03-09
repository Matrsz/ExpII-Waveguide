import numpy as np
import csv
import matplotlib.pyplot as plt


filename = 'aire.csv'
data1 = np.genfromtxt('aire.csv', delimiter=' ')
z1, v1 = data1[:,0], data1[:, 1]
data2 = np.genfromtxt('cortocircuito.csv', delimiter=' ')
z2, v2 = data2[:,0], data2[:, 1]

data3 = np.genfromtxt('acrilico.csv', delimiter=' ')
z3, v3 = data3[:,0], data3[:, 1]

data4 = np.genfromtxt('corneta.csv', delimiter=' ')
z4, v4 = data4[:,0], data4[:, 1]



plt.plot(z1, v1, z2, v2, z3, v3, z4, v4)
plt.legend(["aire", "cortocircuito", "acrilico", "corneta"])
plt.show()