import arff
import csv


class CSV_to_ARFF:
    def __init__(self, in_filename=None, out_filename=None):
        self.in_file = in_filename
        self.out_file = out_filename

    def write_arff(self):
        with open(self.in_file, newline="") as csvfile:
            data = list(csv.reader(csvfile))

        nominal_values = [[] for i in range(len(data[1]))]

        for i in range(len(data[1:])):
            for j in range(len(data[i + 1])):
                data[i + 1][j] = data[i + 1][j].replace(" ", "_")
                data[i + 1][j] = data[i + 1][j].replace("cm", "")
                data[i + 1][j] = data[i + 1][j].replace("kg", "")
                try:
                    data[i + 1][j] = int(data[i + 1][j])
                except:
                    try:
                        data[i + 1][j] = float(data[i + 1][j])
                    except:
                        if data[i + 1][j] not in nominal_values[j]:
                            nominal_values[j].append(data[i + 1][j])

        arff.dump(
            self.out_file,
            data[1:],
            relation=self.in_file,
            names=[attribute.replace("%", "_percent") for attribute in data[0]],
        )

        print(f"Nominal Values: {nominal_values}")


if __name__ == "__main__":
    arff_writer = CSV_to_ARFF(
        in_filename=r"./files/finalDataSetTrimmed.csv",
        out_filename=r"./files/finalDataSetTrimmed.arff",
    )
    arff_writer.write_arff()
