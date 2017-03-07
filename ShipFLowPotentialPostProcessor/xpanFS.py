# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 16:17:07 2015

@author: Binoy

"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class FreeSurface:
    """
    Reads the Ship flow xpan output file for free surface.
     x      : x-coordinate of panel center
     y      : y-coordinate of panel center
     z      : z-coordinate of panel center
     VT  : Total velocity
     CP  : Dynamic pressure coefficient
     VX  : x-component of velocity vector
     VY  : y-component of velocity vector
     VZ  : z-component of velocity vector
     SIG : Source strength
     WH  : Wave height at panel center
     NX  : x-component of panel normal vector
     NY  : y-component of panel normal vector
     NZ  : z-component of panel normal vector
     AREA: Panel area
    Structured numpy array is created out of the files

    """
    def __init__(self, fname, Iterations = 0, Fn = None):
        
        try:
            _file = open(fname, 'r')
        except:
            print("No File Found")
            return None 
        
        head = [next(_file) for x in xrange(16)] #skipping initial 16 lines
        
        nPanel = int(next(_file).split()[0])
        self.N = nPanel
        self.Panels = np.zeros((nPanel), dtype=[('no', 'i4'),('x', 'f8'), ('y', 'f8'), \
        ('z', 'f8'), ('vt', 'f8'), ('cp', 'f8'), ('sig', 'f8'), ('wh', 'f8'), \
        ('nx', 'f8'), ('ny', 'f8'), ('nz', 'f8'), ('area', 'f8'), ('vx', 'f8'),\
        ('vy', 'f8'), ('vz', 'f8')])
        
        
        for pno in range(nPanel):  # Initializing panel numbers
            self.Panels[pno]['no'] = pno + 1
        
#        fs = FreeSurface(nPanel)
        misc = [next(_file) for x in xrange(3)] #skipping
        keylist1 = ('x', 'y', 'z', 'vt', 'cp')
        
        for pNo in xrange(nPanel):
            curlin =[float(v) for v in _file.next().split()]
            indx = 0
            for v in curlin[1:]:
                self.addProp(pNo,keylist1[indx],v)
                indx += 1

        print _file.next()
        keylist2 = ('vx', 'vy', 'vz', 'sig', 'wh')
        for pNo in xrange(nPanel):
            curlin =[float(v) for v in _file.next().split()]
            indx = 0
            for v in curlin[1:]:
                self.addProp(pNo,keylist2[indx],v)
                indx += 1
        print _file.next()
        keylist3 = ('nx', 'ny', 'nz', 'area')
        for pNo in xrange(nPanel):
            curlin =[float(v) for v in _file.next().split()]
            indx = 0
            for v in curlin[1:-1]:
                self.addProp(pNo,keylist3[indx],v)
                indx += 1

        _file.close()

        
    def addProp(self, Pno, _key, _val):
#        _propDic =  {'NPX':1,'NPY          NPZ           VT           CP
#        print 'adding property to no', _key,Pno
#        print self.Panels['no'][self.Panels['no']==Pno]
        self.Panels[Pno][_key] = _val
#        print self.Panels[self.Panels['no'] == Pno+1]


def plt3D(_panel,filt= None):
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    if not filt:
        x = _panel['x']
        y = _panel['y']
        z = _panel['z']
    else:
        x = _panel['x'][filt]
        y = _panel['y'][filt]
        z = _panel['z'][filt]
#    X,Y = np.meshgrid(x, y)
#    Z = np.meshgrid(z,z)
#    ax.plot_surface(X, Y, Z)
    ax.scatter(_panel['x'], _panel['y'], _panel['z'], c = 'b', marker = '.')
    ax.set_zlim(bottom=-0.5)
    ax.quiver(_panel['x'], _panel['y'], _panel['z'],_panel['nx'], _panel['ny'], _panel['nz'],length=0.01)
    plt.show()






if __name__ == '__main__':
    path = "FSRES"
    
    fs = FreeSurface(path)
    ## build a QApplication before building other widgets

    
    
