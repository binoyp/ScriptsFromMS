# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 09:28:30 2016

@author: Binoy
"""
import numpy as np
from scipy.optimize import minimize
from matplotlib import cm
from matplotlib import pyplot as plt

# plot functionalities
# for rosen block function
# only for 2 varibles
# Delete for more that 2 design vars and other functions

###################################################

lfile = open('rosenlog.txt','w') 

def readLogfile(_fname):
    """
    Read from logfile and return as numpy array
    """
    ar = np.genfromtxt(_fname, delimiter='\t')
    return ar

def logger(func):
     def inner(*args, **kwargs): #1
         return func(*args, _fObj=lfile) #2
     return inner

# replace the function
@logger # use this only when len(x)=2 
def rosen(x, _fObj=None):
    s = sum(10.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
    if _fObj:
        logline = "%.5f\t%.5f\t%.5f\n"%(x[0], x[1], s)
#    print logline
    _fObj.write(logline)
#    ax.plot(x[0], x[1], 'o', color = 'k')
    return s
# Optimisation configuration  
domain = 2 * 1.2     # x <= (-domain to +domain)
x0 = np.array([1.9, -1.7])
res = minimize(rosen, x0, method='nelder-mead',
               options={'xtol': 1e-8, 'disp': 1, 'maxiter':500000, 'maxfev':50000})
lfile.close()            
print(res)    # Print results..                
      

x = np.linspace(-domain, domain, 100)
y = np.linspace(-domain, domain, 100)
z = (100*np.power((y- x**2),2)) - np.power((1 - x),2)
xi, yi = np.meshgrid(x, y)
zi = (100*np.power((yi- xi**2),2)) - np.power((1 - xi),2)
fig, ax = plt.subplots()
cs = ax.contour(xi, yi, zi, cmap = plt.cm.binary)  
cs = ax.contourf(xi, yi, zi, 100, cmap=plt.cm.rainbow)        
ldata = readLogfile('rosenlog.txt')
ax.plot(ldata[:, 0], ldata[:, 1], '-+', color = 'k')   
plt.colorbar(cs)
plt.show()
