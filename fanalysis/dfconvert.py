"""
consists of class df_store which allows the user to 
easily store and load their panda dataframes. current storage formats include: json, csv 
and parquet
--try: df_store('test.json').load_df() and df_store('test.json').store_df(df)
--to be incorporated: feather, mongodb, csv, pickle
"""
import pandas as pd
import json
import os
import pickle
try:
    import pyarrow.parquet as pq
except ImportError:
    pass


storagetypes = ["pickle", "json", "csv", "parquet"]
standardpath = 'fanalysis\\data'

class df_store:
    """
    loads/stores specified files to and from pickle, json, csv or parquet formats 
    e.g.1 df_store('test.json').load_df()
    e.g.2 df_store('test.json').store_df(df)
    *args = path parts. if no path entered the default fanalysis\\data is used
    parquet format: "test.parquet.gzip" 
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
            raise FileExistsError('File does not exist')
        if filetype in storagetypes:
            fn = "self." + filetype + "_load(filename)"
            print("Loading "+ filetype + ": " + filename + "...")
            try:
                dataframe = eval(fn)
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
        Require: Visual C++ Redistributable for Visual Studio 2015.
        and python 64 bit
        """
        dataframe.to_parquet(filename,compression='gzip')
        #table = pd.Table.from_pandas(dataframe, preserve_index=True)
        #pq.write_table(table, filename)
        print("dataframe successfully loaded to parquet")



if __name__=='__main__':

    import BrownianMotion as BM
    DF = BM.create_brownian_motion()
    df = pd.DataFrame(df)  

    filename = "x.json" 

    f = df_store(filename).store_df(df)
    print("filename: " + f)
    print("load")
    df = df_store(filename).load_df()
    t = df_store(filename).filetype
    print(df)
    print(t)


