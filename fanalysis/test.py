# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""


x = 1

import pandas as pd
import main as m
import extract as e
import structure as s
import plotting
import generatedata as g
import dfconvert as d

if x == 1:
    #df = m.user_input()
    #df = g.df_user()
    df = d.storage_to_df('x.json').file
    print("done")
    df = s.date_split(df)
    df = s.lag_var(df, 'rnd', -1)
    df['ts'] = df['aggdays'] *0.02 + df['rnd']

elif x == 2:
    df = e.use_csvs()
    df = s.date_split(df)
    df = s.lag_var(df, 'd1', -1)
    df['ts'] = df['aggdays'] *0.02 + df['d1']

print(df.dtypes)
print("done")
df = s.add_rand(df)
print(df.head())
print(df[['date', 'ts']])
print(df.columns)

#plotting.graph_vars(df, ['d1', 'd2', 'd3'])
plotting.graph_vars(df, df.columns)

