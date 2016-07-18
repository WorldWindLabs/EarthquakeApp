# NASA World Wind Earthquake Data Analysis code
import data.loadearthquake as eaq
import anomdetec.detectanomalies as anom
import learning.clusters as clusters

def preprocess(name, magnetic, anomalies):
    x = []
    y = []
    for i in range(3):
        anom_rate = anom.anomaly_rate(magnetic, anomalies[i])
        cluster_list = clusters.get(anom_rate, anomalies[i])
        features, interval = clusters.comp_features(cluster_list)
        x.append(features)
        y.append(eaq.look_relevant_earthquake(name, interval))

    return x, y
