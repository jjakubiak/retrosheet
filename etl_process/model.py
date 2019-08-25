
from feature_engineer import df_boxscore_final
from model_operations import train_test
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
import pandas as pd
from operations import df_to_excel
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score


target = "home.result.target"
game_id = "gameID"


### split into train and test sets
train_set, test_set = train_test(df_boxscore_final, 0.2, game_id)
train_target, test_target = train_set[target], test_set[target]

### keep table of gameID and result
train_target_log, test_target_log = train_set[[game_id, target]], test_set[[game_id, target]]
del train_set[target]
del test_set[target]
del train_set[game_id]
del test_set[game_id]

### convert dataframe to numpy array
arr_train, arr_test = train_set.to_numpy(), test_set.to_numpy()
arr_train_target, arr_test_target = train_target.to_numpy(), test_target.to_numpy()


### instantiate and fit the sgd classifier model
sdg_clf = SGDClassifier(random_state=999, tol=1e-3, max_iter=1000)
sdg_clf.fit(arr_train, arr_train_target)
sdg_result_pred = cross_val_predict(sdg_clf, arr_train, arr_train_target, cv=3)
# print(sdg_result_pred)

# sdg_result_score = cross_val_score(sdg_clf, arr_train, arr_train_target, cv=3, scoring="accuracy")
# print(sdg_result_score)

sdg_result_conf = confusion_matrix(arr_train_target, sdg_result_pred)
print(sdg_result_conf)

# score metrics for sdg classifier
sgd_accuracy = accuracy_score(arr_train_target, sdg_result_pred)
sgd_precision = precision_score(arr_train_target, sdg_result_pred)
sgd_recall = recall_score(arr_train_target, sdg_result_pred)
sgd_f1_score = f1_score(arr_train_target, sdg_result_pred)


### instantiate and fit random forest classifier
forest_clf = RandomForestClassifier(random_state=999, n_estimators=100)

### returns a row per instance and a column per class, representing the probabilty that an instance belong to a class
### in this case the classes are negative (column 0) and posative (column 1)
forest_prob_pred = cross_val_predict(forest_clf, arr_train, arr_train_target, cv=3, method="predict_proba")

### probability of the posititve class
forest_result_pos = forest_prob_pred[:, 1]

### threshold of 0.5
forest_result_pred = forest_result_pos > 0.5
# print(forest_result_pred)

# score metrics for random forest classifier
### instantiate and fit random forest classifier
forest_accuracy = accuracy_score(arr_train_target, forest_result_pred)
forest_precision = precision_score(arr_train_target, forest_result_pred)
forest_recall = recall_score(arr_train_target, forest_result_pred)
forest_f1_score = f1_score(arr_train_target, forest_result_pred)

### print metrics score metrics
print("\n sdg_classifier:"
      "\n accuracy: ", sgd_accuracy,
      "\n prescision: ", sgd_precision,
      "\n recall: ", sgd_recall,
      "\n f1_score: ", sgd_f1_score,
      "\n\n forest_classifier:",
      "\n accuracy: ", forest_accuracy,
      "\n prescision: ", forest_precision,
      "\n recall: ", forest_recall,
      "\n f1_score: ", forest_f1_score
      )

### write pandas dataframe to excel
# df_arr_train = pd.DataFrame(arr_train)
# df_arr_test = pd.DataFrame(arr_test)
# df_arr_train_target = pd.DataFrame(arr_train_target)
# df_arr_test_target = pd.DataFrame(arr_test_target)

# df_to_excel("train_set", "c:/retrosheet/api_structure", train_set)
# df_to_excel("test_set", "c:/retrosheet/api_structure", test_set)
# df_to_excel("train_target", "c:/retrosheet/api_structure", train_target)
# df_to_excel("test_target", "c:/retrosheet/api_structure", test_target)

# df_to_excel("train_target_log", "c:/retrosheet/api_structure", train_target_log)
# df_to_excel("test_target_log", "c:/retrosheet/api_structure", test_target_log)

# df_to_excel("arr_train", "c:/retrosheet/api_structure", df_arr_train)
# df_to_excel("arr_test", "c:/retrosheet/api_structure", df_arr_test)
# df_to_excel("arr_train_target", "c:/retrosheet/api_structure", df_arr_train_target)
# df_to_excel("arr_test_target", "c:/retrosheet/api_structure", df_arr_test_target)
