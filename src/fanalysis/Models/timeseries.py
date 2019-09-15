import pandas as pd 
import scipy
from scipy import linalg










if __name__ == "__main__":
    import sys, os
    parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)+ '../..'))
    if parentdir not in sys.path:
       sys.path.insert(0, parentdir)
    import structure as s
    from dfconvert import df_store
    df = df_store('data.h5').load_df()  
    df = df.sample(n=50000) 
    #df_properties(df['d1'])
    print(df['d1'].isnull().sum())