# Machine Learning helper module

import data.earthquake as eaq
import anomdetec.detectanomalies as anom
import learning.clusters as clusters

def preprocess(name, magnetic, anomalies):
    '''
    Preprocess function for machine learning algorithms.

    Clustering of anomalies, featuring of clusters and ML training output computation

    Args:
        name: (string) station name
        magnetic: (dataframe) magnetic field dataframe
        anomalies: (dataframe tuple) for each axis, dataframe with its anomalies

    Returns:
        x: (list(size = 3) of lists) For each axis, a list with a each cluster's features

        y: (bool list) For each cluster, if there's a relevant earthquake within some time
            after it
    '''

    x = []
    y = []
    for i in range(3):
        anom_rate = anom.anomaly_rate(magnetic, anomalies[i])
        cluster_list = clusters.get(anom_rate, anomalies[i])
        features, interval = clusters.comp_features(cluster_list)
        x.append(features)
        y.append(eaq.look_relevant_earthquake(name, interval))

    return x, y
