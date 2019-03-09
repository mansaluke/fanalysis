import numpy as numpy
import pandas as pd 
from datetime import datetime
import random as rd

class data:
    '''create data'''
    def __init__(self, p, f):
        self.p, self.f = p, f
    try:
        def genseries(self):
            '''generates data'''
            try:
                times = pd.date_range(end=datetime.now(), periods=self.p, freq=self.f)
            except:
                print("Cannot generate that many periods. Please try again")
                l = 'end'
            if 'l' not in locals():
                t=[]
                for i in range(len(times)):
                    t.append(times[i])
                rnd=[]
                for i in range(self.p):
                    rnd.append(rd.random())
                l = pd.DataFrame( rnd, times, columns=['rnd'])
            return l
    except ValueError as err1:
        print("Cannot generate that many periods. Please try again")
        l = "end"
    

print('you will need to choose the frequency and number of periods of the data. e.g. 10 days')
uf = True

while uf:
    f = input('please choose a frequency or press t to terminate (enter d for day or m for month) ')
    if f == 'd' or f =='m' or f=='t':
        if f != 't':
            if f=='d':
                freq='days'
            elif f=='m':
                freq='months'
            p = input('How many {} would you like to generate? '.format(freq))
            try:
                p = int(p)
                d = data(p, f)
                df = d.genseries()
                print(df)
                if not isinstance(df, str):
                    uf = False
                break
            except ValueError:
                print('Non-numeric data inputted. Please try again.')
        elif f =='t':
            uf = False
            break
    else:
        print('response not recognised. Please try again.')


