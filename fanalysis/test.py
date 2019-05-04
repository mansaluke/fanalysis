# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""


x = 2

import pandas as pd
import main as m
import extract as e
import structure as s
import plotting
import generatedata as g

if x == 1:
    #df = m.user_input()
    #df = g.df_user()
    df = m.json_load('x.json')
    print("done")

elif x == 2:
    df = e.use_csvs()

print(df.dtypes)
df = s.date_split(df)
print("done")
df = s.add_rand(df)
df = s.lag_var(df, 'd1', -1)
print(df.head())
df['ts'] = df['aggdays'] *0.02 + df['d1']
print(df[['date', 'ts']])
print(df.columns)

plotting.graph_vars(df, ['d1', 'd2', 'd3'], 1)
#import matplotlib.pyplot as plt
#count_row = df.shape[0] 
#plt.plot(df['date'], df['ts'])

#plt.show()
