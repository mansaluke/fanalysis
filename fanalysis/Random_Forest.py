import sys, os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_categorical_dtype
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import forest
from sklearn import metrics

import extract as e
import structure as s
import plotting
from dfconvert import df_store



def parallel_trees(rf, fn, n_jobs=4):
        return list(ThreadPoolExecutor(n_jobs).map(fn, rf.estimators_))


#tree sample size
def set_rf_samples(n):
        """ Changes Scikit learn's random forests to give each tree a random sample of
        n random rows.
        """
        forest._generate_sample_indices = (lambda rs, n_samples:
                forest.check_random_state(rs).randint(0, n_samples, n))

def reset_rf_samples():
        """ Undoes the changes produced by set_rf_samples.
        """
        forest._generate_sample_indices = (lambda rs, n_samples:
                forest.check_random_state(rs).randint(0, n_samples, n_samples))


#statistical calculations
def rmse(x,y): return np.sqrt(((x-y)**2).mean())

def print_score(rf, train_dependent, test_dependent, train_independent, test_independent):
        """
        prints train rmse, test rmse,
        r^2 train, test,
        oob_score_
        """
        res = ['RMSE of train:', rmse(rf.predict(train_dependent), train_independent),'RMSE of test:', rmse(rf.predict(test_dependent), test_independent),
                    'RF score (r^2) of train:', rf.score(train_dependent, train_independent), 'RF score (r^2) of (test)', rf.score(test_dependent, test_independent)]
        if hasattr(rf, 'oob_score_'): res.append('RF oob_score (r^2):', rf.oob_score_)
        print(res)


#structure
def fix_missing(df, col, name, na_dict):
        """ Fill missing data in a column of df with the median, and add a {name}_na column
        which specifies if the data was missing.
        Parameters:
        -----------
        df: The data frame that will be changed.
        col: The column of data to fix by filling in missing data.
        name: The name of the new filled column in df.
        na_dict: A dictionary of values to create na's of and the value to insert. If
            name is not a key of na_dict the median will fill any missing data. Also
            if name is not a key of na_dict and there is no missing data in col, then
            no {name}_na column is not created.
        Examples:
        ---------
        >>> df = pd.DataFrame({'col1' : [1, np.NaN, 3], 'col2' : [5, 2, 2]})
        >>> df
           col1 col2
        0     1    5
        1   nan    2
        2     3    2
        >>> fix_missing(df, df['col1'], 'col1', {})
        >>> df
           col1 col2 col1_na
        0     1    5   False
        1     2    2    True
        2     3    2   False
        >>> df = pd.DataFrame({'col1' : [1, np.NaN, 3], 'col2' : [5, 2, 2]})
        >>> df
           col1 col2
        0     1    5
        1   nan    2
        2     3    2
        >>> fix_missing(df, df['col2'], 'col2', {})
        >>> df
           col1 col2
        0     1    5
        1   nan    2
        2     3    2
        >>> df = pd.DataFrame({'col1' : [1, np.NaN, 3], 'col2' : [5, 2, 2]})
        >>> df
           col1 col2
        0     1    5
        1   nan    2
        2     3    2
        >>> fix_missing(df, df['col1'], 'col1', {'col1' : 500})
        >>> df
           col1 col2 col1_na
        0     1    5   False
        1   500    2    True
        2     3    2   False
        """
        if is_numeric_dtype(col):
            if pd.isnull(col).sum() or (name in na_dict):
                df[name+'_na'] = pd.isnull(col)
                filler = na_dict[name] if name in na_dict else col.median()
                df[name] = col.fillna(filler)
                na_dict[name] = filler
        return na_dict

def mean_col(df, col):
   """add a column with the mean if not exists
   """
   if 'mean' in map(lambda x:x.lower(),df.columns.tolist()):
      pass
   else:
      df['mean'] =  df.loc[:,col].mean()


def drop_col(df, col_names):
   for col in col_names:
      if col in df.columns:
         df = df.drop(col, axis = 1)
   return df


def dectree_max_depth(tree):
   """gives max tree depth:
   for one tree: 
   t=rf.estimators_[0].tree_
   dectree_max_depth(t)
   for all:
   [dectree_max_depth(tn.tree_) for tn in rf.estimators_]
   """
   children_left = tree.children_left
   children_right = tree.children_right
   def walk(node_id):
       if (children_left[node_id] != children_right[node_id]):
           left_max = 1 + walk(children_left[node_id])
           right_max = 1 + walk(children_right[node_id])
           return max(left_max, right_max)
       else: # leaf
           return 1
   root_node_id = 0
   return walk(root_node_id)




