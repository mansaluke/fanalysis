

try:
    from fanalysis.Models.optimize import optimize_rf
    from fanalysis.Models.Random_Forest import do_rf
    import fanalysis.Download.downloadhistoricals as dh
    import fanalysis.Models.Random_Forest as rf
except ImportError:
    from Models.optimize import optimize_rf
    from Models.Random_Forest import do_rf
    import Download.downloadhistoricals as dh
    import Models.Random_Forest as rf
from generatedata import data
import dfconvert as dfc
import structure as s
from plotting import plots

from datetime import datetime, timedelta
import pandas as pd
import pickle

dfc.get_path()



df = dfc.df_store('c').load_df()
#df =df.reset_index()
df = s.date_split(df)


print(df.head())
print(len(df))
dfc.df_store('data.h5').store_df(df)

df = dfc.df_store('data.h5').load_df()
print(df.head())

#import os
#
#scores = {} # scores is an empty dict already
#
#if os.path.getsize(target) > 0:      
#    with open(target, "rb") as f:
#        unpickler = pickle.Unpickler(f)
#        # if file is not empty scores will be equal
#        # to the value unpickled
#        scores = unpickler.load()

