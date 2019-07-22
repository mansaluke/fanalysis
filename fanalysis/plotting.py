from misc import Ipython
import time
import matplotlib
from misc import Ipython
if Ipython.run_from_ipython()!=True:
    matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np

date_attr = ['date', 'Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 
            'Is_quarter_start', 'Is_year_end', 'Is_year_start',
            'Hour', 'Minute', 'Second', 'not_dupym', 'daysinmonth',
            'aggdays']


class plots:
    """
    Produces graphs looping through time series a.k.a headers
    insert headers as list
    --e.g. 1.   plots(df, None, 1) - can pass none into headers to plot all headers against date
    --e.g. 2.   plots.graph_vars(df, ['rnd'], 1) - can run function directly
    """ 
    def __init__(self, df, header = None, p = 0.05, seperate=False, legend = False, point=None):
        self.df, self.header, self.p, self.seperate, self.legend, self.point = df, header, p, seperate, legend, point
        self.date_col = self.df.select_dtypes(include=[np.datetime64]).columns[0]
        
        if self.header is None:
            self.header = df.columns.values
        try:
            list(self.header)
        except:
            raise ValueError("header should be a list")

        self.graph_vars(self.df, self.header, self.p, self.seperate, False, self.point)

    @staticmethod
    def graph_vars(df, header = None, p = 0.05, seperate=False, legend=False, point=None):
        """
        Produces graphs looping through time series a.k.a headers
        insert headers as list
        point as datindex in df
        """ 
        try:
            date_col = self.date_col
        except:
            date_col = df.select_dtypes(include=[np.datetime64]).columns[0]
        
        if Ipython.run_from_ipython() is False:
            plt.rcParams['figure.figsize'] = (15, 5)
            try:
                for h in header:
                    if h not in date_attr:
                        if point == None:
                            plt.plot(df[date_col], df[h])
                            plt.title([h])
                            plt.xlabel('Date')
                            plt.pause(p)
                            plt.show(block=False)
                            time.sleep(0.5)
                            plt.close
                        else: 
                            plt.plot(df[date_col], df[h], 'b')
                            plt.plot(df.loc[point, date_col] , df.loc[point, h] , 'rD')
                            plt.title([h])
                            plt.xlabel('Date')
                            #plt.pause(p)
                            plt.show()
                            #time.sleep(0.5)
                            #plt.clf 
                            #plt.close
            except:
                pass

        elif Ipython.run_from_ipython() is True:
            if seperate is False:
                for h in header:
                    if h not in date_attr:
                        if point == None:
                            plt.plot(df[date_col], df[h], label = h)
                            if legend == True:
                                plt.legend(loc = 'upper left')
                        else:
                            plt.plot(df[date_col], df[h], 'b')
                            plt.plot(df.loc[point, date_col] , df.loc[point, h] , 'rD')
                            plt.show()
            elif seperate is True:
                for h in header:
                    if h not in date_attr:
                        plt.plot(df[date_col], df[h]) 
                        plt.title([h])
                        plt.show()


if __name__ == "__main__":
    #from generatedata import data
    #c = data(1000, "d").genseries()
    #print(c.head())
    #plots(c, None, 1)
    #plots.graph_vars(df, ['rnd'], 1)

    from dfconvert import df_store
    df=df_store('quanddata').load_df().reset_index()
    print(df.head())
    import pandas as pd
    df=df.sort_index()
    plots.graph_vars(df, ['Open'], point = 2)
