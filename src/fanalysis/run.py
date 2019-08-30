#TODO create module which downloads latest data and runs all pre-optimised models

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

def download(start_date, finish_date):
    return dh.generate_market_data_for_tests(start_date, finish_date)

    
def test_split_df(df, prop = 0.25):
    df.sort_values(by=['Date'], inplace=True)
    return df[:round(len(df) *(1-prop))], df[round(len(df) * (1-prop)):]

class run_pred():

    def __init__(self, df):
        self.df = df
        self.max_estimators = 100
        self.opt_n_estimators = self.opt_estimator_fn()
        self.hmax, self.nmax = self.update_times()

    def update_times(self):
        df = self.df
        start_date = df['Date'].max()
        finish_date = datetime.now()
        print(start_date, finish_date)
        print('updating: ' , finish_date - start_date)
        return start_date, finish_date

    def update_df(self):
        df = self.df
        start_date, finish_date = self.hmax, self.nmax
        #make sure historicals are up-to-date
        df_latest = download(start_date, finish_date)
        del df_latest
        return pd.concat([df, df_latest], keys = list(df.columns), axis= 0, sort=False)

    def opt_estimator_fn(self):
        """optimizes rf model"""
        df = self.df
        max_estimators=100
        #df, test = test_split_df(df)
        orf =  optimize_rf(df, n_estimators=self.max_estimators, indep_col = 'EURUSD.bid' )        
        opt_n_estimators = orf.opt_n_estimators
        print('opt: {}'.format(opt_n_estimators))
        return opt_n_estimators

    def create_pred(self):    
        """creates predictions"""
        df = self.df
        rf = do_rf(df, n_estimators=opt_n_estimators, indep_col = 'EURUSD.bid')
        rf.predict_out(True)
        rf.return_error_details()
        rf.print_score()
        rf.importances()
        osd = data(100, "S", "Forward").gendateseries()
        osd = s.date_split(osd)
        return rf.out_of_sample_pred(osd)
        


if __name__ == "__main__":
    a=1
    while 1==1:
        df = dfc.df_store('EURUSD_tick_sample.h5').load_df()
        print(df.head())
        #make sure historicals are up-to-date
        df = run_pred(df).update_df()
        print(df.head())
        print(df.memory_usage())
        print(len(df))
        if a == 1:
            dfc.df_store('EURUSD_tick_sample.h5').store_df(df)
            a = 0

        df = run_pred(df).update_df()
        #run model on historicals
        oosp = run_pred(df).create_pred()
        df_test = pd.merge(oosp, df, on='Date')   
        plots(df_test, ['EURUSD.bid', 'oos_pred'])
        df_test['mean'] =  df['EURUSD.bid'].mean()
        print(abs((df_test['EURUSD.bid']-df_test['mean']).mean()) - abs((df_test['EURUSD.bid']-df_test['oos_pred']).mean()))

