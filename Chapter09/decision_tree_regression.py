'''
Source codes for Python Machine Learning By Example 2nd Edition (Packt Publishing)
Chapter 9: Stock Price Prediction with Regression Algorithms
Author: Yuxi (Hayden) Liu
'''
import numpy as np


# Mean squared error calculation function given continuous targets of a data set,
def mse(targets):
    # When the set is empty
    if targets.size == 0:
        return 0
    return np.var(targets)

def weighted_mse(groups):
    """ Calculate weighted MSE of children after a split
    Args:
        groups (list of children, and a child consists a list of targets)
    Returns:
        float, weighted impurity
    """
    total = sum(len(group) for group in groups)
    weighted_sum = 0.0
    for group in groups:
        weighted_sum += len(group) / float(total) * mse(group)
    return weighted_sum


print('{0:.4f}'.format(mse(np.array([1, 2, 3]))))
print('{0:.4f}'.format(weighted_mse([np.array([1, 2, 3]), np.array([1, 2])])))

print('type-semi: {0:.4f}'.format(weighted_mse([np.array([600, 400, 700]), np.array([700, 800])])))
print('bedroom-2: {0:.4f}'.format(weighted_mse([np.array([700, 400]), np.array([600, 800, 700])])))
print('bedroom-3: {0:.4f}'.format(weighted_mse([np.array([600, 800]), np.array([700, 400, 700])])))
print('bedroom-4: {0:.4f}'.format(weighted_mse([np.array([700]), np.array([600, 700, 800, 400])])))


print('bedroom-2: {0:.4f}'.format(weighted_mse([np.array([]), np.array([600, 400, 700])])))
print('bedroom-3: {0:.4f}'.format(weighted_mse([np.array([400]), np.array([600, 700])])))
print('bedroom-4: {0:.4f}'.format(weighted_mse([np.array([400, 600]), np.array([700])])))




def split_node(X, y, index, value):
    """ Split data set X, y based on a feature and a value
    Args:
        X, y (numpy.ndarray, data set)
        index (int, index of the feature used for splitting)
        value (value of the feature used for splitting)
    Returns:
        list, list: left and right child, a child is in the format of [X, y]
    """
    x_index = X[:, index]
    # if this feature is numerical
    if type(X[0, index]) in [int, float]:
        mask = x_index >= value
    # if this feature is categorical
    else:
        mask = x_index == value
    # split into left and right child
    left = [X[~mask, :], y[~mask]]
    right = [X[mask, :], y[mask]]
    return left, right


def get_best_split(X, y):
    """ Obtain the best splitting point and resulting children for the data set X, y
    Args:
        X, y (numpy.ndarray, data set)
        criterion (gini or entropy)
    Returns:
        dict {index: index of the feature, value: feature value, children: left and right children}
    """
    best_index, best_value, best_score, children = None, None, 1e10, None
    for index in range(len(X[0])):
        for value in np.sort(np.unique(X[:, index])):
            groups = split_node(X, y, index, value)
            impurity = weighted_mse([groups[0][1], groups[1][1]])
            if impurity < best_score:
                best_index, best_value, best_score, children = index, value, impurity, groups
    return {'index': best_index, 'value': best_value, 'children': children}



def get_leaf(targets):
    # Obtain the leaf as the mean of the targets
    return np.mean(targets)



