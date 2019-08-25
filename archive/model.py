# import numpy as np
# from feature_engineer import df_final
# from zlib import crc32
# from sklearn.linear_model import SGDClassifier
# from sklearn.model_selection import cross_val_score, cross_val_predict
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler, CategoricalEncoder
# from sklearn.base import BaseEstimator, TransformerMixin
# from sklearn.impute import SimpleImputer
# from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score


# def test_set_check(indentifier, test_ratio):
#     return crc32(np.int64(indentifier)) & 0xffffffff < test_ratio *2**32


# def train_test(data, test_ratio, id_column):
#     ids = data[id_column]
#     in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
#     return data.loc[~in_test_set], data.loc[in_test_set]


# # rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6
# # class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
# #     def __init__(self, add_bedrooms_per_room = True): # no *args or **kargs
# #         self.add_bedrooms_per_room = add_bedrooms_per_room
# #     def fit(self, X, y=None):
# #         return self  # nothing else to do
# #     def transform(self, X, y=None):
# #         rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
# #         population_per_household = X[:, population_ix] / X[:, household_ix]
# #         if self.add_bedrooms_per_room:
# #             bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
# #             return np.c_[X, rooms_per_household, population_per_household,
# #                          bedrooms_per_room]
# #         else:
# #             return np.c_[X, rooms_per_household, population_per_household]


# class DataFrameSelector(BaseEstimator, TransformerMixin):
#     def __init__(self, attibute_names):
#         self.attribute_names = attibute_names
#     def fit(self, X, y=None):
#         return self
#     def transform(self, X):
#         return X[self.attribute_names].values


# # num_pipeline = Pipeline([
# #         ("selector", DataFrameSelector(num_attrib)),
# #         ("imputer", SimpleImputer(strategy="median")),
# #         # ("attribs_adder", CombinedAttributesAdder()),
# #         ("std_acaler", StandardScaler()),
# #     ])

# # cat_pipeline = Pipeline([
# #     ("selector", DataFrameSelector(cat_attrib)),
# #     ("cat_encoder", CategoricalEncoder(encoding="onehot-dense")),
# #     ])

# ### split into train and test sets
# target = "home.result.target"
# game_id = "gameID"
# train_set, test_set = train_test(df_final, 0.2, game_id)
# train_target, test_target = train_set[target], test_set[target]

# train_target_log, test_target_log = train_set[[game_id, target]], test_set[[game_id, target]]
# del train_set[target]
# del test_set[target]


# arr_train, arr_test = train_set.to_numpy(), test_set.to_numpy()
# arr_train_target, arr_test_target = train_target.to_numpy(), test_target.to_numpy()

# # print(arr_train.shape, type(arr_train))
# # print(arr_test.shape, type(arr_test))
# # print(arr_train_target.shape, type(arr_train_target))
# # print(arr_test_target.shape, type(arr_test_target))

# ### single game for evaluation
# # test_game = test_set.iloc[0,:]
# # arr_test_game = test_game.to_numpy()
# # arr_test_game = arr_test_game.reshape(1,-1)
# # print(sdg_clf.predict(arr_test_game))

# sdg_clf = SGDClassifier(random_state=999)
# sdg_clf.fit(arr_train, arr_train_target)


# result_pred = cross_val_predict(sdg_clf, arr_train, arr_train_target, cv=5)
# # print(result_pred)

# result_score = cross_val_score(sdg_clf, arr_train, arr_train_target, cv=2, scoring="accuracy")
# # print(result_score)

# result_conf = confusion_matrix(arr_train_target, result_pred)
# print(result_conf)

# print(precision_score(arr_train_target, result_pred))
# print(recall_score(arr_train_target, result_pred))
# print(f1_score(arr_train_target, result_pred))

