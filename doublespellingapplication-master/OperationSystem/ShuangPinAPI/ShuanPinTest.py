import numpy as np
import pandas as pd
import tables
from ShuangPinSystem.Utils import csv2df
from ShuangPinSystem.pinyin2ID import pinyin2ID

Combination = np.load(r'Combination.npy',allow_pickle=True).tolist()
dictionary_word = np.load(r'dictionary_word.npy',allow_pickle=True).tolist()
IDTable = pd.read_csv(r'IDTable.csv')
IDTable = np.array(IDTable.values)
ref_pinyin2ID_yunmu = np.load(r'reference_pinyin2ID_yunmu.npy',allow_pickle=True).tolist()


idArray = pinyin2ID(['w','o','c','ao'],IDTable)
print(idArray)
