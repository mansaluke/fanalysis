import pandas as pd
import random as rd
import json
from datetime import datetime
from calendar import monthrange

def add_rand(df):
    rand = []
    for r in range(len(df)):
        rand.append(rd.random())
    rand = pd.Series(rand, name = 'randseries')
    df = pd.concat([df, rand], axis = 1)
    return df


#funciton to extract date elements (not used for now)
def datesplit(df):
    #df = df.copy()
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['week'] = pd.DatetimeIndex(df['date']).week
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['aggdaybyyear'] = df[df['month']>1].apply(lambda row: monthrange(row['year'], row['month']), axis=1)
    df[['a', 'aggdaybyyear']] = df['aggdaybyyear'].apply(pd.Series)
    df.drop(columns=['a'], inplace=True)
    df.loc[df['month'] ==1, 'aggdaybyyear'] = 0
    df['aggdaybyyear'] = df['aggdaybyyear'] + df['day']
    df['totaldays']=df['aggdaybyyear'].cumsum()
    return df


def lag_var(df, var, lags):
    df[var+'_lag'+str(lags)]=df[var].shift(lags)
    return df

#if __name__ == '__main__':
#    import main
#    #userinput()
#    df=jload('x.json')
#    df = add_rand(df)
#    df = datesplit(df)
#    df = lag_var(df, 'rnd', -1)
#    print(df.head())

if __name__ == '__main__':
    df.drop
    print(df)
    import extract
    df = add_rand(df)
    df = datesplit(df)
    #df = lag_var(df, 'd1', -1)
    print(df.head())

