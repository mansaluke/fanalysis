import pandas as pd 
import scipy
import statsmodels.api as sm

import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

def decompose(y):

   from pylab import rcParams
   rcParams['figure.figsize'] = 18, 8
   decomposition = sm.tsa.seasonal_decompose(y, freq = 5, model='additive')
   plt = decomposition.plot()
   plt.show()


if __name__ == "__main__":
      import numpy as np
      from pandas import DataFrame
      import sys, os
      parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)+ '../..'))
      if parentdir not in sys.path:
         sys.path.insert(0, parentdir)
      import structure as s
      import generatedata as g
      from generatedata import create_data
      from dfconvert import df_store
      import plotting as p
      import utils


      #df = df_store('data.h5').load_df()
      indep_col='EURUSD.bid'
      df = df_store('EURUSD_tick_historicals_2019_post.h5').load_df()
      date_col = 'Date'

      #we only use the independant col and date column as the index
      df = df[[date_col, indep_col]].set_index(date_col)

      utils.df_describe(df)

      df = df[indep_col].resample('MS').mean()
      print(df.head())

      decompose(df)
      #print(df.head())  
      


