# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 12:20:11 2015

@author: Binoy
"""

from loadparam import ktparam,kqparam
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
param_kt = ktparam()
param_kq = kqparam()


def kt(j,pd,aea0,z):
    """
    Calculate kt = Thrust coefficient
    j = advance velocity
    pd = pitch ratio
    aea0 = BAR
    z = Number of blades
    """
    term_array = np.zeros(39,dtype=np.float64)
    for i in range(39):
        c = param_kt['c'][i]
        t = param_kt['t'][i]
        u = param_kt['u'][i]
        v = param_kt['v'][i]
        s = param_kt['s'][i]
        base = np.array([c,j,pd,aea0,z])
        exp =  np.array([1,s,t,u,v])
        term_array[i] = np.prod(np.power(base,exp))
    return np.sum(term_array)
    
    
def kq(j,pd,aea0,z):
    """
    Calculate kq = Torque coefficient 
    j = advance velocity
    pd = pitch ratio
    aea0 = BAR
    z = Number of blades
    """
    term_array = np.zeros(47,dtype = np.float64)
    for i in range(47):
        c = param_kq['c'][i]
        t = param_kq['t'][i]
        u = param_kq['u'][i]
        v = param_kq['v'][i]
        s = param_kq['s'][i]
#            print c
        base = np.array([c,j,pd,aea0,z])
        exp =  np.array([1,s,t,u,v])
        term_array[i] = np.prod(np.power(base,exp))
    return np.sum(term_array)

def ktpds(j, pds,aea0,z):
    """
    Calculate kt = Thrust coefficient  for different pitch ratios
    j = advance velocity as array
    pd = pitch ratio as array
    aea0 = BAR
    z = Number of blades 
    returns
    kt for pd / j
    +------+-------------+-------------+------------+-------------+
    | j/pd |         0.6 |         0.8 |        1.0 |         1.2 |
    +======+=============+=============+============+=============+
    """
    nj = len(j)
    
    outArr = np.zeros((nj), dtype =[('j','f8')]+ [ (str(pd), 'f8') for pd in pds])

    for row in range(nj):
        outArr[row] =  np.array([j[row]]+[ kt(j[row], pd, aea0,z) for pd in pds])

    return outArr

def kqpds(j, pds,aea0,z):
    """
    Calculate kq = Torque coefficient  for different pitch ratios
    j = advance velocity as array
    pd = pitch ratio as array
    aea0 = BAR
    z = Number of blades    
    
    Return numpy structured array
    kq for pd / j
    +------+-------------+-------------+------------+-------------+
    | j/pd |         0.6 |         0.8 |        1.0 |         1.2 |
    +======+=============+=============+============+=============+
    """    
    nj = len(j)
    
    outArr = np.zeros((nj), dtype =  [('j','f8')] +[(str(pd), 'f8') for pd in pds])
    
    for row in range(nj):
        outArr[row] =  np.array([j[row]]+[ kq(j[row], pd, aea0,z) for pd in pds])

    return outArr

def pltTab(ax, tab):
    """
    ax = Matplotlib axis
    tab = numpy structure array
    
    
    """
    nms = tab.dtype.names
    
    for  n in nms:
        if n != 'j':
            ax.plot(tab['j'], tab[n])
    ax.set_ylim(0,1)
 

def getIntersect(x1,y1, x2, y2, deg1,deg2):
    """
    Find roots of two curves
    x1, y1 -> arrays first polynomial
    x2, y2 -> arrays second polynomial
    deg1 -> degree of x1, y1
    deg2 -> degree of x2, y2
    return intersection
    """
    fit1 = np.polyfit(x1,y1,deg1)
    fit2  = np.polyfit(x2, y2, deg2)
    eqn = np.polysub(fit1,fit2)
    roots = np.roots(eqn)
    return roots
    
def plotInter(ax, x, y):
    """
    Draw ordinates (x, y)
    ax - maplotlib axes object
    """
    ax.hlines(y, 0, x, linestyle ='-.')
    ax.vlines(x, 0, y, linestyle ='-.')
    
def onlyreal(arr):
    return arr[arr.imag == 0].real

def print_structarray(arr):
    hdr =list(arr.dtype.names)
    print tabulate(list(arr), headers = hdr, tablefmt = 'grid')


def customktkq(p, **kwargs):
    jx = np.arange(0.01,1.5,.05) 
    y = np.polyval(p, jx)
    plt.plot( jx, y)
    plt.ylim(0,1)
    if 'vals' in kwargs:
        outl = []
        for v in kwargs['vals']:
            outl.append([v, np.polyval(p,v)])
        print tabulate(outl)
    if 'yval' in kwargs:
        ps = np.polysub(p, kwargs['yval'])
        r =  filter(lambda x: (x>0.01) and (x<1.5),np.roots(ps))
        print r
        plt.plot(r[0], kwargs['yval'],'o')
        if 'p2' in kwargs:
            p2 = kwargs['p2']
            print p2
            plt.plot(jx, np.polyval(p2,jx))
            print 'value of p2 for the %f is '%r[0], np.polyval(p2, r[0])
            plt.plot(r[0], np.polyval(p2, r[0]),'o')
    
if __name__ == '__main__':
    customktkq([0.169,-.527, 0.319],vals=[.2],yval=0.22036, p2 = 0.1*np.array([0.203,-0.578,0.354]))
#    print onlyreal(a)