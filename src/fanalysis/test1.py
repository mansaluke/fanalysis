"""
brownian() implements one dimensional Brownian motion (i.e. the Wiener process).
"""

from math import sqrt
from scipy.stats import norm
import numpy as np
from pylab import plot, show, grid, xlabel, ylabel


def brownian(delta: "The Wiener process parameter" = 2):
    # The Wiener process parameter.
    delta = 2
    # Total time.
    T = 10.0
    # Number of steps.
    N = 500
    # Time step size
    dt = T/N
    # Number of realizations to generate.
    m = 1

    x = np.empty((m,N+1))
    print(x)
    x[:, 0] = 100

    r = norm.rvs(size=x[:,0].shape + (N,), scale=delta*sqrt(dt))

    np.cumsum(r, axis=-1, out=x[:,1:])

    x[:,1:] += np.expand_dims(x[:,0], axis=-1)

    out= x[:,1:]
    return out

b = brownian()
delta = 2
# Total time.
T = 10.0
# Number of steps.
N = 500
# Time step size
dt = T/N
# Number of realiza
m = 1
t = np.linspace(0.0, N*dt, N+1)
print(b[0])
#for k in range(m):
plot(t, b[0])
#
#show()

