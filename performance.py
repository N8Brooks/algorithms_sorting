# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:20:53 2019

@author: DSU
"""

from stopwatch import stopwatch
from sorting import *
from sorting import algorithms
from tqdm import trange
from random import sample
from scipy.optimize import curve_fit
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# setting variables
TRIALS = 100    # how many trials to run per test
IMIN = 3        # minimum power of 2 to test (inclusive)
POINTS = 1000    # about how many points to put on predict curve graph
simple = ['bubbleSort', 'insertionSort']
presort = False

# arg2 - what power of 2 to test up to (excluseive)
IMAX = int(sys.argv[2])

# arg1 - which algorithms to run
if sys.argv[1] == 'all': # test all algorithms
    names = [algo.__name__ for algo in algorithms]
elif sys.argv[1] == 'simple': # test simple algorithms
    names = simple.copy()
elif sys.argv[1] == 'divide': # test divide and conquer algorithms
    names = ['mergeSort', 'quickSort', 'quickSortNaive', 'timSort']
elif sys.argv[1] == 'quickunsorted': # just quicksorts - no presort
    names = ['quickSort', 'quickSortNaive'] 
elif sys.argv[1] == 'quicksorted': # take just quick sorts - presort for demo
    names = ['quickSort', 'quickSortNaive'] 
    presort = True
else: # test specific algorithm
    names = [sys.argv[1]]

# take the specified algorithms
algorithms = [algo for algo in algorithms if algo.__name__ in names]
if not algorithms: raise Exception(f'{names} not in algorithms list')

# run experiments
clock = stopwatch()
df = pd.DataFrame()
for i in range(IMIN, IMAX):
    i = 2**i
    row = pd.Series([0]*len(names), index=names, name=i)
    
    for _ in trange(TRIALS, desc=str(i)):
        arr = sample(range(int(-2e9), int(2e9)), i)
        if presort: arr.sort()
        for name, algo in zip(names, algorithms):
            cpy = arr.copy()
            
            clock.start()
            algo(cpy)
            row[name] += clock.time()
    
    # we want the average time
    df = df.append(row.div(TRIALS))

# show table results of actual values
print(df)

# quadratic and log-linear functions for curve fitting
def quad(x, a, b, c):
    return a*x**2 + b*x + c

def log_lin(x, a, b, c):
    b = max(abs(b), 1e-10)
    return a*x * np.log(b*x) + c

step_size = math.ceil((2**IMAX - 2**IMIN) / POINTS)
predict = pd.DataFrame(index=range(2**IMIN, int(2**(IMAX-1)+1), step_size))
for name in names:
    # simple algorithms are n**2
    fit = quad if name in simple else log_lin
    
    # curve fit
    var, _ = curve_fit(fit, df.index, df[name])
    
    # predict points
    y = [fit(x, *var) for x in range(2**IMIN, int(2**(IMAX-1)+1), step_size)]
    
    # add to dataframe
    predict[(name, 'predict')] = y

# show actual values and predicted values with plot
pd.concat([df, predict], sort=False).plot()
plt.show()
