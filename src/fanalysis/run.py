
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
        
        start_date, finish_date = self.hmax, self.nmax
        #make sure historicals are up-to-date
        try:
            df_latest = download(start_date, finish_date)
            print('latest data')
            print(df_latest.head())
            df_latest = df_latest.reset_index()
            df_latest = s.date_split(df_latest)
            rf.fix_missing(df_latest, df_latest['EURUSD.bid'], 'EURUSD.bid', {})
            print(df_latest.head())
            self.df = pd.concat([self.df, df_latest], keys = list(df.columns), ignore_index=True, sort=False)
            print('concat')
            print(self.df.head())
            del df_latest
            #return new
        except:
            pass
            #return self.df

    def opt_estimator_fn(self):
        """optimizes rf model"""
        max_estimators=100
        #df, test = test_split_df(df)
        orf =  optimize_rf(self.df, n_estimators=self.max_estimators, indep_col = 'EURUSD.bid' )        
        opt_n_estimators = orf.opt_n_estimators
        print('opt: {}'.format(opt_n_estimators))
        return opt_n_estimators

    def create_pred(self):    
        """creates predictions"""
        
        rf = do_rf(self.df, n_estimators=self.opt_n_estimators, indep_col = 'EURUSD.bid')
        rf.predict_out(True)
        rf.return_error_details()
        rf.print_score()
        rf.importances()
        osd = data(100, "S", "Forward").gendateseries()
        osd = s.date_split(osd)
        return rf.out_of_sample_pred(osd)
        


if __name__ == "__main__":
    a=1
    df = dfc.df_store('EURUSD_tick_historicals.h5').load_df()
    print(len(df))
    print(df.memory_usage(deep=True))

    print('size: ', df.memory_usage().sum()/1000000, 'mb')

    if len(df) > 100000:
        df = df.sample(n=100000)
    print(len(df))
    print(df.head())
    #rf.fix_missing(df, df['EURUSD.bid'], 'EURUSD.bid', {})


    while 1==1:

        #make sure historicals are up-to-date

        
        print(len(df))
        #if a == 1:
        #    dfc.df_store('EURUSD_tick_historicals.h5').store_df(df)
        #    a = 0
        rp = run_pred(df)
        print(5)

        #run model on historicals
        oosp = run_pred(df).create_pred()
        df_test = pd.merge(oosp, df, on='Date')   
        plots(df_test, ['EURUSD.bid', 'oos_pred'])
        df_test['mean'] =  df['EURUSD.bid'].mean()
        print(abs((df_test['EURUSD.bid']-df_test['mean']).mean()) - abs((df_test['EURUSD.bid']-df_test['oos_pred']).mean()))




    #Index(['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
    #   'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start',
    #   'Is_year_end', 'Is_year_start', 'not_dupym', 'daysinmonth', 'aggdays',
    #   'mean'],
    #  dtype='object')






