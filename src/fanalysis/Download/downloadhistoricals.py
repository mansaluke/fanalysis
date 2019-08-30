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
#from dfconvert import df_store

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
    df = market.fetch_market(md_request)
    print(df.head())
    #try:
    #    df_store('EURUSD_tick_historicals_2019.h5').store_df(df)
    #except:
    #    df_store('EURUSD_tick_historicals.feather').store_df(df)
    ##df.to_hdf5("fanalysis\\data\\EURUSD_tick.h5")
    #print(4)
    return df


if __name__ == "__main__":
    pass
    #generate_market_data_for_tests(start_date='08 Jan 2019', finish_date='07 Aug 2019')

