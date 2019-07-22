"""
consists of class df_store which allows the user to 
easily store and load their panda dataframes. current storage formats include: json, csv, parquet, pickle, feather and HDF5
--df_store('test.json').load_df()
--df_store('test.json').store_df(df)
--to be incorporated: BSON
"""
from datetime import datetime
import pandas  as pd
from calendar import monthrange
import sys, os
from misc import Ipython
import pandas as pd
import json
import pickle
import feather


try:
    import pyarrow.parquet as pq
except ImportError:
    pass
#from tqdm import tqdm

storagetypes = ["pickle", "json", "csv", "parquet", "feather", "h5"]
storagetypes_dict = {"pickle": "", "json": "json", "csv": "csv", "parquet": "parquet", "feather": "feather", "HDF5": "h5" }

from misc import Ipython
if Ipython.run_from_ipython()==True:
    print('Ipython active')
    standardpath='data'
else:
    print('Ipython not active')
    standardpath = 'fanalysis\\data'

class df_store:
    """
    loads/stores specified files to and from pickle, json, csv or parquet formats 
    e.g.1 df_store('test.json').load_df()
    e.g.2 df_store('test.json').store_df(df)
    *args = path parts. if no path entered the default fanalysis\\data is used
    parquet format: "test.parquet.gzip" 
    to store and load in current directory simply: df_store('test.csv', 'fanalysis').load_df()
    """

    def __init__(self, filename, *args):
        if args:
            self.filename = os.path.join(*args, filename)
        else:
            self.filename = os.path.join(standardpath, filename)
        try:
            self.filetype = self.filename.split(".",-1)[1]
        except:
            self.filetype = "pickle"

    def load_df(self):     
        filename = self.filename
        filetype = self.filetype   

        if self.check_file_exists(filename) == False:
            print('path: ' + filename  )
            raise FileExistsError('File does not exist')

        if filetype in storagetypes:
            fn = "self." + filetype + "_load(filename)"
            print("Loading "+ filetype + ": " + filename + "...")

            try:
                dataframe = eval(fn)
                #tqdm slows down code considerably
                #for index in tqdm(dataframe.iterrows(), total=dataframe.shape[0]):
                #    pass


                if dataframe is not None:
                    print("dataframe loaded successfully")

            except:
                raise OSError("could not load "+filetype+". Check file exists - file may be too large.")
            return dataframe
        else:
            raise ValueError("Cannot load that file type. Please check file name and try again.")                          
 
    def check_file_exists(self, filename): 
        return os.path.exists(filename)

    def pickle_load(self, pfile):
        with open(pfile,'rb') as pObject:
            df = pickle.load(pObject)
        df = pd.DataFrame(df)
        return df

    def json_load(self, jfile):    
        df = pd.read_json(jfile, orient='records') #, convert_dates=['date'])
        return df

    def csv_load(self, csvfile):    
        df = pd.read_csv(csvfile) 
        return df
    
    def parquet_load(self, pfile):
        table = pq.read_table(pfile)
        df = table.to_pandas()
        return df
    
    def feather_load(self, ffile):
        #df = pd.read_feather(ffile)
        df = feather.read_dataframe(ffile)
        return df
    
    def h5_load(self, hdffile):
        df = pd.read_hdf(hdffile, 'df')
        return df




    def store_df(self, dataframe): 
        filename = self.filename
        filetype = self.filetype
        print(filename)
        
        if self.user_input_file_exists(filename) == True:
            raise NameError("Filename already exists. please try again")
        
        if filetype in storagetypes:
            fn = "self.dfto" + filetype + "(dataframe, filename)"
            print("Storing "+ filetype + ": " + filename + "...")
            
            exec(fn)
            #tqdm slows down code considerably
            #for index in tqdm(dataframe.iterrows(), total=dataframe.shape[0]):
            #        pass
                    
            print("dataframe stored successfully")
            return filename
        
        else:
            raise ValueError("Cannot store that file type. Please check file name and try again.")
    
    def user_input_file_exists(self, filename):
        #Check whether file already exists
        filetype = self.filetype
        f = os.path.isfile(filename)
        if f==True:           
            a = True
            while a:
                r = input(filetype+' file with the same name found. Your existing '+filetype+' file will be replaced. proceed?(y/n) ')
                if r == 'y':    
                    os.remove(filename)
                    return False
                elif r =='n':
                    return True
                else:
                    a = True

    def dftopickle(self, dataframe, filename):
        with open(filename,'wb') as fObject:
            pickle.dump(dataframe,fObject, pickle.HIGHEST_PROTOCOL)   

    def dftojson(self, dataframe, filename):
        dataframe.to_json(filename, orient='records')
        print("dataframe successfully loaded to json")

    def dftocsv(self, dataframe, filename):
        dataframe.to_csv(filename, sep='\t')
        print("dataframe successfully loaded to csv")

    def dftoparquet(self, dataframe, filename):
        """
        Requirements: Visual C++ Redistributable for Visual Studio 2015.
        and python 64 bit
        """
        dataframe.to_parquet(filename,compression='gzip')
        #table = pd.Table.from_pandas(dataframe, preserve_index=True)
        #pq.write_table(table, filename)
        print("dataframe successfully loaded to parquet")

    def dftofeather(self, dataframe, filename):
        feather.write_dataframe(dataframe, filename)
    
    def dftoh5(self, dataframe, hdffile):
        #e.g. data.h5
        dataframe.to_hdf(hdffile, key= 'df', mode='w')



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





def use_csvs(path = 'fanalysis\\data\\get_fx_data'):
    """
    loads the csv files generates by the get_fx_m1/api module
    colnames = {'d1':'Bar OPEN Bid Quote', 
            'd2':'Bar HIGH Bid Quote', 
            'd3':'Bar LOW Bid Quote', 
            'd4' : 'Bar CLOSE Bid Quote', 
            'v': 'Volume'}
    """
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
    

    df.set_index('date')
    return df







if __name__=='__main__':

    import generatedata as g
    df = g.create_brownian_motion()
    df = pd.DataFrame(df)  

    filename = "bm.feather" 

    f = df_store(filename).store_df(df)
    print("filename: " + f)
    print("load")
    df = df_store(filename).load_df()
    t = df_store(filename).filetype
    print(df)
    print(t)
    #df = df_store(filename).load_df()

