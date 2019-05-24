# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 14:37:11 2019

@author: Luke
"""

# =============================================================================
# descriptive analysis
# 
# =============================================================================
x = 2

import extract as e
import structure as s
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import dfconvert as dfC
from plotting import plots
if x == 1:
    import main
    df = dfC.storage_to_df('x.json').file
    print(df.head())
elif x == 2: 
    df = e.use_csvs()

df = s.date_split(df)
df = s.add_rand(df)

#plots(df, None)

df['average'] = df.mean(numeric_only=True, axis=1)

print(df.describe())
features = pd.get_dummies(df)
print(features.head(5))
#print(features.iloc[:,10006:].head(5))
print(features.iloc[:,0:5].head(5))

def drop_col(df, col_names):
    for col in col_names:
        if col in df.columns:
            df = df.drop(col, axis = 1)
    return df

features = drop_col(features, ['date', 'd2', 'd3', 'd4'])


if 'd1' in features:
    labels = np.array(features['d1'])
    features = features.drop('d1', axis = 1)
elif 'rnd' in features:
    labels = np.array(features['rnd'])
    features = features.drop('rnd', axis = 1)

feature_list = list(features.columns)
print(feature_list)
features = np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state=42)
print(train_features.shape)
print(test_features.shape)
print(train_labels.shape)
print(test_labels.shape)

#historical average
baseline_preds = test_features[:,feature_list.index('average')]
baseline_errors = abs(baseline_preds - test_labels)

print('av basline error: ', round(np.mean(baseline_errors), 2))

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=5, random_state=42, max_depth=4, n_jobs=-1)
rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)
errors = abs(predictions - test_labels)
print('mean absolute error: ', round(np.mean(errors), 2), 'degrees.')


mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)
print('accuracy:', round(accuracy, 2), '%.')


###################################################
#install pydot
##################################################
from sklearn.tree import export_graphviz 
#from sklearn.tree import pydot
#import pydot
import pydotplus
#from sklearn import pydot

tree= rf.estimators_[3]
export_graphviz(tree, out_file = 'tree.dot', feature_names=feature_list, rounded = True, precision=1)
graph = pydotplus.graph_from_dot_file('tree.dot')
#graph.write_png('tree.png')
#Image(graph.create_png())


importances = list(rf.feature_importances_)
print(importances)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip (feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('variable: {:20} importance : {}'.format(*pair)) for pair in feature_importances]

important_indices = [feature_list.index('aggdays'), feature_list.index('average')]
train_important=train_features[:,important_indices]
test_important=test_features[:,important_indices]
rf.fit(train_important, train_labels)
predictions= rf.predict(test_important)
errors = abs(predictions-test_labels)
print(errors)

import matplotlib.pyplot as plt
#%matplotlib inline

plt.style.use('fivethirtyeight')
x_values=list(range(len(importances)))
plt.bar(x_values, importances, orientation='vertical')
plt.xticks(x_values, feature_list, rotation='vertical')
plt.ylabel('Importance')
plt.xlabel('Variable')
plt.title('var importance')

years = test_features[:, feature_list.index('year')]
months = test_features[:feature_list.index('month')]
days = test_features[:, feature_list.index('day')]
print(years)
print(months)
print(days)
print( zip(years, months, days))
test_dates = [str(int(year)) + '-' + str(int(month))+'-' + str(int(day)) for year, month, day in zip(years, months, days)]

test_dates = [datetime.strftime(date, '%Y-%m-%d') for date in test_dates]
prediction_data = pd.DataFrame(data = {'date': test_dates, 'prediction': predictions})

plt.plot(prediction_data['prediction'], 'ro', label = 'prediction')
plt.xticks(rotation  = '60')
plt.ylabel('date')
plt.xlabel('actual and predicted')




