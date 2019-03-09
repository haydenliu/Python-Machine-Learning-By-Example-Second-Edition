'''
Source codes for Python Machine Learning By Example 2nd Edition (Packt Publishing)
Chapter 10: Machine Learning Best Practices
Author: Yuxi (Hayden) Liu
'''

from sklearn.preprocessing import Binarizer

X = [[4], [1], [3], [0]]
binarizer = Binarizer(threshold=2.9)
X_new = binarizer.fit_transform(X)
print(X_new)




from sklearn.preprocessing import PolynomialFeatures

X = [[2, 4],
     [1, 3],
     [3, 2],
     [0, 3]]
poly = PolynomialFeatures(degree=2)
X_new = poly.fit_transform(X)
print(X_new)
