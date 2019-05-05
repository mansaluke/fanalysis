import os
import json
from pprint import pprint
from misc import run_from_ipython
import pandas as pd

def df_to_json(df):
    try:       
        import json
        f = os.path.isfile('x.json')
        if f==True:
            r = input('your existing json file will be replaced. proceed?(y/n) ')
            a = True
            while a:
                if r == 'y':
                    os.remove('x.json')
                    df.to_json('x.json', orient='records', date_unit='s')
                    f=open('x.json', 'r')
                    print("json created successfully")
                    a = False
                elif r == 'n':
                    a= False
                    print('process terminated')
                    if run_from_ipython == False:
                        os._exit(1)
                    else:
                        break
                else:
                    a = True
        elif f==False:
            df.to_json('x.json', orient='records', date_unit='s')
            f=open('x.json', 'r')
            print("json created successfully")
    except:
        print("no json created - process failed")

def json_load(jfile='x.json'):
    try:
        df = pd.read_json(jfile, orient='records', convert_dates=['date'])
        print("json loaded successfully")
        return df
    except:
        print("could not load json")


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
        elif c=='c': 
            import generatedata
            try:
                df = generatedata.df_user()
                df_to_json(df)
                print(df.head())
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


if __name__== '__main__':
    df = user_input()   
    #df = json_load('x.json')
