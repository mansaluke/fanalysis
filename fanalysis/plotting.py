from misc import Ipython
import time
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class plots:
    """
    Produces graphs looping through time series a.k.a headers
    insert headers as list
    --e.g. 1.   plots(df, None, 1) - can pass none into headers to plot all headers against date
    --e.g. 2.   plots.graph_vars(df, ['rnd'], 1) - can run function directly
    """ 
    def __init__(self, df, header = None, p = 0.05):
        self.df, self.p = df, p
        self.header = header
        if self.header is None:
            self.header = df.columns.values
        try:
            list(self.header)
        except:
            raise ValueError("header should be a list")

        self.graph_vars(self.df, self.header, self.p)

    @staticmethod
    def graph_vars(df, header = None, p = 0.05):
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
                if h != 'date':
                    plt.plot(df['date'], df[h])
                    plt.title([h])
                    plt.xlabel('Date')
                    plt.pause(p)
                    plt.show(block=False)
                    time.sleep(0.5)
                    plt.close
        elif Ipython.run_from_ipython() is True:
            for h in header:
                if h != 'date':
                    plt.plot(df['date'], df[h]) 
                    plt.title([h])
                    plt.savefig('plots\\x.png', bbox_inches='tight')


if __name__ == "__main__":
    from generatedata import data
    df = data(1000, "d").genseries()
    print(df.head())
    plots(df, None, 1)
    #plots.graph_vars(df, ['rnd'], 1)
