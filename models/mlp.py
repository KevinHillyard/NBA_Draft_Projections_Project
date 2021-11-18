from random import random
import numpy as np
import csv
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
import arff_reader
import math
import sys


def mlp():
    np.set_printoptions(threshold=sys.maxsize)
    data_arff = arff_reader.Arff(arff=r"./files/allPlayers.arff", label_count=1)
    data = data_arff.data
    data = shuffle(data)

    scaler = MinMaxScaler()
    scaler.fit(data[:, : data_arff.features_count])
    data_features = scaler.transform(data[:, : data_arff.features_count])

    training_index = round(len(data_features) * 0.8)
    training_x = data_features[:training_index]
    test_x = data_features[training_index:]
    training_y = data[:training_index, data_arff.features_count :]
    test_y = data[training_index:, data_arff.features_count :]

    hidden_nodes_options = [(32), (64), (128), (8, 8), (16, 16), (32, 32)]
    lrs = [1.0, 0.8, 0.1, 0.01]
    momentums = [0.0, 0.5, 0.8, 1.0]
    nesterov = [True, False]
    regularization = [0, 0.00001, 0.0001, 0.0005]
    with open(
        r"./files/grid_search.csv",
        "w",
        encoding="UTF8",
        newline="",
    ) as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(
            [
                "RMSE",
                "Hidden Nodes",
                "Learning Rate",
                "Momentum",
                "Nesterov",
                "Regularization",
            ]
        )
        for hn_ in hidden_nodes_options:
            for lr_ in lrs:
                for momentum_ in momentums:
                    for nest_ in nesterov:
                        for reg_ in regularization:
                            mlp_model = MLPClassifier(
                                hidden_layer_sizes=hn_,
                                alpha=reg_,
                                learning_rate_init=lr_,
                                max_iter=10000000,
                                momentum=momentum_,
                                nesterovs_momentum=nest_,
                            )
                            mlp_model.fit(
                                training_x,
                                training_y.flatten(),
                            )
                            predictions = mlp_model.predict(test_x)
                            y = test_y.flatten()
                            mse = np.zeros(len(y))
                            for i in range(len(predictions)):
                                prediction = predictions[i]
                                if prediction > 61:
                                    prediction == 61
                                mse[i] = (prediction - y[i]) ** 2

                            mse = np.sum(mse) / len(mse)
                            rmse = math.sqrt(mse)
                            result_row = [
                                rmse,
                                hn_,
                                lr_,
                                momentum_,
                                nest_,
                                reg_,
                            ]
                            writer.writerow(result_row)
                            print(f"{result_row}")


if __name__ == "__main__":
    mlp()
