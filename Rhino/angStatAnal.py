# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 18:46:05 2015

@author: Binoy
"""
from matplotlib import pyplot as plt
import numpy as np
import os

f1 = open('init-iso', 'r')


data = f1.read().split('\n')[1:]

f1.close()
numDat1 = np.array([[float(num) for num in v.split('\t') ] for v in data if v])

f2 = open('init-wl', 'r')


data = f2.read().split('\n')[1:]

f2.close()
numDat2 = np.array([[float(num) for num in v.split('\t') ] for v in data if v])

print numDat2