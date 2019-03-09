########download historical data before using this file (get_fx_m1)

from datetime import datetime
import os
import pandas  as pd
import matplotlib.pyplot as plt
from calendar import monthrange
import sys
import time

if not os.path.exists('fanalysis/data'):
    print('data directory not found. Please create the fanalysis/data folder amd try again')
    os._exit(1)
#collect files from data folder
files = os.listdir('fanalysis/data') #use os.getcwd() if files in same path. otherwise set path
def strlistconcat (input, str):
    l = len(input)
    list = []
    for i in range(l):
        list.append(str)
        list[i] = list[i] + input[i]
    input = list
    return input

files = strlistconcat(files, "fanalysis/data/")

#read and combine data
headers = ['date', 'd1', 'd2', 'd3', 'd4', 'v']
dtypes = {'d1': 'float32',   
          'd2': 'float32', 
          'd3': 'float32', 
          'd4': 'float32', 
          'v': 'float32'}

files_csv = [pd.read_csv(f, sep = ";", header = None, names=headers, parse_dates = ['date'], 
    dtype = dtypes, infer_datetime_format=True) 
    for f in files if f[-3:] == 'csv']
        
df = pd.concat(files_csv, ignore_index=True)

colnames = {'d1':'Bar OPEN Bid Quote', 
            'd2':'Bar HIGH Bid Quote', 
            'd3':'Bar LOW Bid Quote', 
            'd4' : 'Bar CLOSE Bid Quote', 
            'v': 'Volume'}

#set date
#from datetime import datetime
print(df[:10])
#df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y%m%d %H%M%S'))
df.set_index('date')

#graph
plt.rcParams['figure.figsize'] = (15, 5)
#df['d2'].plot()
#df = df.cumsum()
#plt.figure(); df.plot();plt.legend(loc='best')
for h in headers[1:-1]:
    plt.plot(df['date'], df[h])
    plt.title('USD ($)/Pound Sterling (£)' + colnames[h])
    plt.ylabel('Price (£)')
    plt.pause(0.01)
    plt.show(block=False)
    time.sleep(0.5)
    plt.close
    #plt.gcf()

