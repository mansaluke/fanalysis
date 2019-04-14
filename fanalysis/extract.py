########download historical data first (get_fx_m1)

from datetime import datetime
import os
import pandas  as pd
import matplotlib.pyplot as plt
from calendar import monthrange
import sys
import time

def create_path(path):
    if not os.path.exists(path):
        print('data directory not found. Please create the data folder amd try again')
        #os._exit(1)
    return path



def str_listconcat (input, str):
    l = len(input)
    list = []
    for i in range(l):
        list.append(str)
        list[i] = list[i] + input[i]
    input = list
    return input
#join(x.tolist())



def use_csvs():
    path = create_path('data')
    #collect files from data folder
    files = os.listdir(path) #use os.getcwd() if files in same path. otherwise set path
    files = str_listconcat(files, "data/")
    
    #read and combine data
    header= ['date', 'd1', 'd2', 'd3', 'd4', 'v']
    dtypes = {'d1': 'float32',   
              'd2': 'float32', 
              'd3': 'float32', 
              'd4': 'float32', 
              'v': 'float32'}
    
    files_csv = [pd.read_csv(f, sep = ";", header = None, names=header, parse_dates = ['date'], 
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
    return df



def graph_vars(df, header):
    plt.rcParams['figure.figsize'] = (15, 5)
    #plt.figure(); df.plot();plt.legend(loc='best')
    for h in header:
        plt.plot(df['date'], df[h])
        #plt.plot(df['date'], df[colnames(h)])        
        plt.title([h])
        #plt.ylabel('Price (£)')
        plt.pause(0.01)
        plt.show(block=False)
        time.sleep(0.5)
        plt.close
        #plt.gcf()


if __name__ == '__main__':
    df = use_csvs()
    import structure as s
    #df = s.add_rand(df)
    #df = s.datesplit(df)
    #df = s.lag_var(df, 'd1', -1)

    print(df.columns)
    header = ['d1','d2', 'd3', 'd4']
    #header[1:-1]
    graph_vars(df, header)



