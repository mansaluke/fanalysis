
try:
    from fanalysis.models.optimize_random_forest import optimize_rf
    from fanalysis.models.random_forest import do_rf
    import fanalysis.download.downloadhistoricals as dh
    import fanalysis.models.random_forest as rf
except ImportError:
    from models.optimize_random_forest import optimize_rf
    from models.random_forest import do_rf
    import download.downloadhistoricals as dh
    import models.random_forest as rf
from generatedata import create_data
import dfconvert as dfc
import structure as s
from plotting import graph_vars
import utils

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

import threading


def download(start_date, finish_date):
    return dh.generate_market_data_for_tests(start_date, finish_date)



def test_split_df(df, date_col='Date', prop = 0.25):
    df.sort_values(by=[date_col], inplace=True)
    return df[:round(len(df) *(1-prop))], df[round(len(df) * (1-prop)):]


def update_decorator(func): 
    hmax, nmax = self.hmax, self.nmax
    def update_after(*args, **kwargs): 
        print("before execution") 
        # getting the returned value 
        returned_value = func(*args, **kwargs) 
        print("after execution: initiate update") 
        print(hmax, nmax)
        # returning the value to the original frame 
        return returned_value 
    update_df
    return update_after 



class run_pred():
    """
    continuously runs optimization modules and extracts output (for now just optimize_random_forest) 
    """
    def __init__(self, df, indep_col, date_col=None):
        self.df = df
        self.indep_col = indep_col
        self.max_estimators = 10
        self.opt_n_estimators = self.opt_estimator_fn()
        
        if date_col == None:
            try:
                self.date_col = self.df.select_dtypes(include=[np.datetime64]).columns[0]
            except:
                raise AttributeError('No date column found')
        else:
            self.date_col = date_col
        print(self.df.head())
        print('date col: ', date_col)
        print(self.date_col)
        self.hmax, self.nmax = self.update_times()

    def update_times(self):
        start_date = self.df[self.date_col].max()
        finish_date = datetime.now()
        print(start_date, finish_date)
        print('updating: ' , finish_date - start_date)
        return start_date, finish_date

    def update_df(self):
        #make sure historicals are up-to-date
        start_date, finish_date = self.hmax, self.nmax

        #try:
        df_latest = download(start_date, finish_date)
        print('new data: ')
        print(df_latest.head())
        df_latest = df_latest.reset_index()
        df_latest = s.date_split(df_latest)
        rf.fix_missing(df_latest, df_latest[indep_col], indep_col, {})
        self.df = pd.concat([self.df, df_latest], keys = list(df.columns), ignore_index=True, sort=False)
        print('new data has been joined to df')
        return self.df
        #except:
        #    print('Could not update')


    def opt_estimator_fn(self):
        """optimizes rf model"""
        max_estimators=100
        #df, test = test_split_df(df)
        orf =  optimize_rf(self.df, n_estimators=self.max_estimators, indep_col = indep_col )        
        opt_n_estimators = orf.opt_n_estimators
        print('opt: {}'.format(opt_n_estimators))
        return opt_n_estimators

    def create_pred(self):    
        """creates predictions using opt no. estimators on validation set."""
        
        rf = do_rf(self.df, n_estimators=self.opt_n_estimators, indep_col = indep_col)
        preds = rf.predict_out(graph=False)
        rf.return_error_details()
        rf.print_score()
        rf.importances(graph=False)
        return preds

        #task = threading.Thread(target=self.update_df, args=(self.hmax, self.nmax))
        #task.daemon = True
        #task.start()
        #return pd.DataFrame(preds)


    def oos_pred(self):
        #create_data('S', date = [self.hmax, datetime.now()]).gendateseries()
        print(self.df.head())
        osd = self.df[date_col][self.df[date_col]>=self.hmax]
        print(osd.head())
        #osd = create_data("S", "Forward").gendateseries()
        #osd = s.date_split(osd, time=False)
        return rf.out_of_sample_pred(osd)
        


if __name__ == "__main__":

    indep_col='EURUSD.bid'
    df = dfc.df_store('EURUSD_tick_historicals_2019_post.h5').load_df()
    date_col = 'Date'

    utils.df_describe(df)

    print('entering loop')

    while 1==1:

        # by initiating the run_pred class we find the optimal number of trees in the existing dataset 
        # and we identify the difference between the end point of the historical data and our current date.
        # this is used later to update our dataset
        rp = run_pred(df, indep_col)
        print('here')

        #run model on historicals using the optimal number of trees. out-of-sample preds are assigned to variable oosp
        oosp = rp.create_pred()
        print('out-of-sample preds:')
        print(oosp.head())

        print('updating dataframe with the latest data')
        #try:
        df = rp.update_df()
        print(df.head())
        #except:
        print('update df failed')

        
        # we join our previous out-of-sample predictions to check how well they did against the real data
        df_test = pd.merge(oosp, df, left_on='Date', right_on=date_col) 

        #visualise predictions 
        graph_vars(df_test, [indep_col, 'prediction'], pause=None).show()
        
        #compare prediction against the mean
        df_test['mean'] =  df[indep_col].mean()
        print(abs((df_test[indep_col]-df_test['mean']).mean()) - abs((df_test[indep_col]-df_test['prediction']).mean()))




