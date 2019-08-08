import numpy as np
import pandas as pd 
from datetime import datetime
import random as rd
from pandas import DataFrame




class data:
    '''create data
    e.g. df = data(100, "S").genseries()


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
    def __init__(self, starting_period, frequency):

        self.p, self.f = starting_period, frequency

        self.dates = DataFrame(self.gendateseries())
        self.length = len(self.dates)

    def gendateseries(self):
        try:
            dates = pd.date_range(end=datetime.now(), periods=self.p, freq=self.f)
        except:
            raise ValueError("Cannot generate that many periods.")
        return dates

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
        X = (mu-0.5*sigma**2)*t + sigma*W ### ITO'S LEMMA
        S = S0*np.exp(X) ### geometric brownian motion ###
        df = self.dates.assign(bm = S)
        return pd.DataFrame(S)

    



if __name__ == '__main__':
    import plotting as p
    df = data(100, "S").create_brownian_motion()
    print(df)
    p.plots(df)
    