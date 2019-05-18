"""
download historical data first (get_fx_m1)
"""

from datetime import datetime
import os
import pandas  as pd
from calendar import monthrange
import sys
from misc import Ipython


def mkdir_p(path):
    import errno
    try:
        path = path
        os.makedirs(path)
        return path
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return path
        else:
            raise


def create_path(path):
    if not os.path.exists(path):
        path = mkdir_p(path)
        raise FileNotFoundError("file/directory not found. path has been created load cvs") 
    else:
        pass
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


#def mk_file(file):
#    try:
#       open(file, 'x')
#    except FileExistsError:
#       pass

def use_csvs():
    """
    loads the csv files generates by the get_fx_m1/api module
    colnames = {'d1':'Bar OPEN Bid Quote', 
            'd2':'Bar HIGH Bid Quote', 
            'd3':'Bar LOW Bid Quote', 
            'd4' : 'Bar CLOSE Bid Quote', 
            'v': 'Volume'}
    """
    path = create_path('fanalysis\\data\\get_fx_data')
    #collect files from data folder
    files = os.listdir(path) #use os.getcwd() if files in same path. otherwise set path
    files = str_listconcat(files, path + "\\")
    #read and combine data
    header= ['date', 'd1', 'd2', 'd3', 'd4', 'v']
    dtypes = {'d1': 'float32',   
              'd2': 'float32', 
              'd3': 'float32', 
              'd4': 'float32', 
              'v': 'float32'}
    
    #could use numpy.memmap for partial read
    
    fx = path + '\\DAT_ASCII'
    ln = len(fx)

    files_csv = [pd.read_csv(f, sep = ";", header = None, names=header, parse_dates = ['date'], 
        dtype = dtypes, infer_datetime_format=True) 
        for f in files if f[-3:] == 'csv' and f[:ln] == fx]
            
    df = pd.concat(files_csv, ignore_index=True)
    

    #set date
    #from datetime import datetime
    print(df[:10])
    #df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y%m%d %H%M%S'))
    df.set_index('date')
    return df


if __name__ == '__main__':
    df = use_csvs()  
    import plotting as p
    #import structure as s
    #df = s.add_rand(df)
    #df = s.datesplit(df)
    #df = s.lag_var(df, 'd1', -1)
    print(df.columns)
    colnames = {'d1':'Bar OPEN Bid Quote', 
            'd2':'Bar HIGH Bid Quote', 
            'd3':'Bar LOW Bid Quote', 
            'd4' : 'Bar CLOSE Bid Quote', 
            'v': 'Volume'}
    headers = [ k for k in colnames][:-1]
    #headers = ['d1','d2', 'd3', 'd4']
    p.graph_vars(df, headers)
    
    #import dfConvert as dfC
    #dfC.df_store("c").store_df(df)


