# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""

#import main
#df = jload('x.json')
#
#import structure
#df = add_rand(df)
#df = datesplit(df)
#df = lag_var(df, 'rnd', -1)
#
#print(df.head())

print("start")
import extract

print(df)
import structure
df = add_rand(df)
df = datesplit(df)
df = lag_var(df, 'rnd', -1)

df.drop