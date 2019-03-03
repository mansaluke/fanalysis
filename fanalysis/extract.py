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