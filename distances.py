from scipy.spatial import distance
from scipy.stats import wasserstein_distance
from normalize_features import normalize_single_feature

WEIGHTS = [5, 5, 5, 5, 5, 15, 15, 15, 15, 15]


def euclidean_distance(vector1, vector2):
    euc_d = distance.euclidean(vector1, vector2)
    return euc_d


def cosine_distance(vector1, vector2):
    cos_d = distance.cosine(vector1, vector2)
    return cos_d


def earth_movers_distance(vector1, vector2):
    emd = wasserstein_distance(vector1, vector2)
    return emd


def combine_distance(vector1, vector2):
    global_vector1 = [val * 0.04 for val in vector1[:5]]
    global_vector2 = [val * 0.04 for val in vector2[:5]]
    dist1 = cosine_distance(global_vector1, global_vector2)
    hista3_vector1 = [val * 0.02 for val in vector1[5:15]]
    hista3_vector2 = [val * 0.02 for val in vector2[5:15]]
    dist2 = earth_movers_distance(hista3_vector1, hista3_vector2)
    histd1_vector1 = [val * 0.02 for val in vector1[15:25]]
    histd1_vector2 = [val * 0.02 for val in vector1[15:25]]
    dist3 = earth_movers_distance(histd1_vector1, histd1_vector2)
    histd2_vector1 = [val * 0.02 for val in vector1[25:35]]
    histd2_vector2 = [val * 0.02 for val in vector1[25:35]]
    dist4 = earth_movers_distance(histd2_vector1, histd2_vector2)
    histd3_vector1 = [val * 0.02 for val in vector1[35:]]
    histd3_vector2 = [val * 0.02 for val in vector1[35:]]
    dist5 = earth_movers_distance(histd3_vector1, histd3_vector2)
    avg_dist = (dist1 + dist2 + dist3 + dist4 + dist5) / 5
    return avg_dist
