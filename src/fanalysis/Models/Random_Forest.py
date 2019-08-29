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

def print_score(rf, train_dependent, valid_dependent, train_independent, valid_independent):
        """
        prints train rmse, valid rmse,
        r^2 train, valid,
        oob_score_
        """
        res = ['RMSE of train:', rmse(rf.predict(train_dependent), train_independent),'RMSE of valid:', rmse(rf.predict(valid_dependent), valid_independent),
                    'RF score (r^2) of train:', rf.score(train_dependent, train_independent), 'RF score (r^2) of (valid)', rf.score(valid_dependent, valid_independent)]
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

def draw_tree(tr, df_cols, size=10, ratio=0.6, precision=0, max_depth=3):
    """ Draws a representation of a random forest in IPython.
    Parameters:
    -----------
    t: The tree you wish to draw
    df_cols: The data used to train the tree. This is used to get the names of the features.
    """
    from sklearn.tree import export_graphviz 
    import pydotplus
    import IPython.display
    import graphviz
    import re
    s=export_graphviz(tr, max_depth=max_depth, out_file=None, feature_names=df_cols, filled=True, rounded = True,
                      special_characters=True, rotate=True, precision=precision)
    display(graphviz.Source(re.sub('Tree {',
       f'Tree {{ size={size}; ratio={ratio}', s)))



