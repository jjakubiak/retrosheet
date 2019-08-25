
import numpy as np
from zlib import crc32
from sklearn.base import BaseEstimator, TransformerMixin
from feature_engineer import df_boxscore_final 


def test_set_check(indentifier, test_ratio):
    return crc32(np.int64(indentifier)) & 0xffffffff < test_ratio *2**32


def train_test(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attibute_names):
        self.attribute_names = attibute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values