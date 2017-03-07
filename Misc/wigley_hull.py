# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 10:02:08 2015

@author: Binoy
"""
import sys

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
app = QtGui.QApplication(sys.argv)
## make a widget for displaying 3D objects
view = gl.GLViewWidget()
view.show()

## create three grids, add each to the view
xgrid = gl.GLGridItem()
ygrid = gl.GLGridItem()
zgrid = gl.GLGridItem()
#view.addItem(xgrid)
#view.addItem(ygrid)
#view.addItem(zgrid)

import numpy as np
L = 5
B = 0.91
D = 0.9

x = np.linspace(-L, L, 100)
#y = np.linspace(-0.1, 0.1, 100)
color  =   (0.0, 1.0, 0.0, 0.5)
size = [0.00500] * len(x)
for z in np.linspace(0,-D,20):
    y = (0.5*B)*(1 - ((2*x)/L)**2)*(1-(z/D)**2)
    y2 = -1 *y
    zz = np.ones_like(y)*z
    print y
    pos = np.transpose(np.vstack((x,y,zz)))
    pos2 = np.transpose(np.vstack((x,y2,zz)))
#    sp1 = gl.GLScatterPlotItem(pos=pos, size=size , color=color, pxMode=False)
    l1 = gl.GLLinePlotItem(pos=pos, width=0.01 , color=color, mode='line_strip')
    view.addItem(l1)
    l2 = gl.GLLinePlotItem(pos=pos2, width=0.01 , color=color, mode='line_strip')
    view.addItem(l2)

app.exec_()