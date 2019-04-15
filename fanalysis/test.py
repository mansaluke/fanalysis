# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""


x = 1

import main as m
if x == 1:
    df = m.user_input()
    import pandas as pd
    df = pd.DataFrame(df)
    #df = m.json_load('x.json')
    print("done")

elif x == 2:
    
    df = e.use_csvs()

import structure as s
#df = s.date_split(df)
print("done")
df['year'] = pd.DatetimeIndex(df['date']).year
print(df)
#df = s.add_rand(df)
#df = s.lag_var(df, 'rnd', -1)


#df['ts'] = df['aggdays'] *0.2 + + df['rnd']
#
#
#print(df[['date', 'ts']])
#print(df.columns)
#
#
#import matplotlib.pyplot as plt

#plt.plot(df['date'], df['day'])


