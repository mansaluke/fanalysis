#import blpapi
#options = blpapi.SessionOptions()
#options.setServerHost('localhost')
#options.setServerPort(8194)
#session = blpapi.Session(options)
#session.start()

try:
    from findatapy.market import MarketDataGenerator, Market, MarketDataRequest
except ImportError:
    from fanalysis.findatapy.market import MarketDataGenerator, Market, MarketDataRequest
import pandas as pd

def generate_market_data_for_tests(start_date, finish_date):

    # generate daily S&P500 data from Quandl
    #md_request = MarketDataRequest(start_date='01 Jan 2001', finish_date='01 Dec 2008',
    #                               tickers=['S&P500'], vendor_tickers=['YAHOO/INDEX_GSPC'], fields=['close'],
    #                               data_source='quandl')
#
#
#
    #market = Market(market_data_generator=MarketDataGenerator())
#
    #df = market.fetch_market(md_request)
    #df.to_csv("data\\S&P500.csv")

    # generate tick data from DukasCopy for EURUSD

    md_request = MarketDataRequest(start_date=start_date, finish_date=finish_date, cut='NYC', category='fx',
                                   fields=['bid'], freq='tick', data_source='dukascopy',
                                   tickers=['EURUSD'])


    market = Market(market_data_generator=MarketDataGenerator())
    try:
        df = market.fetch_market(md_request)
        return df
    except:
        return None


if __name__ == "__main__":

    #df = generate_market_data_for_tests(start_date='01 Jan 2019', finish_date='29 Aug 2019')
#
    import sys, os
    parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)+ '../..'))
    if parentdir not in sys.path:
       sys.path.insert(0, parentdir)

    from dfconvert import df_store
    import structure as s
    #df = pd.read_hdf('C:/Users/luke/Documents/Python Scripts/fanalysis/data/EURUSD_tick_historicals_2019.h5', 'df')
    #try:
    #    df_store('EURUSD_tick_historicals_2019.h5').store_df(df)
    #    df_store('EURUSD_tick_historicals_2019.feather').store_df(df)
    #except:
    #    pass
        #
    df = df_store('EURUSD_tick_historicals_2019.h5').load_df()
    print(df.head())
    df = df.reset_index()
    df = s.date_split(df)
    #try:
    #    df.memory_use()
    #except:
    #    pass
    try:
        df_store('EURUSD_tick_historicals.h5').store_df(df)
        df_store('EURUSD_tick_historicals.feather').store_df(df)
        print(2)
    except:
        df_store('EURUSD_tick_historicals.feather').store_df(df)
        print(3)
    #df_store('EURUSD_tick_historicals_2019.feather').store_df(df)
    #print(1)
    #df_store('EURUSD_tick_historicals.h5').store_df(df)

    df = df_store('EURUSD_tick_historicals_2019.h5').load_df()
    print(df.head())
    print(1)


