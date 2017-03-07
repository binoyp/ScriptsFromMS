 # -*- coding: utf-8 -*-
"""
Created on Sat Oct 03 11:22:34 2015

@author: Binoy
"""
import rhinoscriptsyntax as rs

def readOffset(filename= None):
    fname = rs.OpenFileName("offset")
    #fname = r"C:\Users\Binoy\Google Drive\Academics\General Pyscripts\Scripts-Intern\Rhino\xpan--200"
    _file = open(fname, 'r')


    hdr = _file.next()

    line = _file.next()             


    _curves = []
    _Cur = []
    while line:                     
        

        lstLine = [float(v) for v in line.split()]

        if int(lstLine[-1]) == 1:
            if  _Cur:            #Adding curve to curve list
                _curves.append(_Cur)
                #print _Cur
                _Cur = []
                _Cur.append(tuple(lstLine[:-1]))
        else:
            _Cur.append(tuple(lstLine[:-1]))



        line = _file.next()
        if line == "end":
            _curves.append(_Cur)
            
            _file.close()
            break

    return _curves

def DrawSpline(dat, convfact= 1000):
    
    for l in dat:
        #print(l)
        cpt = [(x*1000,y*1000,z*1000) for (x,y,z) in l]
        #print cpt
        
        rs.AddCurve( cpt, degree=3)
        
        
    

if __name__ == "__main__":
    DrawSpline(readOffset())
