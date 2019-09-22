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


class graph_vars():
    """
    Produces graphs looping through time series a.k.a headers
    insert headers as list


    """ 
    def __init__(self, df, header = None, fmt='.', pause = 0.5, point=None, legend = False):
        self.df, self.header, self.fmt, self.pause, self.legend, self.point = \
            df, header, fmt, pause, legend, point
        self.date_col = self.df.select_dtypes(include=[np.datetime64]).columns[0]
        
        day_diff = (self.df[self.date_col].max() -  self.df[self.date_col].min()).days

        if day_diff>= 28:
            self.ymd = True 
        else:
            self.ymd = False

        if self.header is None:
            self.header = df.columns.values

    def _get_header(self):
        return self.__header

    def _set_bar(self, value):
        if not isinstance(value, list):
            raise TypeError("header must be a list")
        self.__header = value
        
    header = property(_get_header, _set_bar)

    def plot(self):
        """
        Produces graphs looping through time series a.k.a headers
        insert headers as list
        point as datindex in df
        """ 

        #set subplots
        fig, ax = plt.subplots()

        if Ipython.run_from_ipython() is False:
            plt.rcParams['figure.figsize'] = (15, 5)
            for h in self.header:
                if h not in date_attr and h != self.date_col:  
                    ax.plot(self.df[self.date_col], self.df[h], self.fmt, label = h)
                    if self.point != None:
                        ax.plot(self.df.loc[self.point, self.date_col], self.df.loc[self.point, h], self.fmt)

                    if self.ymd == True:
                        fig.autofmt_xdate()
                        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
                    
                    plt.xlabel('Date')

                    if self.pause is not None:
                        ax.set_title([h])
                        plt.show(block=False)
                        plt.pause(self.pause)
                        plt.close

                        if h == self.header[-1]:
                            plt.close('all')

            if self.pause is None:
                ax.set_title(self.header)
                plt.show()


        elif Ipython.run_from_ipython() is True:
            for h in self.header:
                if h not in date_attr and h != self.date_col:
                        #plt.plot(self.df[self.date_col], self.df[h], self.fmt, label = h)
                        ax.plot(self.df[self.date_col], self.df[h], self.fmt, label = h)
                        if self.point != None:
                            ax.plot(self.df.loc[self.point, self.date_col] , self.df.loc[self.point, h] , self.fmt)
                        if self.ymd == True:
                            fig.autofmt_xdate()
                            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
                        plt.show()
                        if self.legend == True:
                            plt.legend(loc = 'upper left')



       
if __name__ == "__main__":

    from dfconvert import df_store
    df = df_store('bm').load_df()
    #print(df.head())
    #import pandas as pd
    #df=df.sort_index()
    
    graph_vars(df, ['bm']).plot()
