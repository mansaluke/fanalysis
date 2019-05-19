# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""


x = 3

import pandas as pd
import sys, os
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
import main as m
import generatedata as g
import extract as e
import structure as s 
from plotting import plots
import dfConvert as d
import unittest

if x == 1:
    df = m.user_input()
    #df = g.df_user()
    #df = d.df_store('x.json').load_df()
    print("done")
    df = s.date_split(df)
    df = s.lag_var(df, 'rnd', -1)
    df['ts'] = df['aggdays'] *0.02 + df['rnd']
    df = s.add_rand(df)

elif x == 2:
    df = e.use_csvs()
    df = s.date_split(df)
    df = s.lag_var(df, 'd1', -1)
    df['ts'] = df['aggdays'] *0.02 + df['d1']
    df = s.add_rand(df)

elif x == 3:
    df = d.df_store('x.json').load_df()

print("done")
print(df.dtypes)
print(df.head())
print(df.columns)
print("done")

d.df_store('x.csv').store_df(df)


try:
    plots(df, None)
except:
    plots(df, None)

