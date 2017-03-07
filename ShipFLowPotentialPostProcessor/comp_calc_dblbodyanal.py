# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:07:43 2015

@author: Binoy
"""


import numpy as np
import re
import os
from tabulate import tabulate
from matplotlib import pyplot as plt

def getlineparam(l):
    patt1 = re.compile(r"\s*(?P<param>\w*)\s*(?P<desc>.*)[:]{1}(?P<val>\s*[-]?\w*\.?\w*E*[+-]?\w*)")
    mat = patt1.search(l)
    if mat:
        return mat.groupdict()
    else: return  None
        

def extract_dat(f):
    """
    Extract important data from summary  file
    """
    kwd_hdr = r" *Case no *(\d) : Flow Angle = *(?P<fl_ang>\d+.?\d*)\s*"
    patt_hdr = re.compile(kwd_hdr, re.M)
    
    _file = open(f,'r')
    dic_iteration ={}
    under_iter = 0
        
    for line in _file:
#        print line
        match = patt_hdr.match(line)
        
        if match:
#            print line
            hdrdic = match.groupdict()
            curiter = 1
#            print curiter
            dic_iteration ={}
            under_iter = 1
        else:
            if under_iter:
#                print dic_iteration
                dic_par = getlineparam(line)
                if  dic_par:
                    dic_iteration[dic_par['param']] = float(dic_par['val'].strip())
            else:
                pass
            
    _file.close()
#    print dic_iteration
    nrow = len(dic_iteration)
    if nrow > 0:
        keylist = dic_iteration.keys()
        fmtlist = ['f8']*len(keylist)

        outarr = np.zeros((1), dtype = zip(keylist,fmtlist) )
        i = 0 

        for k,v in dic_iteration.items():
            outarr[k]= v
            i += 1
#        print outarr
    return outarr
 
        
def consolidate_folder(_dir):
    def visit(arg, dirname, fnames):
        for f in fnames:
            if arg in f:
                fpath = os.path.join(dirname,f)
                summarr = extract_dat(fpath)
#                print summarr
                return summarr
        
        
        
    data_dict = {}
    rootfold = os.path.basename(_dir)
    for root, dirs, files in os.walk(_dir):
        if os.path.basename(root) != rootfold:
            data_dict[int(os.path.basename(root))] = visit('SUMMARY',root,files)
    return data_dict
    
    
dat = consolidate_folder(r"D:\Workshop\MasterThesisDatAnal\BodyMesh\RunFold")
import xlsxwriter as _xl
#wb = _xl.Workbook(r"D:\Workshop\MasterThesisDatAnal\BodyMesh\mesh.xlsx")
#wsht = wb.add_worksheet()
##out =  extract_dat(r"D:\Workshop\MasterThesisDatAnal\BodyMesh\RunFold\1\config_run_SUMMARY")
##disp = [ 'IT', 'CW']
#curRow = 0 
#for k,v in dat.items():
#    wsht.write(curRow,0, k)
#    wsht.write(curRow,2, v['S'])
#    wsht.write(curRow,3, v['CXPI'])
#    curRow +=1
#w
    
    
plt.plot(x,y)
#print tabulate(list(out[disp]), headers = disp)
## print out.dtype.names
#plt.show()
