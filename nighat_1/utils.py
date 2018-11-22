import numpy as np

###########################################################
# DO NOT EDIT ANYTHING ABOVE
###########################################################
#TODO: implement distance functions


def l2_distance(point1, point2):
    return norm(point1, point2, 2)


def l1_distance(point1, point2):
    return norm(point1, point2, 1)


def linf_distance(point1, point2):
    # ensure vectors are np arrays
    point1 = check_nparray_status(point1)
    point2 = check_nparray_status(point2)

    # take the difference first
    difference = point1 - point2

    #take the absolute value of the vector
    difference = np.absolute(difference)

    # find the highest value
    highest_value = 0
    for element in difference:
        if element > highest_value:
            highest_value = element

    return highest_value


def inner_distance(point1, point2):
    # try using the simple dot product as the inner distance

    product = 0
    for i in range(len(point1)):
        product += point1[i]*point2[i]

    return product


def norm(point1, point2, p):
    # ensure vectors are np arrays
    point1 = check_nparray_status(point1)
    point2 = check_nparray_status(point2)


    # first take the difference of the two
    difference = point1 - point2

    # take the absolute value of the difference
    difference = np.absolute(difference)

    # raise each quantity to the p power
    difference = difference**p

    # sum up each element in the vector
    sum = 0
    for element in difference:
        sum += element

    # take the p-root of the sum
    sum = sum**(1/p)

    return sum

def check_nparray_status(vector):
    if type(vector) is not np.ndarray:
        vector = np.asarray(vector)
    return vector

def normalize_vector(vector):
    mag = get_manitude(vector)

    return vector/mag

def get_manitude(vector):
    squared = vector ** 2

    sum = 0
    for element in squared:
        sum += element

    mag = sum ** (1 / 2)

    return mag


def predict(self, feat):
    '''
    -- Input
    feat: N' x M
    -- Ouput
    label: N'
    '''

    n = len(feat)
    label = [None] * n

    for j, feature in enumerate(feat):
        # create a list of k elements
        nearest = None
        num_filled = 0
        distance_threshold = None
        # iterate through the training examples
        for i, ex in enumerate(self.trn_feat):
            # get the distance between the input feature and every example
            distance = l2_distance(feature, ex)
            if distance_threshold is None:
                nearest = [self.trn_label[i], ex, distance]
                distance_threshold = nearest[2]
            elif distance < distance_threshold:
                distance_threshold = distance
                nearest = [self.trn_label[i], ex, distance]

    return nearest


# print(inner_distance([1, 2], [1, 3]))
# print(inner_distance([4, 7], [1, 3]))
# print(inner_distance([1, 100], [100, 100]))

# print(l1_distance([5.8, 2.7, 5.1, 1.9], [4.6, 3.2, 1.4, 0.2]))
# print(l2_distance([5.8, 2.7, 5.1, 1.9], [4.6, 3.2, 1.4, 0.2]))
# print(linf_distance([5.8, 2.7, 5.1, 1.9], [4.6, 3.2, 1.4, 0.2]))
# print(inner_distance([5.8, 2.7, 5.1, 1.9], [4.6, 3.2, 1.4, 0.2]))

# print(l1_distance([1,3], [2, 5]))
# print(l2_distance([1,3], [2, 5]))