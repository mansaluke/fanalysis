import pandas as pd
import random as rd
import json
from datetime import datetime
from calendar import monthrange
from numba import jit, generated_jit

@jit
def add_rand(df):
    rand = []
    for r in range(len(df)):
        rand.append(rd.random())
    rand = pd.Series(rand, name = 'randseries')
    df = pd.concat([df, rand], axis = 1)
    return df



def date_split(df):
    #df = df.copy()
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['week'] = pd.DatetimeIndex(df['date']).week
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['hour'] = pd.DatetimeIndex(df['date']).hour
    #df['daysinmonth'] = df.apply(lambda row: monthrange(row['year'], row['month']), axis=1).str[1]
    df['not_dupym'] = 1 - df[['month', 'year']].duplicated()
    df = df.merge(
    df[df['not_dupym']==1].groupby(['year', 'month'], as_index=False)['year', 'month'].sum().apply(lambda row: monthrange(row['year'].astype('int'), row['month'].astype('int')), axis=1).str[1].reset_index().rename(columns={0:"daysinmonth"})
, on = ['year', 'month'], how = 'left')
    df = df.merge(
    df[df['not_dupym']==1].groupby(['year', 'month'])
    ['daysinmonth'].sum().cumsum().reset_index().groupby(['year','daysinmonth'])
    ['month'].sum().transform(lambda x: x+1).reset_index()
, on = ['year', 'month'], how = 'left')
    df['aggdays']=df['daysinmonth_y'].fillna(0).astype('int') + df['day']
    df.drop(columns=['daysinmonth_x','daysinmonth_y', 'not_dupym'], inplace=True)
    return df

@jit
def lag_var(df, var, lags):
    df[var+'_lag'+str(lags)]=df[var].shift(lags)
    return df


x=0
if __name__ == '__main__':
    if x == 0:
        import main
        df=main.json_load('x.json')
    elif x ==1:
        import extract
        df = use_csvs()
        
    df = add_rand(df)
    df = date_split(df)
    #df = lag_var(df, 'd1', -1)
    print(df.columns)
    print(df[['date', 'day', 'month', 'year', 'aggdays']])


