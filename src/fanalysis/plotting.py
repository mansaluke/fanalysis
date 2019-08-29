import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np

try:
    from fanalysis.utils import Ipython
except ImportError:
    from utils import Ipython

if Ipython.run_from_ipython()!=True:
    matplotlib.use('tkAgg')

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
    def __init__(self, df, header = None, fmt='.', p = 0.05, seperate=False, legend = False, point=None):
        self.df, self.header, self.fmt, self.p, self.seperate, self.legend, self.point = df, header, p, fmt, seperate, legend, point
        self.date_col = self.df.select_dtypes(include=[np.datetime64]).columns[0]
        
        if self.header is None:
            self.header = df.columns.values
        try:
            list(self.header)
        except:
            raise ValueError("header should be a list")

        self.graph_vars(self.df, self.header, self.p, self.seperate, False, self.point)

    @staticmethod
    def graph_vars(df, header = None, fmt='.', p = 0.05, seperate=False, legend=False, point=None):
        """
        Produces graphs looping through time series a.k.a headers
        insert headers as list
        point as datindex in df
        """ 
        try:
            date_col = self.date_col
        except:
            date_col = df.select_dtypes(include=[np.datetime64]).columns[0]
        
        #set subplots
        fig, ax = plt.subplots()

        if Ipython.run_from_ipython() is False:
            plt.rcParams['figure.figsize'] = (15, 5)
            try:
                for h in header:
                    if h not in date_attr and h != date_col:
                        if point == None:
                            #plt.plot(df[date_col], df[h], fmt)
                            ax.plot(df[date_col], df[h], fmt, label = h)
                            plt.title([h])
                            ax_set.xlabel('Date')
                            plt.pause(p)
                            fig.autofmt_xdate()
                            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
                            plt.show(block=False)
                            #time.sleep(0.5)
                            plt.close
                        else: 
                            ax.plot(df[date_col], df[h], 'b')
                            ax.plot(df.loc[point, date_col] , df.loc[point, h] , fmt)
                            ax.set_title([h])
                            plt.xlabel('Date')
                            #plt.pause(p)
                            fig.autofmt_xdate()
                            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
                            plt.show()
                            #time.sleep(0.5)
                            #plt.clf

                        if h == header[-1]:
                            plt.close('all')
            except:
                pass

        elif Ipython.run_from_ipython() is True:
            if seperate is False:
                for h in header:
                    if h not in date_attr and h != date_col:
                            #plt.plot(df[date_col], df[h], fmt, label = h)
                            ax.plot(df[date_col], df[h], fmt, label = h)
                            if point != None:
                                ax.plot(df.loc[point, date_col] , df.loc[point, h] , fmt)
                            fig.autofmt_xdate()
                            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
                            plt.show()

                            if legend == True:
                                plt.legend(loc = 'upper left')

            elif seperate is True:
                for h in header:
                    if h not in date_attr:
                        ax.plot(df[date_col], header) 
                        fig.autofmt_xdate()
                        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
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
