import pandas as pd
import random as rd
import json
from datetime import datetime
from calendar import monthrange
from numba import jit



@jit
def add_rand(df):
    rand = []
    for r in range(len(df)):
        rand.append(rd.random())
    rand = pd.Series(rand, name = 'randseries')
    df = pd.concat([df, rand], axis = 1)
    return df



def date_split(df):
    """
    Extracts date elements from pandas DataFrame:
    --year, month, week, day, hour, daysinmonth, aggdays
    """
    try:
        df['year'] = pd.DatetimeIndex(df['date']).year
        df['month'] = pd.DatetimeIndex(df['date']).month
        df['day'] = pd.DatetimeIndex(df['date']).day
    except:
        raise OSError("could not create dates - check date column exists and correct format")
    try:
        df['week'] = pd.DatetimeIndex(df['date']).week
    except:
        pass
    try:
        df['hour'] = pd.DatetimeIndex(df['date']).hour
    except:
        pass
    #df['daysinmonth'] = df.apply(lambda row: monthrange(row['year'], row['month']), axis=1).str[1]
    df['not_dupym'] = 1 - df[['month', 'year']].duplicated()
    df = df.merge(
df[df['not_dupym']==1].groupby(['year', 'month'], as_index=False)['year', 'month'].sum().apply(lambda row: monthrange(row['year'].astype('int'), row['month'].astype('int')), axis=1).str[1].reset_index().rename(columns={0:"daysinmonth"})
, on = ['year', 'month'], how = 'left')

    #edit 21/05/2019
    days_first_month = df[df['not_dupym']==1].groupby(['year', 'month'])['daysinmonth'].sum().cumsum().idxmin()
    days_first_month = monthrange(days_first_month[0], days_first_month[1])[1]
    df = df.merge(
    df[df['not_dupym']==1].groupby(['year', 'month'])
    ['daysinmonth'].sum().cumsum().transform(lambda x: x-days_first_month).reset_index()
, on = ['year', 'month'], how = 'left')
    #end 

    #df = df.merge(
    #df[df['not_dupym']==1].groupby(['year', 'month'])
    #['daysinmonth'].sum().cumsum().reset_index().groupby(['year','daysinmonth'])
    #['month'].sum().transform(lambda x: x+1).reset_index()
#, on = ['year', 'month'], how = 'left')
    df['aggdays']=df['daysinmonth_y'].fillna(0).astype('int') + df['day']
    df.drop(columns=['daysinmonth_x','daysinmonth_y', 'not_dupym'], inplace=True)
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
        
    df = add_rand(df)
    df = date_split(df)
    #df = lag_var(df, 'd1', -1)
    print(df.columns)
    print(df[['date', 'day', 'month', 'year', 'aggdays']])
    from plotting import plots
    plots(df, None, 1)


