 # -*- coding: utf-8 -*-
"""
Created on Sat Oct 03 11:22:34 2015

@author: Binoy
"""
import rhinoscriptsyntax as rs

def readOffset(filename= None):
    fname = rs.OpenFileName("offset")
    #fname = r""
    _file = open(fname, 'r')


    hdr = _file.next()

    ncurves = int(_file.next())
    


    _curves = []
    
    print ncurves
    for i in range(ncurves):                     
        _Cur = []

        npt = int(_file.next())

            
        for j in range(npt):
            
            line = _file.next()
            
            lstLine = [float(v) for v in line.split()]
            #print lstLine
            _Cur.append(tuple(lstLine))
        _curves.append(_Cur)
    _file.close()
    return _curves
    
    
def DrawSpline(dat, convfact= 36145):
    #print dat

    for l in dat:
        #print(l)
        cpt = [(x*convfact,y*convfact*-1,z*convfact+1400) for (x,y,z) in l]
        #print cpt
        print rs.AddCurve( cpt, degree=3)
        
        
    

if __name__ == "__main__":
    DrawSpline(readOffset(r"D:\Workshop\MasterThesisDatAnal\XBLIMIT.plt"))
