import pandas as pd
import random as rd
import json
from datetime import datetime
from calendar import monthrange
from numba import jit
import numpy as np
import matplotlib.pyplot as plt
from plotting import plots


class outlier_detect():
    """
    finds the observations with the largest variance
    e.g.
    a = outlier_detect(df, 'Open', graph = True)
    print(a.outliers)
    a.zoom_in(remove_option=True)
    """
    def __init__(self, df, variable, xlen = 10, graph = False):        
        self.df = df.copy()
        self.variable = variable
        self.xlen = xlen
        self.graph = graph
        self.date_col = df.select_dtypes(include=[np.datetime64]).columns[0]

        self.outliers = self.differences_collect()
        
        if self.graph == True:
            self.graph_outliers()
 
            
    def differences_collect(self):
        largest = self.df[[self.variable]].copy(deep=False)
        largest['diff_t'] = np.sqrt(((largest[self.variable].shift(1) - largest[self.variable])/largest[self.variable])**2)*100
        largest = largest.nlargest(self.xlen, 'diff_t')
        return largest

    def graph_outliers(self):
        plt.style.use('fivethirtyeight')
        x_values = list(range(self.xlen))
        plt.bar(x_values, self.outliers['diff_t'], orientation='vertical')
        plt.ylabel('% diff')
        plt.title('outliers')
        plt.show()

    def zoom_in(self, period = 20, remove_option = False):
        #zooms in so user can check whether they want to remove the outlier or not
        if isinstance(period, bool)==True:
            remove_option, period = period, 20
        
        anom_list = list(self.outliers.reset_index()['index'])
        remove = None

        for i in anom_list:
            start = self.df.loc[i, self.date_col]+ pd.DateOffset(-period/2)
            end = self.df.loc[i, self.date_col]+ pd.DateOffset(period/2)
            tmp = self.df[(self.df[self.date_col]>start) & (self.df[self.date_col]<end)][[self.date_col, self.variable]]
            
            if remove != 't':
                plots.graph_vars(tmp, [self.variable], point = i)
            #plt.plot(tmp[self.date_col], tmp[self.variable], 'b')
            #plt.plot(tmp.loc[i, self.date_col] , tmp.loc[i, self.variable] , 'rD')
            #plt.show()
        
            while remove_option == True:   

                remove = input('do you wish to remove this observation? (y/n/t to terminate): ' )

                if remove == 'y':
                    self.df = self.rm_outlier(i)
                    break
                if remove == 'n':
                    break
                if remove == 't':
                    remove_option=False
                    break

        remove_option=False
        
        try:
            self.df = self.df.set_index('index')
        except:
            pass
            
        return self.df
    
    def rm_outlier(self, outlier_index, toNaN = True):
        if toNaN == False:
            self.df.drop(self.df.index[outlier_index])
        elif toNaN != False:
            self.df.loc[self.df.index == outlier_index, self.variable] = np.NaN
        return self.df




@jit
def add_rand(df):
    rand = []
    for r in range(len(df)):
        rand.append(rd.random())
    rand = pd.Series(rand, name = 'randseries')
    df = pd.concat([df, rand], axis = 1)
    return df



def date_split(df, datename = 'date', time=False, errors="raise"):
    """
    Extracts date elements from pandas df:
    --year, month, week, day, hour, daysinmonth, aggdays
    """
    datecol = df[datename]

    datecol_dtype = datecol.dtype
    if isinstance(datecol_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        datecol_dtype = np.datetime64
    if not np.issubdtype(datecol_dtype, np.datetime64):
        df[datename] = datecol = pd.to_datetime(datecol, infer_datetime_format=True, errors=errors)


    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    
    for n in attr: 
        df[n] = getattr(datecol.dt, n.lower())
    
    if time==True: 
        attr = ['Hour', 'Minute', 'Second']
        try:
            for n in attr: 
                df[n] = getattr(datecol.dt, n.lower())
            raise ValueError
        except ValueError:
            print("No time element to extract.")
            raise
            
    df['not_dupym'] = 1 - df[['Month', 'Year']].duplicated()
    
    df_daysinmonth = df[df['not_dupym']==1].groupby(['Year', 'Month'], as_index=False)['Year', 'Month'].sum().apply(lambda row: monthrange(row['Year'].astype('int'), row['Month'].astype('int')), axis=1).str[1].reset_index().rename(columns={0:'daysinmonth'})
    days_first_month = df_daysinmonth.groupby(['Year', 'Month'])['daysinmonth'].sum().cumsum().idxmin()
    days_first_month = monthrange(days_first_month[0], days_first_month[1])[1]
    
    df_daysinmonth = df_daysinmonth.groupby(['Year', 'Month'])['daysinmonth'].sum().cumsum().transform(lambda x: x-days_first_month).reset_index()
    df = df.merge(df_daysinmonth, on = ['Year', 'Month'], how = 'left')
    df['aggdays']=df['daysinmonth'].fillna(0).astype('int') + df['Day'].astype('int')
    df.drop(columns=['not_dupym'], inplace=False)
    return df
    


def lag_var(df, var, lags):
    df[var+'_lag'+str(lags)]=df[var].shift(lags)
    return df



if __name__ == '__main__':
    x=0

    if x == 0:
        from dfconvert import df_store
        df=df_store('data').load_df().reset_index()
    elif x ==1:
        import extract as e
        df = e.use_csvs()
    print(df.head())
    #df = add_rand(df)
    #df = date_split(df, 'Date')
    #df = lag_var(df, 'Open', -1)
    a = outlier_detect(df, 'd3', graph = False)
    print(a.outliers)
    df = a.zoom_in(remove_option=True)
    print('done')
    plots(df, None, 1)



