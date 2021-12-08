from arff_utils import Arff_Utils
import numpy as np
from sklearn import tree
import csv


def dt():
    hyperparameter_grid = [
        ["squared_error", "friedman_mse", "absolute_error", "poisson"],
        ["best"],  # , "random"],
        [8, 16, 24, 32, 48],
        [2, 4, 6],
        [1, 2, 4],
        [0.0, 0.001, 0.01],
        [0.0, 0.001, 0.01],
    ]
    with open(
        r"./files/grid_search_dt_no_undrafted.csv",
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
                "criterion",
                "splitter",
                "max depth",
                "min_samp_split",
                "min_samp_leaf",
                "min_weight_frac_leaf",
                "min_impurity_dec",
            ]
        )
        for iteration in range(3):
            x, y = Arff_Utils.get_all_players_as_numpy(include_undrafted=False)
            for criterion in hyperparameter_grid[0]:
                for splitter in hyperparameter_grid[1]:
                    for max_depth in hyperparameter_grid[2]:
                        for min_samp_split in hyperparameter_grid[3]:
                            for min_samp_leaf in hyperparameter_grid[4]:
                                for min_weight_frac_leaf in hyperparameter_grid[5]:
                                    for min_impurity_decrease in hyperparameter_grid[6]:
                                        DecisionTree = tree.DecisionTreeRegressor(
                                            criterion=criterion,
                                            splitter=splitter,
                                            max_depth=max_depth,
                                            min_samples_split=min_samp_split,
                                            min_samples_leaf=min_samp_leaf,
                                            min_weight_fraction_leaf=min_weight_frac_leaf,
                                            min_impurity_decrease=min_impurity_decrease,
                                        )
                                        me = Arff_Utils.ten_fold_cross_validation(
                                            DecisionTree, x, y
                                        )
                                        result_row = [
                                            me,
                                            iteration,
                                            criterion,
                                            splitter,
                                            max_depth,
                                            min_samp_split,
                                            min_samp_leaf,
                                            min_weight_frac_leaf,
                                            min_impurity_decrease,
                                        ]
                                        writer.writerow(result_row)
                                        print(f"{result_row}")


if __name__ == "__main__":
    dt()
