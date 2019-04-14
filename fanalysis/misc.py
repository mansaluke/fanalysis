# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

if __name__=='__main__':
    print(run_from_ipython())


