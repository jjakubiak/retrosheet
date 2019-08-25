
import numpy as np
from process_df import df_final
from zlib import crc32
from sklearn.linear_model import SGDClassifier
from sklearn.impute import SimpleImputer


def test_set_check(indentifier, test_ratio):
    return crc32(np.int64(indentifier)) & 0xffffffff < test_ratio *2**32


def train_test(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]

### update in process_df
def target(row):
    if row["home_result_ind"] == 1:
        result = True
    else:
        result = False
    return result

### add target field
df_final["target"] = df_final.apply(target, axis=1)
df_final.drop("home_result_ind", axis=1, inplace=True)
df_final.set_index("gameID", inplace=True, drop=False)


### split into train and test sets
train_set, test_set = train_test(df_final, 0.2, "gameID")

### split target into train and test sets
train_target, test_target = train_set["target"], test_set["target"]

train_set.drop("target", axis=1, inplace=True)
test_set.drop("target", axis=1, inplace=True)

print(train_set.shape, type(train_set))
print(test_set.shape, type(test_set))
print(train_target.shape, type(train_set))
print(test_target.shape, type(test_set))

### impute null value on training set
# null_col = train_set.columns[train_set.isnull().any()].tolist()
# imputer = SimpleImputer(strategy="median")

# temp = test_set.loc[529566,:]
# numpy_matrix = temp.values
# numpy_matrix.reshape(1, -1)
# print(type(temp))
# print(type(train_set))

# sdg_clf = SGDClassifier(random_state=999)
# sdg_clf.fit(train_set, train_target)

# print(sdg_clf.predict(numpy_matrix))



