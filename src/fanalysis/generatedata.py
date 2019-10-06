import numpy as np
import pandas as pd
from datetime import datetime
import random as rd
from pandas import DataFrame
from math import sqrt
from scipy.stats import norm
from pandas import DataFrame
from functools import wraps


class create_data():
    '''create data
    e.g.
    s = pd.to_datetime('01-01-2019')
    create_data('S', date = [s, datetime.now()]).gendateseries()
    create_data('S', date = datetime.now(), direction='Backwards').create_brownian_motion()


    pandas freq options:
    Alias,    Description
    B,    business day frequency
    C,    custom business day frequency
    D,    calendar day frequency
    W,    weekly frequency
    M,    month end frequency
    SM,    semi-month end frequency (15th and end of month)
    BM,    business month end frequency
    CBM,    custom business month end frequency
    MS,    month start frequency
    SMS,    semi-month start frequency (1st and 15th)
    BMS,    business month start frequency
    CBMS,    custom business month start frequency
    Q,    quarter end frequency
    BQ,    business quarter end frequency
    QS,    quarter start frequency
    BQS,    business quarter start frequency
    A, Y,    year end frequency
    BA, BY,    business year end frequency
    AS, YS,    year start frequency
    BAS, BYS,    business year start frequency
    BH,    business hour frequency
    H,    hourly frequency
    T, min,    minutely frequency
    S,    secondly frequency
    L, ms,    milliseconds
    U, us,    microseconds
    N, nanoseconds


    '''

    def __init__(self, frequency, date=datetime.now(), num_periods: 'int' = 100, direction=None):

        self.freq = frequency
        self.date = date
        self.num_periods = num_periods
        self.direction = direction

        if isinstance(date, list):
            self.start = date[0]
            self.end = date[1]
            if self.end < self.start:
                self.end = date[0]
                self.start = date[1]

        self.dates = self.gendateseries()

    def gendateseries(self):

        try:
            dates = pd.date_range(
                start=self.start, end=self.end, freq=self.freq)
        except:
            if self.direction == 'Backwards' or self.direction == 1:
                dates = pd.date_range(
                    end=self.date, periods=self.num_periods, freq=self.freq)
            elif self.direction == 'Forwards' or self.direction == -1:
                dates = pd.date_range(
                    start=self.date, periods=self.num_periods, freq=self.freq)
        # else:
        #    raise AttributeError
        return DataFrame(dates, columns=['Date'])

    def generate_rand_df(self, low=0, high=1) -> DataFrame:
        """
        generates random uniform dataframe
        """
        dates = self.dates
        length = len(self.dates)
        df = dates.assign(rnd=np.random.uniform(low, high, length))
        print("data created")
        return df

    def create_brownian_motion(self, start_price=100, T=1, N=100, mu=0.1, sigma=0.1, S0=20) -> DataFrame:
        """
        dS=μS dt+σS dWt
        t = time
        n = no periods
        mu = drift
        sigma = stand dev
        w = standard brownian motion 
        S = geom standard brownian motion 
        s0 = start price
        """
        N = self.dates.size
        T = ((self.dates.max()-self.dates.min())/np.timedelta64(1, 'D')) / 365
        dt = float(T)/N
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size=N)
        W = np.cumsum(W)*np.sqrt(dt)  # standard brownian motion ###
        W = W.reshape(N, 1)
        X = (mu-0.5*sigma**2)*t + sigma*W  # ITO'S LEMMA
        S = S0*np.exp(X)  # geometric brownian motion ###
        return self.dates.assign(bm=S)


class create_data_sef(create_data):
    """
    we can do the same as in the create_data class but with start, end and freq as inputs

    bm = create_data_sef(pd.to_datetime(min(df['date'])), pd.to_datetime(max(df['date'])), 'd').create_brownian_motion()
    print(bm)
    """

    def __init__(self, start, end, freq):
        self.start, self.end = start, end
        self.freq = freq
        self.dates = self.gendateseries()


def append_df(att1, att2) -> DataFrame:
    """
    joins the dataframe from the init (original_df) with the output of 
    the function
    """
    def do_append_after(fn):
        @wraps(fn)
        def append_after(self, *args, **kwargs):
                #print('entering append_after (append_df decorator)')
                # assign attributes from original class to variables in decorator
            original_df = getattr(self, att1)
            datename = getattr(self, att2)
            returned_df = fn(self, *args, **kwargs)
            cols_o, cols_r = original_df.columns.values, returned_df.columns.values
            cols_r = cols_r[cols_r != datename]

            def change_colname(col, cols_o, cols_r):
                # add 1 to the name of the column if already exists
                # preferred to pandas _X _y append
                i = 1
                new_col = col
                while new_col in cols_o or new_col in cols_r:
                    new_col = col + str(i)
                    i += 1
                col = new_col
                return col

            for col in cols_r:
                returned_df = returned_df.rename(
                    {col: change_colname(col, cols_o, cols_r)}, axis=1)

            appended_df = original_df.merge(
                returned_df, on=datename, how='left')

            return appended_df
        return append_after
    return do_append_after


def callable(o):
    return hasattr(o, "__call__")


def append_df_toclassfns(att1, att2):
    """
    decorator: wraps all functions in class with the append_df decorator
    """
    def do_alterfns(cls):
        for key, val in cls.__dict__.items():
            if key.startswith("__") and key.endswith("__") \
                    or not callable(val):
                continue
            setattr(cls, key, (append_df(att1, att2))(val))
            #print("wrapped", key)
        return cls
    return do_alterfns


@append_df_toclassfns('df', 'datename')
class append_data(create_data):
    """
    modified version of create_data class - uses df as input and
    appends df to output of each function
    e.g.
    d = append_data(df).create_brownian_motion()
    """

    def __init__(self, df):
        self.df = df
        self.datename = self.df.select_dtypes(
            include=[np.datetime64]).columns[0]
        self.dates = DataFrame(self.df[self.datename])

    # @append_df('df', 'datename')
    def generate_rand_df(self, *args, **kwargs) -> DataFrame:
        """
        appends random uniform dist to dataframe
        """
        # return create_data.generate_rand_df(self)
        return super(append_data, self).generate_rand_df(*args, **kwargs)

    def create_brownian_motion(self, *args, **kwargs) -> DataFrame:
        """
        appends brownian motion dict to dataframe
        """
        return super(append_data, self).create_brownian_motion(*args, **kwargs)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    #print(pd.date_range(start = s, end=datetime.now(), freq='S'))
    #print(create_data('S', date = [s, datetime.now()]).gendateseries())
    #df = create_data('d', date = datetime.now(), direction='Backwards').generate_rand_df(0, 1)
    df = create_data('d', date=datetime.now(),
                     direction='Backwards').create_brownian_motion()

    for i in range(10):
        df = append_data(df).create_brownian_motion()

    print(df.head())

    for col in df.columns.values[df.columns.values != 'Date']:
        plt.plot(df['Date'], df[col], '.')
    plt.show()