class do_rf():
   """create rf predictions with 1 line of code e.g. do_rf(df, n_estimators=1).predict_train()[0]
   """
   def __init__(self,
                df,
                indep_col = 'Bar OPEN Bid Quote',
                test_size = 0.25,
                sample_random_state = 42,
                n_estimators=40,
                criterion="mse",
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=3,
                min_weight_fraction_leaf=0.,
                max_features=0.5,
                max_leaf_nodes=None,
                min_impurity_decrease=0.,
                min_impurity_split=None,
                bootstrap=True,
                oob_score=True,
                n_jobs=-1,
                random_state=None,
                verbose=0,
                warm_start=False):

      #start rf class
      self.rf = RandomForestRegressor(n_estimators,criterion,max_depth,min_samples_split \
         ,min_samples_leaf,min_weight_fraction_leaf,max_features,max_leaf_nodes \
            ,min_impurity_decrease ,min_impurity_split)

      #define variables
      self.df = df
      self.n_estimators = n_estimators
      self.labels = df[indep_col]                 
      self.test_size = test_size
      self.sample_random_state = sample_random_state
      self.indep_col = indep_col

      #define dataframes
      self.features = self.feature_adjust_dataframe(self.df, self.indep_col)
      self.train_dependent, self.test_dependent, self.train_independent, self.test_independent = self.split_df()



   def feature_adjust_dataframe(self, df, indep_col):
      """
      add mean, remove independent variable, apply pandas.get_dummies and fill null values with mean
      """
      features = self.df

      try:
         mean_col(features, indep_col)
      except:
         print("Add mean col funcion has failed.")
         pass

      try:
         to_drop = ['date', 'Bar OPEN Bid Quote', 'Bar HIGH Bid Quote', 'Bar LOW Bid Quote', 'Bar CLOSE Bid Quote']
         to_drop.append(indep_col)
         features = features.drop(indep_col, axis = 1) 
         features = drop_col(features, to_drop)
      except: 
         raise ValueError('Column: ', indep_col, ', could not be dropped from axis')

      try:
         features = pd.get_dummies(features)
      except:
         print('pandas get_dummies function has failed.')
         pass  
      
      for col in features: 
         try:
            r.fix_missing(features, features[col], col, {})
         except:
            pass

      return features

   def split_df(self): 
      return train_test_split(self.features, self.labels, test_size = self.test_size, random_state=self.sample_random_state) 

   def split_shape(self): 
      return self.train_dependent.shape, self.test_dependent.shape, self.train_independent.shape, self.test_independent.shape  

   def draw(self, size=10, ratio=0.6, precision=0, max_depth=3):
      plotting.draw_tree(self.rf.estimators_[self.n_estimators-1], list(self.features.columns), size=size, ratio=ratio, precision=precision, max_depth=max_depth)

   def predict_out(self, graph = False):
      self.rf.fit(self.train_dependent, self.train_independent)
      self.predictions = self.rf.predict(self.test_dependent)
       
      if graph == True:
         self.graph_predictions()
      
      return self.predictions #, self.baseline_errors, rfprediction_errors

   def graph_predictions(self):

      
      test_dates =pd.to_datetime(self.test_dependent[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])
      #self.test_dependent['prediction'] = self.predict_out()

      prediction_data = pd.DataFrame(data = {'date': test_dates, 'prediction': self.predict_out()})


      fig, ax = plt.subplots()
      ax.plot(self.df['date'], self.df[self.indep_col], 'b.', label = 'actual')
      ax.plot(prediction_data['date'], prediction_data['prediction'], '.', label = 'prediction')
      # rotate and align the tick labels so they look better
      #fig.autofmt_xdate()
      # use a more precise date string for the x axis locations in the
      # toolbar
      #ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
      ax.set_title('Actual and Predicted Values'); plt.xlabel('Date'); plt.ylabel('rate')
      plt.show()

   def error_calc(self, predictions, label_sample):
      return abs(predictions - label_sample)

   def return_error_details(self, to_return = 'mean'):

      baseline_errors = self.error_calc(self.features['mean'], self.test_independent)
      rfprediction_errors = self.error_calc(self.predict_out(), self.test_independent)

      mean_baseline_error = np.mean(baseline_errors)
      mean_rfprediction_error = np.mean(rfprediction_errors)

      mean_error_difference = mean_baseline_error - mean_rfprediction_error

      mape = (rfprediction_errors / self.test_independent) *100
      accuracy = 100 - np.mean(mape)
      
      if to_return =='all':
         return 'basline errors', baseline_errors, \
               'rfprediction_errors', rfprediction_errors, \
               'mean_baseline_error', mean_baseline_error, \
               'mean_rfprediction_error', mean_rfprediction_error, \
               'mean_error_difference', mean_error_difference 
      else:
         print('mean_baseline_error:', mean_baseline_error, 'mean_rfprediction_error:', mean_rfprediction_error, 'mean_error_difference:', mean_error_difference, \
            'accuracy (100-MAPE):', accuracy, '%')

   def print_score(self):
      print_score(self.rf, self.train_dependent, self.test_dependent, self.train_independent, self.test_independent)   

   def tree_preds(self, n_jobs=4):
      """ get predictions of each tree
      """
      def get_preds(t): return t.predict(self.test_dependent)
      
      t_preds = np.stack(parallel_trees(self.rf, get_preds, n_jobs))

      plt.plot([metrics.r2_score(self.test_independent, np.mean(t_preds[:i+1], axis=0)) for i in range(self.n_estimators)])

      return t_preds

   def importances(self):
      importances = list(self.rf.feature_importances_)
      print(importances)
      feature_importances = [(feature, importance) for feature, importance in zip (list(self.features.columns), importances)]
      feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
      [print('variable: {:20} importance : {}'.format(*pair)) for pair in feature_importances if pair[1] != 0]
      plt.style.use('fivethirtyeight')
      x_values=list(range(len(importances)))
      plt.bar(x_values, importances, orientation='vertical')
      plt.xticks(x_values, list(self.features.columns), rotation='vertical')
      plt.ylabel('Importance');plt.xlabel('Variable');plt.title('var importance')

   def feature_analysis(self, col):
      x = self.df.sample(n = self.split_shape()[0][0]) 
      x['prediction_std'] = np.std(self.predict_out(), axis=0).size
      x['prediction'] = np.mean(self.predict_out(), axis=0)
      x[col].value_counts().plot.barh()

      flds = [col, self.indep_col, 'prediction', 'prediction_std']
      print(x[flds].groupby(col, as_index=False).mean())




if __name__ == "__main__":
   pass
