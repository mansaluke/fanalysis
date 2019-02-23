import os
import json
from pprint import pprint
import numpy as np

files = os.listdir('.')
jsontype = '.json'


def userinput():
    l = True
    while l:
        c = input('do you want to create data or use existing data. (enter c for create, e for existing and t to terminate process) ')
        c=c.lower()
        if c =='e':
            if not any(fname.endswith(jsontype) for fname in files):
                import extract
            else:
                with open('temp.json', 'r') as f:
                    df = json.load(f)
            l = False
            break
        elif c=='c': 
            import generatedata
            try:
                df = generatedata.df
                print(df)
            except:
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
userinput()            



