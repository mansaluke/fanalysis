import os
import json
from pprint import pprint


def df_to_json(df):
    import pandas as pd
    import json
    import random as rd
    from datetime import datetime
    print(df[:10])
    f = os.path.isfile('x.json')
    if f==True:
        r = input('your existing json file will be replaced. proceed?(y/n) ')
        a = True
        while a:
            if r == 'y':
                os.remove('x.json')
                a = False
            elif r == 'n':
                a= False
                print('process terminated')
                os._exit(1)
            else:
                a = True
    df.to_json('x.json', orient='table', date_unit='s')
    f=open('x.json', 'r')
    print(f.read())

def json_load(jfile):
    import pandas as pd
    with open(jfile, 'r') as f:
        df = json.load(f)
    df = df['data']
    df = pd.DataFrame(df)
    return df


files = os.listdir('.')
jsontype = '.json'


def user_input():
    l = True
    while l:
        c = input('do you want to create data or use existing data. (enter c to create, e to existing and t to terminate process) ')
        c=c.lower()
        if c =='e':
            if not any(fname.endswith(jsontype) for fname in files):
                import extract as e
                df =e.use_csvs()
                df_to_json(df)
            df = json_load('x.json')
            print(df[:10])
            l = False
            return df
            break
        elif c=='c': 
            import generatedata
            try:
                df = generatedata.df
                df_to_json(df)
                print(df)
                return df
            except:
                print('something went wrong')
                pass
            l = False
            break
        elif c=='t':
            print('Process terminated')
            l = False
            break
        else:    
            print('Response not recognised')
            #l = False
            #continue

if __name__== '__main__':
    df = user_input()   
    #df = json_load('x.json')


