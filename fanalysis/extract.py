########download historical data
#git clone https://github.com/philipperemy/FX-1-Minute-Data.git fx
#if __name__ == '__main__':
#    download_fx_m1_data_year()
#download all months needed. in this example i download all of 2018

import os
import pandas  as pd
import matplotlib.pyplot as plt
import random as rd
import datetime
import numpy as np
from calendar import monthrange
import statistics
import json
from datetime import datetime
print(datetime.now())

#collect files from data folder
files = os.listdir("data") #use os.getcwd if files in same path. otherwise set path
def strlistconcat (input, str):
    l = len(input)
    list = []
    for i in range(l):
        list.append(str)
        list[i] = list[i] + input[i]
    input = list
    return input

files = strlistconcat(files, "data/")

#read and combine data
headers = ['date', 'd1', 'd2', 'd3', 'd4', 'v']
print(datetime.now())
files_csv = [pd.read_csv(f, sep = ";", header = None, names=headers) 
    for f in files if f[-3:] == 'csv']
print(datetime.now())
df = pd.concat(files_csv, ignore_index=True)
print(datetime.now())
colnames = {'d1':'Bar OPEN Bid Quote', 'd2':'Bar HIGH Bid Quote', 'd3':'Bar LOW Bid Quote', 'd4' : 'd4', 'v': 'Volume'}

#set date
#from datetime import datetime

df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y%m%d %H%M%S'))
df.set_index('date')

#graph
plt.rcParams['figure.figsize'] = (15, 5)
#df['d2'].plot()
#df = df.cumsum()
#plt.figure(); df.plot();plt.legend(loc='best')
plt.plot(df['date'], df['d1'])
plt.title('USD $-Pound Sterling £')
plt.ylabel('Price (£)')
#plt.show()


#create data
#l = len(df)
rand = []
for r in enumerate(df):
    rand.append(rd.random())
rand = pd.Series(rand, name = 'rand')
df = pd.concat([df, rand], axis = 1, join = 'inner')


#funciton to extract date elements (not used for now)
def datesplit(df):
    df = df.copy()
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['week'] = pd.DatetimeIndex(df['date']).week
    df['year'] = pd.DatetimeIndex(df['date']).year
    return df
df = datesplit(df)


df['aggday'] = df[df['month']>1].apply(lambda row: monthrange(row['year'], row['month']), axis=1)

df[['a', 'aggday']] = df['aggday'].apply(pd.Series)

df.drop(columns=['a'], inplace=True)

df.loc[df['month'] ==1, 'aggday'] = 0
df['aggday'] = df['aggday'] + df['day']
print(df.head())
print(df.info())

print(datetime.now())
#out = df.to_json(orient='split')
#
#with open('temp.json', 'w') as f:
#    f.write(out)
fd.to_json('temp.json', orient='index')
print(datetime.now())

df['TS'] =  0.1 * df['aggday'] - df['rand'] *0.1 
print(df.head())
plt.plot(df['date'], df['TS'])
plt.title('TS')
plt.ylabel('Price (£)')
plt.show()

mean = df['d1'].mean()
print(mean)

variance = statistics.variance(df['d1'])
print(variance)

