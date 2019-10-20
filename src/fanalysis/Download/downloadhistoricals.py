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
from datetime import datetime, timedelta


def generate_market_data_for_tests(start_date, finish_date):


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
    days_to_download = 10
    end_date = datetime.now()
    start_date = end_date - timedelta(days_to_download)
    print(f"""start date: {start_date} \
            end date: {end_date}""")


    import sys, os
    parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)+ '../..'))
    if parentdir not in sys.path:
       sys.path.insert(0, parentdir)

    from dfconvert import df_store
    import structure as s

    file_name = 'EURUSD_tick_historicals_' + str(end_date).replace(' ', '_') + '.h5' 
    print(file_name)



    df = generate_market_data_for_tests(start_date=start_date, finish_date=end_date)


    #try:
    #    df_store('EURUSD_tick_historicals.h5').store_df(df)
    #    df_store('EURUSD_tick_historicals.feather').store_df(df)
    #    print(2)
    #except:
    #    df_store('EURUSD_tick_historicals.feather').store_df(df)
    #    print(3)

    #df = df_store(file_name).load_df()
    #print(df.head())
    #df = df.reset_index()
    #df = s.date_split(df)


