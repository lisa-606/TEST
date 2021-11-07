import pandas as pd
import numpy as np


def pinyin2ID(pinyin, IDTable):
    """
    convert pinyin 2 ID in IDTable
    :param pinyin: list of pinyin
    :param IDTable: the IDTable in numpy array
    :return: idArray, the IDs in IDTable
    """
    idArray = []
    for num, sing_py in enumerate(pinyin):
        if num % 2 == 0:
            if np.any(sing_py == IDTable[0:26, 2]):
                ind = np.where(IDTable[0:26, 2] == sing_py)
                # print(ind)
                idArray.append(IDTable[ind[0].tolist()[0], 0])

        if num % 2 == 1:
            if np.any(sing_py == IDTable[26:, 2:4]):
                ind = np.where(sing_py == IDTable[26:, 2:4])
                # print(ind)
                idArray.append(IDTable[ind[0].tolist()[0] + 26, 0])
            else:
                print('didnt find')

    return idArray


if __name__ == '__main__':
    IDTable = pd.read_csv(r'IDTable.csv')
    IDTable = np.array(IDTable.values)
    # print(IDTable[:,1])
    pinyin = ['ai','o','c','ao']
    idarray = pinyin2ID(pinyin, IDTable)
    print(idarray)
