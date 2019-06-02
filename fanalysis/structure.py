import pandas as pd
import random as rd
import json
from datetime import datetime
from calendar import monthrange
from numba import jit
import numpy as np


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

    #split into seperate dataset - memory error
    df_daysinmonth = df[df['not_dupym']==1].groupby(['Year', 'Month'], as_index=False)['Year', 'Month'].sum().apply(lambda row: monthrange(row['Year'].astype('int'), row['Month'].astype('int')), axis=1).str[1].reset_index().rename(columns={0:'daysinmonth'})
    days_first_month = df_daysinmonth.groupby(['Year', 'Month'])['daysinmonth'].sum().cumsum().idxmin()
    days_first_month = monthrange(days_first_month[0], days_first_month[1])[1]

    df_daysinmonth = df_daysinmonth.groupby(['Year', 'Month'])['daysinmonth'].sum().cumsum().transform(lambda x: x-days_first_month).reset_index()
    df = df.merge(df_daysinmonth, on = ['Year', 'Month'], how = 'left')
    df['aggdays']=df['daysinmonth'].fillna(0).astype('int') + df['Day'].astype('int')
    try:
        df.drop(columns=['not_dupym'], inplace=False)
    except:
        pass
    return df
    


@jit
def lag_var(df, var, lags):
    df[var+'_lag'+str(lags)]=df[var].shift(lags)
    return df



if __name__ == '__main__':
    x=1

    if x == 0:
        import main
        df=main.json_load('fanalysis\\data\\x.json')
    elif x ==1:
        import extract as e
        df = e.use_csvs()
    print(df.memory_usage())
    print(df.memory_usage().sum()) 
    df.info(memory_usage='deep')   
    #df = add_rand(df)
    df = date_split(df)
    #df = lag_var(df, 'd1', -1)
    print(df.columns)
    #print(df[['date', 'Day', 'Month', 'Year', 'aggdays']])
    #from plotting import plots
    #plots(df, None, 1)


