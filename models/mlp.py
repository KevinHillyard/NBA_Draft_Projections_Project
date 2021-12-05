from random import random
import numpy as np
import csv
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from arff_utils import Arff_Utils
import math
import sys


def mlp():
    x, y = Arff_Utils.get_all_players_as_numpy()

    training_index = round(len(x) * 0.8)
    training_x = x[:training_index]
    test_x = x[training_index:]
    training_y = y[:training_index, :]
    test_y = y[training_index:, :]

    hidden_nodes_options = [
        (32),
        (64),
        (128),
        (8, 8),
        (16, 16),
        (32, 32),
        (8, 16, 8),
        (16, 32, 16),
        (8, 8, 8),
    ]
    lrs = [0.01, 0.1, 0.8, 1.0]
    momentums = [0.0, 0.5, 0.8, 1.0]
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
                "Regularization",
            ]
        )
        for hn_ in hidden_nodes_options:
            for lr_ in lrs:
                for momentum_ in momentums:
                    for reg_ in regularization:
                        mlp_model = MLPRegressor(
                            hidden_layer_sizes=hn_,
                            alpha=reg_,
                            learning_rate_init=lr_,
                            max_iter=1000000,
                            momentum=momentum_,
                        )
                        mlp_model.fit(
                            training_x,
                            training_y.flatten(),
                        )
                        predictions = mlp_model.predict(test_x)
                        y = test_y.flatten()
                        # print(training_x)
                        # print("Y")
                        # print(training_y)
                        # print("TEST X")
                        # print(test_x)
                        # for i in range(len(predictions)):
                        #     if predictions[i] > 61:
                        #         predictions[i] == 61
                        # print("TEST Y VS PREDICTIONS")

                        me = np.zeros(len(y))
                        for i in range(len(predictions)):
                            if predictions[i] > 61:
                                predictions[i] = 61
                            me[i] = abs(predictions[i] - y[i])

                        # for i in range(len(predictions)):
                        #     print(f"me: {me[i]} y: {y[i]} pred: {predictions[i]}")

                        me = np.sum(me) / len(me)
                        result_row = [
                            me,
                            hn_,
                            lr_,
                            momentum_,
                            reg_,
                        ]
                        writer.writerow(result_row)
                        print(f"{result_row}")


if __name__ == "__main__":
    mlp()