def split(node, max_depth, min_size, depth):
    """ Split children of a node to construct new nodes or assign them terminals
    Args:
        node (dict, with children info)
        max_depth (int, maximal depth of the tree)
        min_size (int, minimal samples required to further split a child)
        depth (int, current depth of the node)
    """
    left, right = node['children']
    del (node['children'])
    if left[1].size == 0:
        node['right'] = get_leaf(right[1])
        return
    if right[1].size == 0:
        node['left'] = get_leaf(left[1])
        return
    # Check if the current depth exceeds the maximal depth
    if depth >= max_depth:
        node['left'], node['right'] = get_leaf(left[1]), get_leaf(right[1])
        return
    # Check if the left child has enough samples
    if left[1].size <= min_size:
        node['left'] = get_leaf(left[1])
    else:
        # It has enough samples, we further split it
        result = get_best_split(left[0], left[1])
        result_left, result_right = result['children']
        if result_left[1].size == 0:
            node['left'] = get_leaf(result_right[1])
        elif result_right[1].size == 0:
            node['left'] = get_leaf(result_left[1])
        else:
            node['left'] = result
            split(node['left'], max_depth, min_size, depth + 1)
    # Check if the right child has enough samples
    if right[1].size <= min_size:
        node['right'] = get_leaf(right[1])
    else:
        # It has enough samples, we further split it
        result = get_best_split(right[0], right[1])
        result_left, result_right = result['children']
        if result_left[1].size == 0:
            node['right'] = get_leaf(result_right[1])
        elif result_right[1].size == 0:
            node['right'] = get_leaf(result_left[1])
        else:
            node['right'] = result
            split(node['right'], max_depth, min_size, depth + 1)


def train_tree(X_train, y_train, max_depth, min_size):
    """ Construction of a tree starts here
    Args:
        X_train,  y_train (list, list, training data)
        max_depth (int, maximal depth of the tree)
        min_size (int, minimal samples required to further split a child)
    """
    root = get_best_split(X_train, y_train)
    split(root, max_depth, min_size, 1)
    return root



CONDITION = {'numerical': {'yes': '>=', 'no': '<'},
             'categorical': {'yes': 'is', 'no': 'is not'}}
def visualize_tree(node, depth=0):
    if isinstance(node, dict):
        if type(node['value']) in [int, float]:
            condition = CONDITION['numerical']
        else:
            condition = CONDITION['categorical']
        print('{}|- X{} {} {}'.format(depth * '  ', node['index'] + 1, condition['no'], node['value']))
        if 'left' in node:
            visualize_tree(node['left'], depth + 1)
        print('{}|- X{} {} {}'.format(depth * '  ', node['index'] + 1, condition['yes'], node['value']))
        if 'right' in node:
            visualize_tree(node['right'], depth + 1)
    else:
        print('{}[{}]'.format(depth * '  ', node))


X_train = np.array([['semi', 3],
                    ['detached', 2],
                    ['detached', 3],
                    ['semi', 2],
                    ['semi', 4]], dtype=object)

y_train = np.array([600, 700, 800, 400, 700])

tree = train_tree(X_train, y_train, 2, 2)
visualize_tree(tree)



# Directly use DecisionTreeRegressor from scikit-learn
from sklearn import datasets
boston = datasets.load_boston()

num_test = 10    # the last 10 samples as testing set
X_train = boston.data[:-num_test, :]
y_train = boston.target[:-num_test]
X_test = boston.data[-num_test:, :]
y_test = boston.target[-num_test:]

from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(max_depth=10, min_samples_split=3)

regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)
print(predictions)
print(y_test)


from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_split=3)
regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)
print(predictions)





import tensorflow as tf
from tensorflow.contrib.tensor_forest.python import tensor_forest
from tensorflow.python.ops import resources


n_iter = 20
n_features = int(X_train.shape[1])
n_trees = 10
max_nodes = 30000


x = tf.placeholder(tf.float32, shape=[None, n_features])
y = tf.placeholder(tf.float32, shape=[None])


hparams = tensor_forest.ForestHParams(num_classes=1, regression=True, num_features=n_features, num_trees=n_trees,
                                      max_nodes=max_nodes, split_after_samples=30).fill()


forest_graph = tensor_forest.RandomForestGraphs(hparams)


train_op = forest_graph.training_graph(x, y)
loss_op = forest_graph.training_loss(x, y)


infer_op, _, _ = forest_graph.inference_graph(x)

cost = tf.losses.mean_squared_error(labels=y, predictions=infer_op[:, 0])



init_vars = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer(), resources.initialize_resources(resources.shared_resources()))

sess = tf.Session()

sess.run(init_vars)


for i in range(1, n_iter + 1):
    _, c = sess.run([train_op, cost], feed_dict={x: X_train, y: y_train})
    print('Iteration %i, training loss: %f' % (i, c))


pred = sess.run(infer_op, feed_dict={x: X_test})[:, 0]
print(pred)
