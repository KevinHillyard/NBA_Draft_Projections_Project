import numpy as np
import sys
import csv
from sklearn.linear_model import LinearRegression
from arff_utils import Arff_Utils


def linear_regression():
    with open(
        r"./files/grid_search_linear_regression_no_undrafted.csv",
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
                "Coefficients",
            ]
        )
        for iteration in range(10):
            x, y = Arff_Utils.get_all_players_as_numpy(include_undrafted=False)
            linreg = LinearRegression()
            me = Arff_Utils.ten_fold_cross_validation(linreg, x, y)
            result_row = np.concatenate(
                (
                    np.array(
                        [
                            me,
                            iteration,
                        ]
                    ),
                    linreg.coef_,
                )
            )
            writer.writerow(result_row)
            print(f"{result_row}")


if __name__ == "__main__":
    linear_regression()
