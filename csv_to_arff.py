import arff
import csv


class CSV_to_ARFF:
    def __init__(self, in_filename=None, out_filename=None):
        self.in_file = in_filename
        self.out_file = out_filename

    def write_arff(self):
        with open(self.in_file, newline="") as csvfile:
            data = list(csv.reader(csvfile))

        arff.dump(
            self.out_file,
            data[1:],
            relation=self.in_file,
            names=data[0],
        )


if __name__ == "__main__":
    arff_writer = CSV_to_ARFF(in_filename=r"test.csv", out_filename=r"test.arff")
    arff_writer.write_arff()
