#to parquet, feather, mongodb, csv
import pandas as pd
import json
import os
from datetime import datetime
import pyarrow.parquet as pq
#times = pd.date_range(start=datetime.now(), periods= 1000, freq='d')
#t=[]
#for i in range(len(times)):
#    t.append(times[i])
#rnd=[]
#for i in range(1000):
#    rnd.append(rd.random())
#df = pd.DataFrame( rnd, times, columns=['rnd'])

#import extract as e
def dftojson(df):
    if df in locals():
        print(df[:10])

        f = os.path.isfile('x.json')
        if f==True:
            os.remove('x.json')

        df.to_json('x.json', orient='table', date_unit='ms')
        f=open('x.json', 'r')
        print(f.read())
    else:
        print('none')

def dftoparquet(df):
    table = pd.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, 'x.parquet')

