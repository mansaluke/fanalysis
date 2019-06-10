from misc import Ipython
import time
import matplotlib
from misc import Ipython
if Ipython.run_from_ipython()!=True:
    matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

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
    def __init__(self, df, header = None, p = 0.05, seperate=False, legend = False):
        self.df, self.header, self.p, self.seperate, self.legend = df, header, p, seperate, legend
        if self.header is None:
            self.header = df.columns.values
        try:
            list(self.header)
        except:
            raise ValueError("header should be a list")

        self.graph_vars(self.df, self.header, self.p, self.seperate)

    @staticmethod
    def graph_vars(df, header = None, p = 0.05, seperate=False, legend=False):
        """
        Produces graphs looping through time series a.k.a headers
        insert headers as list
        """ 
        try:
            df = self.df
            header = self.header
            p = self.p
        except:
            pass
        if Ipython.run_from_ipython() is False:
            plt.rcParams['figure.figsize'] = (15, 5)
            for h in header:
                if h not in date_attr:
                    plt.plot(df['date'], df[h])
                    plt.title([h])
                    plt.xlabel('Date')
                    plt.pause(p)
                    plt.show(block=False)
                    time.sleep(0.5)
                    plt.close
        elif Ipython.run_from_ipython() is True:
            if seperate is False:
                for h in header:
                    if h not in date_attr:
                        plt.plot(df['date'], df[h], label = h)
                        if legend == True:
                            plt.legend(loc = 'upper left')
            elif seperate is True:
                for h in header:
                    if h not in date_attr:
                        plt.plot(df['date'], df[h]) 
                        plt.title([h])
                        plt.show()


if __name__ == "__main__":
    from generatedata import data
    df = data(1000, "d").genseries()
    print(df.head())
    plots(df, None, 5)
    #plots.graph_vars(df, ['rnd'], 1)
