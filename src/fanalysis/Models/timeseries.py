import pandas as pd 
import scipy
from sklearn.linear_model import LinearRegression









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
      #df = df_store('data.h5').load_df()
      #print(df.head())  
      


