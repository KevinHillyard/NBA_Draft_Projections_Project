from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
import arff_reader
import numpy as np
import math


class Arff_Utils:
    def ten_fold_cross_validation(model_object, x, y):
        agg_me = np.zeros(10)
        n_fold_size = round(len(x) / 10)
        for i in range(10):
            test_indeces = [j + (i * n_fold_size) for j in range(n_fold_size)]
            training_indeces = []
            if i == 9:
                if test_indeces[-1] >= len(x):
                    for j in range(len(test_indeces)):
                        if test_indeces[j] >= len(x):
                            test_indeces = test_indeces[:j]
                            break
                elif test_indeces[-1] < len(x) - 1:
                    test_indeces += [j for j in range(test_indeces[-1] + 1, len(x))]
            for j in range(len(x)):
                if j < test_indeces[0] or j > test_indeces[-1]:
                    training_indeces.append(j)

            training_x = np.delete(x, test_indeces, axis=0)
            training_y = np.delete(y, test_indeces, axis=0)
            test_x = np.delete(x, training_indeces, axis=0)
            test_y = np.delete(y, training_indeces, axis=0)

            model_object.fit(training_x, training_y.flatten())
            predictions = model_object.predict(test_x)

            me = np.zeros(len(test_y))
            for j in range(len(predictions)):
                if predictions[j] > 61:
                    predictions[j] = 61
                me[j] = abs(predictions[j] - test_y[j])
                # print(f"me: {me[j]} y: {test_y[j]} pred: {predictions[j]}")

            agg_me[i] = np.sum(me) / len(me)

        return np.sum(agg_me) / len(agg_me)

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
