import numpy as np
from sklearn.decomposition import IncrementalPCA
from array import array

X = np.array([[-1, -1, 5, 3], [-2, -1, 4, 2], [-3, -2, 3, 1], [1, 1, 6, 4], [2, 1, 3, 1], [3, 2, 0, 8]])
Z = np.array([1, 4, 3, 5, 1, 6, 3, -1, 12, 1, 3, 7, 3, 9])
test = np.zeros(14)
ipca = IncrementalPCA(n_components=3, batch_size=3)
ipca.fit(X)

Y = ipca.transform(X)
print("X : {}".format(X))
print("Z : {}".format(len(Z)))
print("Z == 1 : {}".format((Z == 1)))
print("Y : {}".format(Y))
print("test[Z == 1] : {}".format(test[Z == 1]))
print("test Z bicondittional : {}".format(test[(Z == 1) + (Z == 3)]))