from scipy.spatial import distance


def euclidean_distance(vector1, vector2):
    euc_d = distance.euclidean(vector1, vector2)
    return euc_d


def cosine_distance(vector1, vector2):
    cos_d = distance.cosine(vector1, vector2)
    return cos_d