class do_rf():
   """create rf predictions with 1 line of code e.g. do_rf(df, n_estimators=1).predict_train()[0]
   """
   def __init__(self,
                df,
                indep_col = 'Bar OPEN Bid Quote',
                valid_size = 0.25,
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
      self.valid_size = valid_size
      self.sample_random_state = sample_random_state
      self.indep_col = indep_col
      self.available_date_cols = [x for x in \
         ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second'] if x in list(df.columns)]
      self.date_col = self.df.select_dtypes(include=[np.datetime64]).columns[0]

      #define dataframes
      self.features = self.feature_adjust_dataframe(self.df, self.indep_col, self.date_col)
      self.train_dependent, self.valid_dependent, self.train_independent, self.valid_independent = self.split_df()
      self.predictions = self.predict_out(False)


   def feature_adjust_dataframe(self, df, indep_col, date_col):
      """
      add mean, remove independent variable, apply pandas.get_dummies and fill null values with mean
      """
      features = self.df

      try:
         mean_col(features, indep_col)
      except:
         print("Add mean col function has failed.")
         pass

      try:
         to_drop = \
            ['Bar OPEN Bid Quote', 'Bar HIGH Bid Quote', 'Bar LOW Bid Quote', 'Bar CLOSE Bid Quote', indep_col, date_col]
         #features = features.drop(indep_col, axis = 1) 
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
      indep_col = self.indep_col
      prop = self.valid_size
      #return train_test_split(self.features, self.labels, test_size = self.valid_size, random_state=self.sample_random_state) 
      return self.features[:round(len(self.features) *(1-prop))], \
         self.features[round(len(self.features) * (1-prop)):], \
         self.labels[:round(len(self.features) *(1-prop))], \
         self.labels[round(len(self.features) * (1-prop)):]

   @property
   def split_shape(self): 
      return self.train_dependent.shape, self.valid_dependent.shape, self.train_independent.shape, self.valid_independent.shape  

   def draw(self, size=10, ratio=0.6, precision=0, max_depth=3):
      draw_tree(self.rf.estimators_[self.n_estimators-1], list(self.features.columns), size=size, ratio=ratio, precision=precision, max_depth=max_depth)

   def predict_out(self, graph = True):
      self.rf.fit(self.train_dependent, self.train_independent)
      self.predictions = self.rf.predict(self.valid_dependent)

      if graph == True:
         self.graph_predictions()
      
      return self.predictions

   def graph_predictions(self):

      test_dates =pd.to_datetime(self.train_dependent[self.available_date_cols])
      valid_dates =pd.to_datetime(self.valid_dependent[self.available_date_cols])
      #maxd=valid_dates = max(df['Date'])
      #self.valid_dependent['prediction'] = self.predictions
      fitted_data = pd.DataFrame(data = {self.date_col: test_dates, 'fit': self.rf.predict(self.train_dependent)})
      prediction_data = pd.DataFrame(data = {self.date_col: valid_dates, 'prediction': self.predictions})
      fig, ax = plt.subplots()
      ax.plot(self.df[self.date_col], self.df[self.indep_col], 'b.', label = 'actual')
      ax.plot(fitted_data[self.date_col], fitted_data['fit'], 'r.', label = 'fit')
      ax.plot(prediction_data[self.date_col], prediction_data['prediction'], 'g.', label = 'prediction')
      fig.autofmt_xdate()
      ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
      ax.set_title('Actual and Predicted Values'); plt.xlabel(self.date_col); plt.ylabel('rate')
      plt.show()

   def out_of_sample_pred(self, sample_to_predict, graph =True):

      sample_to_predict_dates =pd.to_datetime(sample_to_predict[self.date_col])
      sample_to_predict = sample_to_predict.loc[:, sample_to_predict.columns != self.date_col]
      fitted_data = pd.DataFrame(data = {self.date_col: sample_to_predict_dates, 'oos_pred': self.rf.predict(sample_to_predict)})

      if graph == True:
         fig, ax = plt.subplots()
         ax.plot(fitted_data[self.date_col], fitted_data['oos_pred'], 'r.', label = 'fit')
         fig.autofmt_xdate()
         ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
         ax.set_title('Out of sample pred'); plt.xlabel(self.date_col); plt.ylabel('rate')
         plt.show()
      return fitted_data

   def error_calc(self, predictions, label_sample):
      return abs(predictions - label_sample)

   def return_error_details(self, to_return = 'mean'):

      baseline_errors = self.error_calc(self.features['mean'], self.valid_independent)
      rfprediction_errors = self.error_calc(self.predictions, self.valid_independent)
      mean_baseline_error = np.mean(baseline_errors)
      mean_rfprediction_error = np.mean(rfprediction_errors)
      mean_error_difference = mean_baseline_error - mean_rfprediction_error
      mape = (rfprediction_errors / self.valid_independent) *100
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
      print_score(self.rf, self.train_dependent, self.valid_dependent, self.train_independent, self.valid_independent)   

   def tree_preds(self, n_jobs=4, graph = True):
      """ get predictions of each tree
      """
      def get_preds(t): return t.predict(self.valid_dependent)
      
      t_preds = np.stack(parallel_trees(self.rf, get_preds, n_jobs))
      all_preds = [metrics.r2_score(self.valid_independent, np.mean(t_preds[:i+1], axis=0)) for i in range(self.n_estimators)]
      
      if graph ==True:
         plt.plot(all_preds)
      #return t_preds
      return all_preds

   def importances(self, graph = True):

      importances = list(self.rf.feature_importances_)
      feature_importances = [(feature, importance) for feature, importance in zip (list(self.features.columns), importances)]
      feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
      [print('variable: {:20} importance : {}'.format(*pair)) for pair in feature_importances if pair[1] != 0]

      if graph == True:
         plt.style.use('fivethirtyeight')
         x_values=list(range(len(importances)))
         plt.bar(x_values, importances, orientation='vertical')
         plt.xticks(x_values, list(self.features.columns), rotation='vertical')
         plt.ylabel('Importance');plt.xlabel('Variable');plt.title('var importance')

      return feature_importances

   def feature_analysis(self, col, graph = True):

      x = self.df.sample(n = self.split_shape[0][0]) 
      x['prediction_std'] = np.std(self.predictions, axis=0).size
      x['prediction'] = np.mean(self.predictions, axis=0)

      if graph == True:
         x[col].value_counts().plot.barh()

      flds = [col, self.indep_col, 'prediction', 'prediction_std']
      summ = x[flds].groupby(col, as_index=False).mean()

      return (summ.prediction_std/summ.prediction).sort_values(ascending=False)





if __name__ == "__main__":
   import sys, os
   parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)+ '../..'))
   if parentdir not in sys.path:
      sys.path.insert(0, parentdir)
   import structure as s
   from dfconvert import df_store
   df = df_store('EURUSD_tick_historicals_aug.h5').load_df()
   
   df = df.sample(n=50000)
   def drop_col(df, col_names):
       for col in col_names:
           if col in df.columns:
               df = df.drop(col, axis = 1)
       return df
   df = df.reset_index()
   print(df.head())
   df = s.date_split(df)
   df = drop_col(df, ['aggdays', 'daysinmonth', 'Bar OPEN Bid Quote_lag-1'])
   print(df.head())
   rf = do_rf(df, 'EURUSD.bid', n_estimators=5)
   print(rf.available_date_cols)
   print(1)
   rf.predict_out(True)
   print(2)
   rf.return_error_details()
   rf.print_score()
   rf.importances()
   rf.tree_preds()
