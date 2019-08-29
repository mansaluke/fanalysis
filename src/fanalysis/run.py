#TODO create module which downloads latest data and runs all pre-optimised models

try:
    from Models.optimize import optimize_rf
    from Models.Random_Forest import do_rf
    import Download.downloadhistoricals as dh
except ImportError:
    from fanalysis.Models.optimize import optimize_rf
    from fanalysis.Models.Random_Forest import do_rf
    import Download.downloadhistoricals as dh

import dfconvert as dfc
from datetime import datetime, timedelta

def download(start_date, finish_date):
    return dh.generate_market_data_for_tests(start_date, finish_date)

    
def test_split_df(df, prop = 0.25):
    df.sort_values(by=['Date'], inplace=True)
    return df[:round(len(df) *(1-prop))], df[round(len(df) * (1-prop)):]

def create_pred(df):
    max_estimators=100
    df, test = test_split_df(df)
    orf =  optimize_rf(df, n_estimators=max_estimators, indep_col = 'EURUSD.bid' )        
    opt_n_estimators = orf.opt_n_estimators
    print('opt: {}'.format(opt_n_estimators))
    rf = do_rf(df, n_estimators=opt_n_estimators, indep_col = 'EURUSD.bid')
    rf.predict_out(True)
    rf.return_error_details()
    rf.print_score()
    rf.importances()
    oosp = rf.out_of_sample_pred(test)


if __name__ == "__main__":
    #df = dfc.df_store('EURUSD_tick_sample.h5').load_df()
    start_date = datetime.today() - timedelta(days=10)
    finish_date = datetime.now()
    print(start_date, finish_date)
    df = download(start_date, finish_date)
    import structure as s

    df = df.sample(n=500000)
    df = df.reset_index()
    print(df.head())
    df = s.date_split(df)
    #df = drop_col(df, ['aggdays', 'daysinmonth'])
    print(df.head())
    create_pred(df)

