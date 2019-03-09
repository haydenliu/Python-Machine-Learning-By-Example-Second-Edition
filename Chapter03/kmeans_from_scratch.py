'''
Source codes for Python Machine Learning By Example 2nd Edition (Packt Publishing)
Chapter 3: Mining the 20 Newsgroups Dataset with Clustering and Topic Modeling Algorithms
Author: Yuxi (Hayden) Liu
'''


from sklearn import datasets
iris = datasets.load_iris()
X = iris.data[:, 2:4]
y = iris.target

import numpy as np
from matplotlib import pyplot as plt
y_0 = np.where(y==0)
plt.scatter(X[y_0, 0], X[y_0, 1])
y_1 = np.where(y==1)
plt.scatter(X[y_1, 0], X[y_1, 1])
y_2 = np.where(y==2)
plt.scatter(X[y_2, 0], X[y_2, 1])
plt.show()


k = 3
random_index = np.random.choice(range(len(X)), k)
centroids = X[random_index]


def visualize_centroids(X, centroids):
    plt.scatter(X[:, 0], X[:, 1])
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=200, c='#050505')
    plt.show()


visualize_centroids(X, centroids)


def dist(a, b):
    return np.linalg.norm(a - b, axis=1)

def assign_cluster(x, centroids):
    distances = dist(x, centroids)
    cluster = np.argmin(distances)
    return cluster

def update_centroids(X, centroids, clusters):
    for i in range(k):
        cluster_i = np.where(clusters == i)
        centroids[i] = np.mean(X[cluster_i], axis=0)


clusters = np.zeros(len(X))

tol = 0.0001
max_iter = 100

iter = 0
centroids_diff = 100000

from copy import deepcopy
while iter < max_iter and centroids_diff > tol:
    for i in range(len(X)):
        clusters[i] = assign_cluster(X[i], centroids)
    centroids_prev = deepcopy(centroids)
    update_centroids(X, centroids, clusters)
    iter += 1
    centroids_diff = np.linalg.norm(centroids - centroids_prev)
    print('Iteration:', str(iter))
    print('Centroids:\n', centroids)
    print('Centroids move: {:5.4f}'.format(centroids_diff))
    visualize_centroids(X, centroids)


for i in range(k):
    cluster_i = np.where(clusters == i)
    plt.scatter(X[cluster_i, 0], X[cluster_i, 1])
plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=200, c='#050505')
plt.show()



