
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
from generatedata import create_data
import dfconvert as dfc
import structure as s
from plotting import plots

from datetime import datetime, timedelta
import pandas as pd

import threading

def download(start_date, finish_date):
    return dh.generate_market_data_for_tests(start_date, finish_date)

    
def test_split_df(df, prop = 0.25):
    df.sort_values(by=['date'], inplace=True)
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

    def __init__(self, df, indep_col):
        self.df = df
        self.indep_col = indep_col
        self.max_estimators = 10
        self.opt_n_estimators = self.opt_estimator_fn()
        self.hmax, self.nmax = self.update_times()


    def update_times(self):
        df = self.df
        start_date = df['date'].max()
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
            rf.fix_missing(df_latest, df_latest[indep_col], indep_col, {})
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
        orf =  optimize_rf(self.df, n_estimators=self.max_estimators, indep_col = indep_col )        
        opt_n_estimators = orf.opt_n_estimators
        print('opt: {}'.format(opt_n_estimators))
        return opt_n_estimators

    def create_pred(self):    
        """creates predictions"""
        
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
        osd = self.df['date'][self.df['date']>=self.hmax]
        print(osd.head())
        #osd = create_data("S", "Forward").gendateseries()
        #osd = s.date_split(osd, time=False)
        return rf.out_of_sample_pred(osd)
        


if __name__ == "__main__":
    a=1
    indep_col='d1'
    date_col = 'date'
    df = dfc.df_store('data.h5').load_df()

    df = rf.drop_col(df, ['d2', 'd2', 'd3', 'd4', 'v'])

    print(df.head())
    print(len(df))
    print(df.memory_usage(deep=True))

    print('size: ', df.memory_usage().sum()/1000000, 'mb')

    print(len(df))
    if len(df) > 100000:
        df = df.sample(n=100000)
    
    print(df.head())
    #rf.fix_missing(df, df[indep_col], indep_col, {})

    #a = optimize_rf(df, indep_col, n_estimators=5)
    #print(a.opt_n_estimators)
    #a.predict_out()

    print('entering loop')

    while 1==1:

        #make sure historicals are up-to-date       
        print(len(df))
        #if a == 1:
        #    dfc.df_store('EURUSD_tick_historicals.h5').store_df(df)
        #    a = 0
        rp = run_pred(df, indep_col)
        print('here')

        #run model on historicals
        oosp = rp.create_pred()
        rp.update_df()
        print(oosp.head())
        df_test = pd.merge(oosp, df, left_on='Date', right_on=date_col)  
        plots(df_test, [indep_col, 'oos_pred'])
        df_test['mean'] =  df[indep_col].mean()
        print(abs((df_test[indep_col]-df_test['mean']).mean()) - abs((df_test[indep_col]-df_test['oos_pred']).mean()))




