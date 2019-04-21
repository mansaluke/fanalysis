from misc import run_from_ipython
import time
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt

def graph_vars(df, header, p = 0.01):
    """
    Produces graphs looping through time series a.k.a headers
    """
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
    if run_from_ipython() is False:
        plt.rcParams['figure.figsize'] = (15, 5)
        #plt.figure(); df.plot();plt.legend(loc='best')
        for h in header:
            plt.plot(df['date'], df[h])
            plt.title([h])
            plt.xlabel('Date')
            plt.pause(p)
            plt.show(block=False)
            time.sleep(0.5)
            plt.close
            #plt.gcf()
    elif run_from_ipython() is True:
        for h in header:
            plt.plot(df['date'], df[h]) 
            plt.title([h])
            #plt.show
            plt.savefig('x.png', bbox_inches='tight')