import pandas as pd 
import scipy
from sklearn.linear_model import LinearRegression









if __name__ == "__main__":
   import sys, os
   parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)+ '../..'))
   if parentdir not in sys.path:
      sys.path.insert(0, parentdir)
   import structure as s
   import generatedata as g
   from dfconvert import df_store
   import plotting as p
   df = df_store('data.h5').load_df()  
   print(df.head())

   rand = g.create_data('S', [pd.to_datetime(min(df['date'])), pd.to_datetime(max(df['date']))]).create_brownian_motion(start_price=1)
   #df = pd.concat([df, rand], axis = 1)
   df = df.merge(rand.reset_index(), left_on = 'date', right_on= 'Date', how = 'left')

   print(df.head())
   p.graph_vars(df, ['d1', 'bm']).plot()
   p.graph_vars(df, ['d1', 'bm'], pause=None).plot()

   #model = LinearRegression().fit(df[['d1', 'd2']], df['d2'])

