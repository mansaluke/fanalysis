#import generatedata as g
#import structureforfinance as sff
#import plotting as p
#
#from datetime import datetime, timedelta
#import pandas as pd
#
#time_start = datetime.now()
#diff = 500
#time_end = time_start + timedelta(seconds = diff)
#
#df = g.create_data('s', date=time_start,
#                direction='Backwards', num_periods=diff).create_brownian_motion()
#
#df = g.append_data(df).create_brownian_motion()
#
#
#print(df.head())
#
#
#my_plot = p.graph_vars(df)
#my_plot.show()
#print(my_plot.header)
from models.random_forest import do_rf
import models.random_forest as rf
from models.optimize_random_forest import optimize_rf

from generatedata import create_data
import dfconvert as dfc
import structure as s
from plotting import graph_vars
import utils

from datetime import datetime, timedelta
import pandas as pd

if __name__ == "__main__":
    a=1
    indep_col='EURUSD.bid'
    df = dfc.df_store('EURUSD_tick_historicals_2019.h5').load_df()

    df = rf.drop_col(df, ['d2', 'd2', 'd3', 'd4', 'v'])

    utils.df_describe(df)

    if len(df) > 100000:
        df = df.sample(n=100000)
        
    df=df.reset_index()
    print(df.head())


    orf =  optimize_rf(df, n_estimators=100, indep_col = indep_col )  
    opt_n_estimators = orf.opt_n_estimators
    print('opt: {}'.format(opt_n_estimators))