from typing import List
import pandas as pd
import numpy as np
import os


def csv2df(file_name: str, colname: list) -> pd.DataFrame:
    """
    load shuangpin_data from csv_file
    :param file_name: ***.csv
    :param colname: column name
    :return:None
    """
    meta_combi = pd.DataFrame(pd.read_csv(file_name))
    meta_combi.columns = colname
    return meta_combi

def IDTableLoader(file_name:str) -> np.ndarray:
    """
    read and IDTable and return a numpy array
    :param file_name:
    :return: a IDTable in np.ndarray style
    """
    # print(os.getcwd())
    __IDtable = pd.read_csv(file_name)
    IDTable = __IDtable.values
    return IDTable

def CombinationLoader(file_name:str) -> dict:
    """
    read a
    :param file_name: the Combination.npy file name
    :return: a Combination dict with it's value aplitted into lists:
    like this:
    'a':['a','ai','an','ang','ao']
    """
    __combination = np.load(file_name,allow_pickle=True).tolist()
    for key in __combination.keys():
        # print(__combination[key])

        Combination = {}
        __combination[key] = __combination[key].split(',')

    return dict(__combination)


def nondictnpy2dict(filename:str) -> dict:
    __npyfile = np.load(filename,allow_pickle=True).tolist()
    npydict = {}
    for key in __npyfile:
        npydict[key] = __npyfile[key]
    print(type(npydict))
    return npydict

if __name__ == '__main__':

    # fn = r'dictionary_word.npy'
    # npyd = nondictnpy2dict(fn)
    # np.save(r'ndictionary_word.npy',npyd)
    file = 'dictionary_word.csv'
    csv_file = pd.read_csv(file)
    dict = {}
    for i in range(0, csv_file.shape[0]):
        dict[csv_file['Var1'][i]] = csv_file['Var2'][i]
    print(dict)
    np.save('ndictionary_word.npy',dict)
