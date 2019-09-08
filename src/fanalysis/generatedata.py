import numpy as np
import pandas as pd 
from datetime import datetime
import random as rd
from pandas import DataFrame




class create_data:
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
    def __init__(self, frequency, date = datetime.now(), num_periods=100, direction=None):

        self.freq = frequency
        self.date = date
        self.num_periods = num_periods
        self.direction = direction

        if isinstance(date, list):
            self.start=date[0]
            self.end=date[1]
        
        self.dates = self.gendateseries()
        self.length = len(self.dates)


    def gendateseries(self):
        
        try:
            dates = pd.date_range(start = self.start, end=self.end, freq=self.freq)
        except:
            if self.direction == 'Backwards' or self.direction == 1:
                dates = pd.date_range(end=self.date, periods=self.num_periods, freq=self.freq)
            elif self.direction == 'Forwards' or self.direction == -1:
                dates = pd.date_range(start=self.date, periods=self.num_periods, freq=self.freq)         
        #else:
        #    raise AttributeError
        return DataFrame(dates, columns = ['Date'])
        


    def genuniformseries(self, low =0, high = 1 ):

        dates = self.gendateseries()
        df = dates.assign(rnd=np.random.uniform(low,high,self.length))
        print("data created")
        return df

    def create_brownian_motion(self, start_price = 100, T = 1, N = 100, mu = 0.1, sigma = 0.1, S0 = 20):
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
        T = ((self.dates.max()-self.dates.min())/np.timedelta64(1,'D'))/ 365
        dt = float(T)/N
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size = N) 
        W = np.cumsum(W)*np.sqrt(dt) ### standard brownian motion ###
        W = W.reshape(100, 1)
        X = (mu-0.5*sigma**2)*t + sigma*W ### ITO'S LEMMA
        S = S0*np.exp(X) ### geometric brownian motion ###
        return self.dates.assign(bm = S)
    



if __name__ == '__main__':

    s = pd.to_datetime('01-01-2019')
    #print(pd.date_range(start = s, end=datetime.now(), freq='S'))
    #print(create_data('S', date = [s, datetime.now()]).gendateseries())
    #print(create_data('S', date = datetime.now(), direction='Backwards').create_brownian_motion())
    
    #import plotting as p
    #print(df.head())
    #p.plots(df)

