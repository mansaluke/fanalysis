import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def geometric_brownian_motion(T = 1, N = 100, mu = 0.1, sigma = 0.1, S0 = 20):   
    """
    dS=μS dt+σS dWt
    t = time
    n = no periods
    mu = drift
    sigma = stand dev
    w = standard brownian motion 
    S = geom standard brownian motion 
    s0 = start price
    """     
    dt = float(T)/N
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size = N) 
    W = np.cumsum(W)*np.sqrt(dt) ### standard brownian motion ###
    X = (mu-0.5*sigma**2)*t + sigma*W ### ITO'S LEMMA
    S = S0*np.exp(X) ### geometric brownian motion ###
    return S
dates = pd.date_range('2012-01-01', '2013-02-22')
T = (dates.max()-dates.min()).days / 365
N = dates.size
start_price = 100
y = pd.Series(
    geometric_brownian_motion(T, N, sigma=0.1, S0=start_price), index=dates)

y.plot()
plt.show()






import numpy as np
import matplotlib.pyplot as plt

seed = 5       
N  = 2.**6     # increments

def Brownian(seed, N):
    
    np.random.seed(seed)                         
    dt = 1./N                                    # time step
    b = np.random.normal(0., 1., int(N))*np.sqrt(dt)  # brownian increments
    W = np.cumsum(b)                             # brownian path
    return W, b


# brownian increments
b = Brownian(seed, N)[1]

# brownian motion
W = Brownian(seed, N)[0]
W = np.insert(W, 0, 0.)                      
# W_0 = 0. for brownian motion
#If we plot the Brownian increments we can see that the numbers oscillate as white noise, while the plot of the Brownian Motion 
# shows a path that looks similar to the movement of a stock price.

# brownian increments
#%matplotlib inline
plt.rcParams['figure.figsize'] = (10,8)
xb = np.linspace(1, len(b), len(b))
plt.plot(xb, b)
plt.title('Brownian Increments')
plt.show()




#import quandl
import dfconvert
#quandl.ApiConfig.api_key = "wDWwy32n6Sm4jg96yHPK"
#
#start = "2016-01-01"
#end = "2016-12-31"
#
#df = quandl.get("WIKI/AMZN", start_date = start, end_date = end)
df = dfconvert.df_store('quanddata').load_df()
#print(df.head())  # taking a look at the first 5 rows

adj_close = df['Adj. Close']
time = np.linspace(1, len(adj_close), len(adj_close))

plt.plot(time, adj_close)
plt.show()
print(df.head())
def daily_return(adj_close):
    returns = []
    for i in range(0, len(adj_close)-1):
        today = adj_close[i+1]
        yesterday = adj_close[i]
        daily_return = (today - yesterday)/yesterday
        returns.append(daily_return)
    return returns

returns = daily_return(adj_close)

mu = np.mean(returns)*252.           # drift coefficient
sig = np.std(returns)*np.sqrt(252.)  # diffusion coefficient

print(mu, sig)



# GBM Exact Solution

# Parameters
#
# So:     initial stock price
# mu:     returns (drift coefficient)
# sigma:  volatility (diffusion coefficient)
# W:      brownian motion
# T:      time period
# N:      number of increments

def GBM(So, mu, sigma, W, T, N):    
    t = np.linspace(0.,1.,N)
    S = []
    S.append(So)
    for i in range(1,int(N)):
        drift = (mu - 0.5 * sigma**2) * t[i]
        diffusion = sigma * W[i-1]
        S_temp = So*np.exp(drift + diffusion)
        S.append(S_temp)
    return S, t

seed = 22
So = adj_close[0]            # Initial AMZN stock price (01/01/2016)
W = Brownian(seed, N)[0]
T = 1.
N = 64

