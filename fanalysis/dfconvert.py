"""
consists of two clases (storage_to_df and df_to_storage) which allow the user to 
easily store and load their panda dataframes. current storage formats include: json 
and parquet
--to be incorporated: feather, mongodb, csv
"""
import pandas as pd
import json
import os
from extract import create_path
try:
    import pyarrow.parquet as pq
except ImportError:
    pass



class storage_to_df:
    """
    loads specified file from json or parquet format e.g. df = storage_to_df('x.json').file
    """
    def __init__(self, filename):
        self.filename = filename
        self.filetype = filename.split(".",1)[1]
        if self.filetype == "json":
            self.file = self.json_load()
 
    def check_file_exists(self, filename): return os.path.isfile(filename)

    def json_load(self, jfile='x.json'):    
        #files = os.listdir('.')
        #if not any(fname.endswith('.json') for fname in files):
        #    raise FileNotFoundError('No json file found.')
        if self.check_file_exists == False:
            raise FileExistsError('File does not exist')
        try:    
            import pandas as pd
            df = pd.read_json(jfile, orient='records', convert_dates=['date'])
            return df
        except:
            print("could not load json - file may be too large.")
    
    def parquet_load(self, pfile='x.parque'):
        table2 = pq.read_table(pfile)
        table2.to_pandas()

   

class df_to_storage:
    """
    loads specified file into json or parquet format e.g. df_to_storage(df, 'x.json')
    """
    def __init__(self, dataframe, filename):
        
        self.filename = filename
        self.filetype = filename.split(".",1)[1]
        self.dataframe = dataframe
        print(filename)
        print(self.filetype)
        if self.user_input_file_exists(filename) == True:
            raise NameError("The filename already exists. please try again")
        if self.filetype == "json":
            self.dftojson(dataframe, filename)
        if self.filetype == "parquet":
            self.dftoparquet(dataframe, filename)



    def user_input_file_exists(self, filename):
        #Check whether file already exists
        f = os.path.isfile(filename)
        if f==True:
            r = input('your existing json file will be replaced. proceed?(y/n) ')
            a = True
            while a:
                if r == 'y':    
                    os.remove(filename)
                    return False
                elif r =='n':
                    return True
                else:
                    a = True


    def dftojson(self, dataframe, filename):
        dataframe.to_json(filename, orient='records')
        print("dataframe successfully loaded to json")
        #f=open(filename, 'r')
        #print(f.read())



    def dftoparquet(self, dataframe, filename):
        """
        Require: Visual C++ Redistributable for Visual Studio 2015.
        and python 64 bit
        """
        table = pd.Table.from_pandas(dataframe, preserve_index=True)
        pq.write_table(table, filename)



if __name__=='__main__':
    df = storage_to_df('x.json').file
    #df_to_storage(df, 'x.json')
    #df_to_storage(df, 'x.parquet')
