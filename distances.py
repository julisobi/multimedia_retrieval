from scipy.spatial import distance
from scipy.stats import wasserstein_distance


def euclidean_distance(vector1, vector2, weights):
    we_vector1 = [a * b for a, b in zip(vector1, weights)]
    we_vector2 = [a * b for a, b in zip(vector2, weights)]
    euc_d = distance.euclidean(we_vector1, we_vector2)
    return euc_d


def cosine_distance(vector1, vector2, weights):
    we_vector1 = [a * b for a, b in zip(vector1, weights)]
    we_vector2 = [a * b for a, b in zip(vector2, weights)]
    cos_d = distance.cosine(we_vector1, we_vector2)
    return cos_d


def earth_movers_distance(vector1, vector2, weights):
    emd = wasserstein_distance(vector1, vector2, weights, weights)
    return emd
