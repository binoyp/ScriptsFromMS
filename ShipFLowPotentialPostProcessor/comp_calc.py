# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:07:43 2015

@author: Binoy

To parse and exctract data from summary file of ship flow

Works only for linear and non linear free surface analysis summary files
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
    kwd_hdr = r" *Case no *(\d) : Flow Angle = *(?P<fl_ang>\d+.?\d*) *Fn = * (?P<frno>\d+.?\d*)    Iteration no +(?P<it>\d+)"
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
            curiter = int(hdrdic['it'].strip())
#            print curiter
            dic_iteration[curiter] ={}
            under_iter = 1
        else:
            if under_iter:
#                print dic_iteration
                dic_par = getlineparam(line)
                if  dic_par:
                    try:
                        dic_iteration[curiter][dic_par['param']] = float(dic_par['val'].strip())
                    except:
                        dic_iteration[curiter][dic_par['param']] = 0.0
                        print "error in float conversion"
            else:
                pass
            
    _file.close()
#    print dic_iteration
    nrow = len(dic_iteration)
    if nrow > 0:
        keylist = dic_iteration[1].keys()
        fmtlist = ['f8']*len(keylist)

        outarr = np.zeros((nrow), dtype = zip(keylist,fmtlist) )
        i = 0 
        for dic in  dic_iteration.values():
            for k,v in dic.items():
                outarr[i][k]= v
            i += 1
#        print outarr
    return outarr
 
        
def consolidate_folder(_dir):
    def visit(arg, dirname, fnames):
        for f in fnames:
            if arg in f:
                fpath = os.path.join(dirname,f)
                summarr = {int(dirname):extract_dat(fpath)}
#                print summarr
                return summarr
        
        
        
    data_dict = {}
    rootfold = os.path.basename(_dir)
    for root, dirs, files in os.walk(_dir):
        if os.path.basename(root) != rootfold:
            data_dict[int(os.path.basename(root))] = visit('SUMMARY',root,files)
    return data_dict
    
    
#consoldat = consolidate_folder(r"D:\Workshop\MasterThesisDatAnal\BodyMesh\RunFold")
      

ref_dat =  extract_dat(r"D:\Workshop\MasterThesisDatAnal\CorrectedHull\corrected_hull_non_linear_fine\xpan_reference_8kn.config_RUN_DIR\xpan_reference_8kn.config_SUMMARY")
opt_dat =  extract_dat(r"D:\Workshop\MasterThesisDatAnal\opt_hulls\xpan_reference_8kn.config_RUN_DIR\xpan_reference_8kn.config_SUMMARY")