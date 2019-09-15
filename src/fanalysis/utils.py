# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""

    

class Ipython():
    @staticmethod
    def run_from_ipython():
        try:
            __IPYTHON__
            return True
        except NameError:
            return False

class timing():
    import threading
    from datetime import datetime, timedelta

    local = threading.local()
    class ExecutionTimeout(Exception): pass

    def start(max_duration = timedelta(seconds=1)):
        local.start_time = datetime.now()
        local.max_duration = max_duration

    def check():
        if datetime.now() - local.start_time > local.max_duration:
            raise ExecutionTimeout()

    def do_work():
        start()
        while True:
            check()
            # do stuff here
        return 10


def df_islarge(df):
    if df.memory_usage().sum()>100*10^6: return True
    else: return False

    
    
def df_describe(df, col_details = True, columns = None):
    """
    returns dataframe statistics
    col_details : column analysis
    
    """
    
    print('Number of rows: {:23} \nNumber of columns: {:20} \nDataframe size: {:20} mb'
          .format(len(df), len(df.columns), df.memory_usage().sum()/1000000))

    if df_islarge(df):
        print('Large dataset warning')
    
    if col_details == True:
        if columns == None:
            print('columns: ', df.columns.values)
            print(df.describe().T)
            print(df.isnull().sum())
        
        else:
            for col in columns:
                print('Column: {:20} \nType: {:20} \nMemory usage: {:20}'
                      .format(col, str(df[col].dtype), df[col].memory_usage()/1000000))
                #print(df[col].describe())
                print('Number of nulls: ', df[col].isnull().sum())
                