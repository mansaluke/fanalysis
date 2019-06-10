import pandas as pd
import random as rd
import json
from datetime import datetime
from calendar import monthrange
from numba import jit
import numpy as np
import matplotlib.pyplot as plt



class anomoly_detect():
    """
    e.g.
    anomoly_detect(df, 'd3').anomolies
    d = anomoly_detect(df, 'd3').rm_anomolies(toNaN=False)
    """
    def __init__(self, df, variable, xlen = 10, graph = True):        
        self.df = df.copy()
        self.variable = variable
        self.xlen = xlen
        self.graph = graph
        
        self.anomolies = self.differences_collect()
        
        if self.graph == True:
            self.graph_anomolies(self.anomolies, 'diff_t', self.variable, self.xlen)

            
    def differences_collect(self):
        largest = self.df[[self.variable]].copy(deep=False)
        largest['diff_t'] = np.sqrt(((largest[self.variable].shift(1) - largest[self.variable])/largest[self.variable])**2)*100
        largest = largest.nlargest(self.xlen, 'diff_t')
        return largest

    def graph_anomolies(self, largest, diff_t, variable, xlen):
        plt.style.use('fivethirtyeight')
        x_values = list(range(xlen))
        plt.bar(x_values, largest[diff_t], orientation='vertical')
        plt.ylabel('% diff')
        plt.title('Anomolies')
        plt.show()
        
    def rm_anomolies(self, toNaN = True):
        anom_list = list(self.anomolies.reset_index()['index'])
        for i in range(len(anom_list)-1):
            cur = anom_list[i+1]
            prev = anom_list[i]
            if cur == prev + 1:
                if toNaN == False:
                    self.df.drop(self.df.index[prev])
                elif toNaN != False:
                    self.df.loc[self.df.index == prev, self.variable] = np.NaN
        return self.df




@jit
def add_rand(df):
    rand = []
    for r in range(len(df)):
        rand.append(rd.random())
    rand = pd.Series(rand, name = 'randseries')
    df = pd.concat([df, rand], axis = 1)
    return df



def date_split(df, datename = 'date', time=False, errors="raise"):
    """
    Extracts date elements from pandas DataFrame:
    --year, month, week, day, hour, daysinmonth, aggdays
    """
    datecol = df[datename]

    datecol_dtype = datecol.dtype
    if isinstance(datecol_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        datecol_dtype = np.datetime64
    if not np.issubdtype(datecol_dtype, np.datetime64):
        df[datename] = datecol = pd.to_datetime(datecol, infer_datetime_format=True, errors=errors)


    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    
    for n in attr: 
        df[n] = getattr(datecol.dt, n.lower())
    
    if time==True: 
        attr = ['Hour', 'Minute', 'Second']
        try:
            for n in attr: 
                df[n] = getattr(datecol.dt, n.lower())
            raise ValueError
        except ValueError:
            print("No time element to extract.")
            raise
            
    df['not_dupym'] = 1 - df[['Month', 'Year']].duplicated()
    
    df_daysinmonth = df[df['not_dupym']==1].groupby(['Year', 'Month'], as_index=False)['Year', 'Month'].sum().apply(lambda row: monthrange(row['Year'].astype('int'), row['Month'].astype('int')), axis=1).str[1].reset_index().rename(columns={0:'daysinmonth'})
    days_first_month = df_daysinmonth.groupby(['Year', 'Month'])['daysinmonth'].sum().cumsum().idxmin()
    days_first_month = monthrange(days_first_month[0], days_first_month[1])[1]
    
    df_daysinmonth = df_daysinmonth.groupby(['Year', 'Month'])['daysinmonth'].sum().cumsum().transform(lambda x: x-days_first_month).reset_index()
    df = df.merge(df_daysinmonth, on = ['Year', 'Month'], how = 'left')
    df['aggdays']=df['daysinmonth'].fillna(0).astype('int') + df['Day'].astype('int')
    df.drop(columns=['not_dupym'], inplace=False)
    return df
    


def lag_var(df, var, lags):
    df[var+'_lag'+str(lags)]=df[var].shift(lags)
    return df



if __name__ == '__main__':
    x=0

    if x == 0:
        from dfconvert import df_store
        df=df_store('quanddata').load_df().reset_index()
    elif x ==1:
        import extract as e
        df = e.use_csvs()
    print(df.head())
    #df = add_rand(df)
    df = date_split(df, 'Date')
    df = lag_var(df, 'Open', -1)
    anomoly_detect(df, 'Open').anomolies



