try:
    from fanalysis.Models.optimize import optimize_rf
    from fanalysis.Models.Random_Forest import do_rf
    import fanalysis.Download.downloadhistoricals as dh
except ImportError:
    from Models.optimize import optimize_rf
    from Models.Random_Forest import do_rf
    import Download.downloadhistoricals as dh
from generatedata import data
import dfconvert as dfc
import structure as s
from plotting import plots

from datetime import datetime, timedelta
import pandas as pd



df = dfc.df_store('EURUSD_tick_historicals.feather').load_df()
print(df.head())
print(len(df))
dfc.df_store('EURUSD_tick_historicals.h5').store_df(df)





