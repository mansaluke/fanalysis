import numpy as np
import pandas as pd 
from datetime import datetime
import random as rd

def gen_uniform(low=-0.2,high=0.2):
    """
    Generates 50 randomly generated points between 0 and 1. low and high values alter the variance
    """
    import matplotlib.pyplot as plt
    x = np.linspace(0, 1)  
    y = x + np.random.uniform(low,high,x.shape)
    plt.scatter(x, y)
    plt.show()
    return x, y


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
                d = 'end'
            if 'd' not in locals():
                t=[]
                for i in range(len(times)):
                    t.append(times[i])
                rnd=[]
                for i in range(self.p):
                    rnd.append(rd.random())
                #d = pd.DataFrame( rnd, times, columns=['rnd'])
                #d = pd.DataFrame( {'date': times, 'rnd':rnd}, columns=['date', 'rnd'])
                np.column_stack([t, rnd])
                d = pd.DataFrame(np.column_stack([t, rnd]), columns=['date', 'rnd'])
                print("data created")
            return d
    except ValueError as err1:
        print("Cannot generate that many periods. Please try again")
        d = "end"

    
def df_user():
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
                    print(df.head())
                    if not isinstance(df, str):
                        uf = False
                    return df
                except ValueError:
                    print('Non-numeric data inputted. Please try again.')
            elif f =='t':
                uf = False
                break
        else:
            print('response not recognised. Please try again.')




if __name__ == '__main__':
    df_user()
