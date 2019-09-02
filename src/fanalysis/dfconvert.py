"""
consists of class df_store which allows the user to 
easily store and load their panda dataframes. current storage formats include: json, csv, parquet, pickle, feather and HDF5
--df_store('test.json').load_df()
--df_store('test.json').store_df(df)
-- TODO incorporate: BSON
"""
from datetime import datetime
import pandas  as pd
from calendar import monthrange
import sys, os
import pandas as pd
import json
import pickle

try:
    from fanalysis.utils import Ipython
    import fanalysis.utils as u
except ImportError:
    from utils import Ipython
    import utils as u



    
def try_import(module_names):

    import importlib

    failed_imports = []

    def import_module_fn(mod_in):
        try:
            #import mod_in
            mod_in = importlib.import_module(mod_in)
        except ImportError:
            failed_imports.append(mod_in)

    if isinstance(module_names, list):
        for mod in module_names:
            import_module_fn(mod)
    else:
        import_module_fn(module_names)

    if failed_imports ==[]:
        pass
    else:
        print('Unable to import ' + ', '.join(failed_imports))


#try_import(['feather', 'pyarrow.parquet'])

import feather


storagetypes = ["pickle", "json", "csv", "parquet", "feather", "h5"]
storagetypes_dict = {"pickle": "", "json": "json", "csv": "csv", "parquet": "parquet", "feather": "feather", "HDF5": "h5" }


if Ipython.run_from_ipython()==True:
    print('Ipython active')
    standardpath='data'
else:
    standardpath = 'data'

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
            mkdir_p(os.path.dirname(filename))
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
        table = pyarrow.parquet.read_table(pfile)
        df = table.to_pandas()
        return df
    
    def feather_load(self, ffile):
        #df = pd.read_feather(ffile)
        df = feather.read_dataframe(ffile)
        return df
    
    def h5_load(self, hdffile):
        try:
            df = pd.read_hdf(hdffile, 'df')
        except:
            import h5py
            df = h5py.File(filename, 'r')
            print("file loaded as {}".format(type(df)))
        return df




    def store_df(self, dataframe, replace_existing = True):
        """
        when replace_existing set to true any existing files with the same name will be automatically replaced
        """ 
        filename = self.filename
        filetype = self.filetype
        
        if self.user_input_file_exists(filename, replace_existing) == True:
            raise NameError("Filename already exists. please try again")
        
        if filetype in storagetypes:
            fn = "self.dfto" + filetype + "(dataframe, filename)"
            print("Storing "+ filetype + ": " + filename + "...")
            
            try:
                exec(fn)
            except:
                create_path(os.dirname(filename))
                exec(fn)
            #tqdm slows down code considerably
            #for index in tqdm(dataframe.iterrows(), total=dataframe.shape[0]):
            #        pass
                    
            print("dataframe stored successfully")
            return filename
        
        else:
            raise ValueError("Cannot store that file type. Please check file name and try again.")
    
    def user_input_file_exists(self, filename, replace_existing):
        """Checks whether file already exists
        when replace_existing set to true any existing files with the same name will be automatically replaced.
        """
        filetype = self.filetype
        f = os.path.isfile(filename)
        if f==True:           
            a = True
            while a:
                if replace_existing != True:
                    r = input(filetype+' file with the same name found. Your existing '+filetype+' file will be replaced. proceed?(y/n) ')
                else:
                    r = 'y'
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
        #pyarrow.parquet.write_table(table, filename)
        print("dataframe successfully loaded to parquet")

    def dftofeather(self, dataframe, filename):
        feather.write_dataframe(dataframe, filename)
    
    def dftoh5(self, dataframe, filename):
        #e.g. data.h5
        dataframe.to_hdf(filename, key= 'df', mode='w')



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
    loads the csv files generated by the get_fx_m1/api module
    """
    #collect files from data folder
    files = os.listdir(path) #use os.getcwd() if files in same path. otherwise set path
    files = str_listconcat(files, path + "\\")
    #read and combine data
    header= ['date', 'Bar OPEN Bid Quote', 'Bar HIGH Bid Quote', 'Bar LOW Bid Quote', 'Bar CLOSE Bid Quote', 'Volume']
    dtypes = {'d1': 'float32',   
              'd2': 'float32', 
              'd3': 'float32', 
              'd4': 'float32', 
              'v': 'float32'}
    
    #could use numpy.memmap for partial read
    
    fx = path + '\\DAT_ASCII'
    ln = len(fx)

    print('Loading files...')
    files_csv = [pd.read_csv(f, sep = ";", header = None, names=header, parse_dates = ['date'], 
        dtype = dtypes, infer_datetime_format=True) 
        for f in files if f[-3:] == 'csv' and f[:ln] == fx]
            
    df = pd.concat(files_csv, ignore_index=True)
    print('Files successfully loaded and concatenated.')

    df.set_index('date')
    return df







if __name__=='__main__':

    import generatedata as g
    #filename = 'pairs.csv'
    #df = df_store(filename).load_df()
    #t = df_store(filename).filetype
    #print(df.head())
    #print(t)
    #df = df_store(filename).load_df()
    try:
        df = df_store('pairs.csv', 'src', 'fanalysis', 'data').load_df()
        print(df.head())
    except:
        pass

