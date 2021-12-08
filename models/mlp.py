import numpy as np
import csv
from sklearn.neural_network import MLPRegressor
from arff_utils import Arff_Utils


def mlp():
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
    lrs = [0.1, 0.2]
    momentums = [0.3, 0.5, 0.8]
    regularization = [0.0001, 0.0005, 0.001]
    with open(
        r"./files/grid_search_mlp_no_undrafted.csv",
        "w",
        encoding="UTF8",
        newline="",
    ) as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(
            [
                "ME",
                "Iteration",
                "Hidden Nodes",
                "Learning Rate",
                "Momentum",
                "Regularization",
            ]
        )
        for iteration in range(3):
            x, y = Arff_Utils.get_all_players_as_numpy(include_undrafted=False)
            for hn_ in hidden_nodes_options:
                for lr_ in lrs:
                    for momentum_ in momentums:
                        for reg_ in regularization:
                            mlp_model = MLPRegressor(
                                hidden_layer_sizes=hn_,
                                alpha=reg_,
                                learning_rate_init=lr_,
                                max_iter=10000,
                                momentum=momentum_,
                            )
                            me = Arff_Utils.ten_fold_cross_validation(mlp_model, x, y)
                            result_row = [
                                me,
                                iteration,
                                hn_,
                                lr_,
                                momentum_,
                                reg_,
                            ]
                            writer.writerow(result_row)
                            print(f"{result_row}")


if __name__ == "__main__":
    mlp()
