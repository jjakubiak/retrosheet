
# import numpy as np
# # import matplotlib.pyplot as plt
# from zlib import crc32
# from pandas.plotting import scatter_matrix
# # from process_df import df_final
# from sklearn.utils import shuffle
# from sklearn.linear_model import SGDClassifier



# def test_set_check(indentifier, test_ratio):
#     return crc32(np.int64(indentifier)) & 0xffffffff < test_ratio *2**32

# def train_test(data, test_ratio, id_column):
#     ids = data[id_column]
#     in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
#     return data.loc[~in_test_set], data.loc[in_test_set]



# ### correlation coefficients
# corr_matrix = df_final.corr()
# corr = corr_matrix["home_result_ind"].sort_values(ascending=False)
# # print(corr.nlargest(20))
# # print(corr.nsmallest(20))




# target_df = df_final[["gameID", "home_result_ind"]]
# target_df.set_index("gameID", inplace=True)
# target_df["target"] = np.where(target_df["home_result_ind"] == 1, True, False)
# target_df.drop("home_result_ind", axis=1, inplace=True)
# # print(target_df)

# df_final.drop("home_result_ind", axis=1, inplace=True)
# # train_set, test_set = train_test(df_final, 0.2, "gameID")

# # print(train_ind)

# ### shuffle data
# # train_set = shuffle(train_set)
# # test_set = shuffle(test_set)



# sdg_clf = SGDClassifier(random_state=999)
# # sgd_clf.fit(train_set, )


# ### write pandas dataframe to excel
# # file_nm = "corr"
# # save_to = "c:/retrosheet/api_structure_" + file_nm + ".xlsx"
# # writer = corr.ExcelWriter(save_to)
# # corr.to_excel(writer,'Sheet1')
# # writer.save()

# ### corr matrix
# attributes = ["home_result_ind"
# , "home.teamStats.batting.wOBA"
# , "home.teamStats.batting.wRAA"
# , "home.teamStats.batting.babip"

# ]



# ### histogram, fix to limit values
# # df_final.hist(bins=50, figsize=(20,15))
# # plt.show()

# ### check test and train set
# # print(len(train_set), ";", len(test_set))
# # print(train_set["gameID"])
# # print(test_set["gameID"])