soln = GBM(So, mu, sig, W, T, N)[0]    # Exact solution
t = GBM(So, mu, sig, W, T, N)[1]       # time increments for  plotting
plt.plot(t, soln)
plt.ylabel('AMZN Stock Price, $')
plt.title('Geometric Brownian Motion - AMZN')

#f we overlay the actual stock prices, we can see how our model compares.



# adjusting the original time array from days to years
time = np.linspace(1, len(adj_close), len(adj_close))
time = [i/252. for i in time]

plt.plot(time, adj_close, label = 'Actual')
plt.plot(t, soln, label = 'GBM (seed = 22)', ls='--')

plt.ylabel('AMZN Stock Price, $')
plt.title('Geometric Brownian Motion - AMZN')

plt.legend(loc = 'upper left')



#We can also plot some other models with different random seeds to see how the path change
T = 1.
N = 2.**6
So = adj_close[0]

seed = 5
W = Brownian(seed, N)[0]
soln2 = GBM(So, mu, sig, W, T, N)[0]    

seed = 15
W = Brownian(seed, N)[0]
soln3 = GBM(So, mu, sig, W, T, N)[0]    

# adjusting the original time array from days to years
time = np.linspace(1, len(adj_close), len(adj_close))
time = [i/252. for i in time]

plt.plot(time, adj_close, label = 'Actual')
plt.plot(t, soln, label = 'GBM (seed = 22)', ls = '--')
plt.plot(t, soln2, label = 'GBM (seed = 5)', ls = '--')
plt.plot(t, soln3, label = 'GBM (seed = 15)', ls = '--')

plt.ylabel('AMZN Stock Price, $')
plt.title('Geometric Brownian Motion - AMZN')

plt.legend(loc = 'upper left')

#Now that we have some working GBM models, we can build an Euler-Maruyama Model to approximate the path.

T = 1.
N = 2.**6
So = adj_close[0]

seed = 5
W = Brownian(seed, N)[0]
soln2 = GBM(So, mu, sig, W, T, N)[0]    

plt.plot(t, soln2, label = 'GBM (seed = 5)', ls = '--')

plt.ylabel('AMZN Stock Price, $')
plt.title('Geometric Brownian Motion - AMZN')

plt.legend(loc = 'upper left')



# Exact solution - GBM Model
seed = 5
So = adj_close[0]            # Initial AMZN stock price (01/01/2016)
W = Brownian(seed, N)[0]
T = 1.
N = 2.**6

soln = GBM(So, mu, sig, W, T, N)[0]    # Exact solution
t = GBM(So, mu, sig, W, T, N)[1]       # time increments for  plotting
plt.plot(t, soln, label ='GBM')


# Euler Maruyama Approximation
def EM(So, mu, sigma, b, T, N, M):
    dt = M * (1/N)  # EM step size
    L = N / M
    wi = [So]
    for i in range(0,int(L)):
        Winc = np.sum(b[(M*(i-1)+M):(M*i + M)])
        w_i_new = wi[i]+mu*wi[i]*dt+sigma*wi[i]*Winc
        wi.append(w_i_new)
    return wi, dt


# Changing the time step sizes
#
# dt = 0.03125
b = Brownian(5, N)[1]    # Brownian increments 
M = 1                    
L = N/M
EM_approx_1 = EM(So, mu, sig, b, T, N, M)[0]
time_EM_1 = np.linspace(0.,1.,L+1)

# dt = 0.0625
b = Brownian(5, N)[1]    # Brownian increments 
M = 4                    
L = N/M
EM_approx_2 = EM(So, mu, sig, b, T, N, M)[0]
time_EM_2 = np.linspace(0.,1.,L+1)


plt.plot(time_EM_1, EM_approx_1, label = 'dt = 0.03125', ls ='--')
plt.plot(time_EM_2, EM_approx_2, label = 'dt = 0.0625', ls ='--')


plt.ylabel('AMZN Stock Price, $')
plt.title('Geometric Brownian Motion - AMZN')

plt.legend(loc = 'upper left')











