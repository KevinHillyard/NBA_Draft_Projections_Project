from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
import arff_reader
import numpy as np
import math


class Arff_Utils:
    def get_all_players_as_numpy():
        data_arff = arff_reader.Arff(
            arff=r"./files/finalDataSetTrimmed.arff", label_count=1
        )
        nominals = data_arff.get_nominal_idx()
        for i in range(len(nominals)):
            nominals[i] = [nominals[i], data_arff.unique_value_count(nominals[i])]
        nominals = np.array(nominals)
        data = data_arff.data
        data = shuffle(data)

        scaler = MinMaxScaler()
        scaler.fit(data[:, : data_arff.features_count])
        data_features = scaler.transform(data[:, : data_arff.features_count])

        columns_needed = [
            math.ceil(math.log(unique_values, 2)) for unique_values in nominals[:, 1]
        ]
        insert_columns = np.zeros((len(data), sum(columns_needed)))

        for row_index in range(len(data_features)):
            col_index = 0
            for i in range(len(nominals)):
                bits = format(
                    int(
                        data_features[row_index][nominals[i][0]] * (nominals[i][1] - 1)
                    ),
                    "b",
                ).zfill(columns_needed[i])

                for j in range(len(bits)):
                    insert_columns[row_index][col_index] = bits[j]
                    col_index += 1

        index_tracker = 0
        for i in range(len(nominals)):
            data_features = np.concatenate(
                (
                    data_features[:, : nominals[i][0] + index_tracker],
                    insert_columns[
                        :, index_tracker + i : index_tracker + columns_needed[i] + i
                    ],
                    data_features[:, nominals[i][0] + index_tracker + 1 :],
                ),
                axis=1,
            )
            index_tracker += columns_needed[i] - 1

        return data_features, data[:, data_arff.features_count :]
