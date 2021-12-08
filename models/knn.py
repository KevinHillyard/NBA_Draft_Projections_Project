from sklearn.metrics.pairwise import haversine_distances
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
import numpy as np
import csv
from arff_utils import Arff_Utils


def knn():
    k_values = [1, 3, 5, 7, 9, 11, 13, 15]
    distance_metrics = [
        "euclidean",
        "manhattan",
        "chebyshev",
        "minkowski",
    ]
    with open(
        r"./files/grid_search_knn_3.csv",
        "w",
        encoding="UTF8",
        newline="",
    ) as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(
            [
                "me",
                "iteration",
                "k",
                "distance metric",
            ]
        )
        for iteration in range(3):
            x, y = Arff_Utils.get_all_players_as_numpy(use_smaller=True)

            for k in k_values:
                for distance_metric in distance_metrics:
                    k_neighbors_model = KNeighborsRegressor(
                        n_neighbors=k, metric=distance_metric
                    )
                    me = Arff_Utils.ten_fold_cross_validation(k_neighbors_model, x, y)
                    result_row = [
                        me,
                        iteration,
                        k,
                        distance_metric,
                    ]
                    writer.writerow(result_row)
                    print(f"{result_row}")


if __name__ == "__main__":
    knn()
