import matplotlib.pyplot as plt
import fnmatch
import os
import csv
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def main():
    graph_best_models()


def graph_best_models():
    model_result_filenames = np.array(
        [f for f in os.listdir("./files") if fnmatch.fnmatch(f, "grid_search*.csv")]
    )

    bar_y = np.zeros(len(model_result_filenames))
    bar_x = [
        x_label[12:-4].replace("_no_undrafted", "_2")
        for x_label in model_result_filenames
    ]

    for i in range(len(model_result_filenames)):
        filename = model_result_filenames[i]
        with open(
            "./files/" + filename,
            "r",
            encoding="UTF8",
            newline="",
        ) as f:
            reader = csv.reader(f)
            row_index = 0
            for row in reader:
                if row_index >= 1:
                    bar_y[i] = row[0]
                    break
                row_index += 1

    bar_y, bar_x = zip(*sorted(zip(bar_y, bar_x), reverse=True))

    fig, ax = plt.subplots()
    barlist = ax.bar(bar_x, bar_y)
    for i in range(len(bar_x)):
        if "_2" in bar_x[i]:
            barlist[i].set_color("r")
        if "_3" in bar_x[i]:
            barlist[i].set_color("g")

    legend_elements = [
        Line2D([0], [0], color="b", lw=4, label="With Undrafted Players"),
        Line2D([0], [0], color="r", lw=4, label="Without Undrafted Players"),
        Line2D([0], [0], color="g", lw=4, label="With Undrafted, Smaller Dataset"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")
    ax.tick_params(axis="x", labelrotation=45)
    plt.ylim([0, 14])
    plt.ylabel("Mean Absolute Error")
    plt.xlabel("Model Name")
    plt.title("Mean Absolute Error Using Ten-Fold Cross Validation")
    plt.tight_layout()
    plt.savefig("./files/error_by_model_2.pdf")


if __name__ == "__main__":
    main()
