<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="bin.20150917102554.2"><vh>ShipFlowXPAN</vh></v>
<v t="bin.20150917102633.1" a="E"><vh>@clean xpanFS.py</vh>
<v t="bin.20150917102722.1"><vh>xpanFS declarations</vh></v>
<v t="bin.20150917102722.2" a="E"><vh>class FreeSurface</vh>
<v t="bin.20150917102751.1"><vh>&lt;&lt;doc&gt;&gt;</vh></v>
<v t="bin.20150917102722.3"><vh>__init__</vh></v>
<v t="bin.20150917102722.4"><vh>addProp</vh></v>
</v>
<v t="bin.20150917102722.5"><vh>plt3D</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="bin.20150917102554.2"></t>
<t tx="bin.20150917102633.1">@language python
@tabwidth -4
@others

if __name__ == '__main__':
    path = "FSRES"
    _file = open(path)

    head = [next(_file) for x in xrange(16)]

    nPanel = int(next(_file).split()[0])
    fs = FreeSurface(nPanel)
    misc = [next(_file) for x in xrange(3)]
    keylist1 = ('x', 'y', 'z', 'vt', 'cp')
    for pNo in xrange(nPanel):
        curlin =[float(v) for v in _file.next().split()]
        indx = 0
        for v in curlin[1:]:
            fs.addProp(pNo,keylist1[indx],v)
            indx += 1

    print _file.next()
    keylist2 = ('vx', 'vy', 'vz', 'sig', 'wh')
    for pNo in xrange(nPanel):
        curlin =[float(v) for v in _file.next().split()]
        indx = 0
        for v in curlin[1:]:
            fs.addProp(pNo,keylist2[indx],v)
            indx += 1
    print _file.next()
    keylist3 = ('nx', 'ny', 'nz', 'area')
    for pNo in xrange(nPanel):
        curlin =[float(v) for v in _file.next().split()]
        indx = 0
        for v in curlin[1:-1]:
            fs.addProp(pNo,keylist3[indx],v)
            indx += 1
#    filt = np.logical_and(  , [fs.Panels['y']&gt;-0.8])
    plt3D(fs.Panels[fs.Panels['nx']&gt;0])
</t>
<t tx="bin.20150917102722.1"># -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 16:17:07 2015

@author: Binoy

"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

</t>
<t tx="bin.20150917102722.2">class FreeSurface:
    &lt;&lt;doc&gt;&gt;
    @others
</t>
<t tx="bin.20150917102722.3">def __init__(self, fname, Iterations = 0, Fn = None):
    
    try:
        _file = open(fname, 'r')
    except:
        print("No File Found")
        return None 
    
    head = [next(_file) for x in xrange(16)] #skipping initial 16 lines
    
    nPanel = int(next(_file).split()[0])
    self.Panels = np.zeros((nPanel), dtype=[('no', 'i4'),('x', 'f8'), ('y', 'f8'), \
    ('z', 'f8'), ('vt', 'f8'), ('cp', 'f8'), ('sig', 'f8'), ('wh', 'f8'), \
    ('nx', 'f8'), ('ny', 'f8'), ('nz', 'f8'), ('area', 'f8'), ('vx', 'f8'),\
    ('vy', 'f8'), ('vz', 'f8')])
    
    
    for pno in range(nPanel):  # Initializing panel numbers
        self.Panels[pno]['no'] = pno + 1
    
\\-4.#        fs = FreeSurface(nPanel)
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

    


</t>
<t tx="bin.20150917102722.4">def addProp(self, Pno, _key, _val):
\\-4.#        _propDic =  {'NPX':1,'NPY          NPZ           VT           CP
\\-4.#        print 'adding property to no', _key,Pno
\\-4.#        print self.Panels['no'][self.Panels['no']==Pno]
    self.Panels[Pno][_key] = _val
</t>
<t tx="bin.20150917102722.5">#        print self.Panels[self.Panels['no'] == Pno+1]


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





</t>
<t tx="bin.20150917102751.1">"""
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
</t>
</tnodes>
</leo_file>
