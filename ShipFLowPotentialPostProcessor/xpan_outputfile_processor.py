# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:07:43 2015

@author: Binoy

To parse and exctract data from summary file of ship flow

Works only for linear and non linear free surface analysis summary files

XBOUND Results should not be present
"""


import numpy as np
import pandas as pd
import re
import os
from tabulate import tabulate
from matplotlib import pyplot as plt
from scipy.interpolate import spline
import matplotlib
matplotlib.style.use('ggplot')

def getlineparam(l):
    rekwd = r"\s*(- )?(?P<param>\w*)\s*(?P<desc>[\s\W\w]*?)\s(?P<op1>=|:){1}\s*(?P<val>[-]?[\d]+\.?\d*E*[+-]?[\d]*)\s*(?P<misc>[\w\s]*)(?P<op2>:)?(?(op2).*)"
    patt1 = re.compile(rekwd)
    mat = patt1.search(l)
    if mat:
        return mat.groupdict()
    else: return  None
        

def iteration_summary(f, stopkwd):
    """
    Extract important data from summary  file
    return pandas data frame
    """
    kwd_hdr = r" *Case no *(\d) : Flow Angle = *(?P<fl_ang>\d+.?\d*) *Fn = * (?P<frno>\d+.?\d*)    Iteration no +(?P<it>\d+)"
    patt_hdr = re.compile(kwd_hdr, re.M)
    patt_stop = re.compile(stopkwd, re.M)
    _file = f
    dic_iteration ={}
    under_iter = 0
        
    for line in _file:
        match = patt_hdr.match(line)
        mat_stop = patt_stop.match(stopkwd)
        if mat_stop:
            return dic_iteration
        
        if match:
            hdrdic = match.groupdict()
            curiter = int(hdrdic['it'].strip())
            dic_iteration[curiter] ={}
            under_iter = 1
        else:
            if under_iter:
                dic_par = getlineparam(line)
                if  dic_par:
                    if dic_par['op1']==':':
                        dic_iteration[curiter][dic_par['param']] = float(dic_par['val'].strip())
                    if dic_par['op2']:
                        dic_iteration[curiter][dic_par['param']+dic_par['desc']] = float(dic_par['val'].strip())
                    if dic_par['op1']=='=':
                        dic_iteration[curiter][dic_par['param']+dic_par['desc']] = float(dic_par['val'].strip())
            else:
                pass
            
    return pd.DataFrame.from_dict(dic_iteration, orient = 'index')
 
        
def consolidate_folder(_dir):
    def visit(arg, dirname, fnames):
        for f in fnames:
            if arg in f:
                fpath = os.path.join(dirname,f)
                summarr = {int(dirname):extract_dat(fpath)}
                return summarr
        
        
        
    data_dict = {}
    rootfold = os.path.basename(_dir)
    for root, dirs, files in os.walk(_dir):
        if os.path.basename(root) != rootfold:
            data_dict[int(os.path.basename(root))] = visit('SUMMARY',root,files)
    return data_dict
   
def outputfile_process(fname):
    _file = open(fname, 'r')
    outdic = {}
    
    
    kywrds = " - COMMANDS AND KEYWORDS FOR (?P<prog>XFLOW|XMESH|XGRID|XPAN|XCHAP|XBOU|XPOST)"
    patt = re.compile(kywrds +"(.*)?",re.DOTALL)
    
    line = _file.next()
    while line:
        mach =  re.match(patt,line)
        if mach:
            if mach.groupdict()['prog'] == 'XMESH':
                pass
            if mach.groupdict()['prog'] == 'XPAN':

                it_dat = iteration_summary(_file, kywrds)
        try:
            line = _file.next()
        except StopIteration:
            break
    return it_dat
          
def LWCUT_parser(path):
    f = open(path,'r')
    df = pd.DataFrame()
    loc = f.readline()
    col = 0
    while loc:
        count = int(f.readline())
        colxi = 'x_loc='+str(float(loc.strip()))  
        colyi = 'y_loc='+str(float(loc.strip()) )
        df[colxi]= [0]*count
        df[colyi]= [0]*count
        for i in range(count):
            curl = [float(v) for v in f.readline().split()]
            df.ix[i,colxi] = curl[0]
            df.ix[i,colyi] = curl[1]



        loc = f.readline()
        col += 2
    f.close()
    return df

def getData(fold, k):
    _d ={'OUT':['_OUTPUT',outputfile_process],\
    'lwave':['_LWAVECUT',LWCUT_parser],'twave':['_TWAVECUT',LWCUT_parser]}
    configname = os.path.basename(fold)[:-8]
    return _d[k][1](os.path.join(fold,configname+_d[k][0]))
    
def procOutdf(df):
    """
    
    """
    pass

def outfile_plot(df):
    fig, ax = plt.subplots()
    col = {k:v for (k,v) in enumerate(df.columns)}
    x = df[col[13]]
    ax2 = ax.twinx()
    ax.plot(x, df[col[31]], label = col[31],marker='o')
    ax2.plot(x, df[col[28]], label= col[28], color='blue', marker='^')
    ax.plot(x, df[col[29]], label = col[29], marker='d')
    ax.legend()
    ax2.legend(loc=2)
    ax2.set_ylabel('sinkage convergence')
    ax.set_ylabel('trim/wave convergence')
    ax.set_xlabel('Iteration number')
    for tl in ax2.get_yticklabels():
        tl.set_color('blue')
    ax2.yaxis.get_major_formatter().set_powerlimits((0, 1))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
    plt.tight_layout()
    plt.grid(1)
    
def tab_output(df,fmt = 'grid'):
    """
    print resistance analysis in tabular format
    fmt = tabular format parameter
    """
    col = {k:v for (k,v) in enumerate(df.columns)}
    finit = max(df['IT'])
    lpp = 36.145
    sref= df[df['IT']==finit]['Sref']* lpp**2
    s = df[df['IT']==finit][col[15]] * lpp**2
    rho = 1000
    cb = df[df['IT']==finit]['CB']
    print cb
    vol = df[df['IT'] == finit]['V']* lpp**3
    t = df[df['IT']==finit][u'T']*lpp
    print t
    b = df[df['IT']==finit]['B']*lpp
    rn = 1.48164E+08
    cw =  df[df['IT']==finit][u'CW']
    rw =  cw * rho * 0.5* (4.115557273)**2*sref
    bd = b/t
    wh = df[df['IT']==finit][col[25]]*lpp
    k=0
#    k = 0.11 + (0.128*bd)-(0.0157*bd**2)-(3.1*(cb/(lpp/b)))+(28.8*(cb/(lpp/b))**2)
    k = -0.095 + (25.6*cb)/((lpp/b)**2*np.sqrt(b/t)) # Watanabe
    cf = 0.075/(np.log10(rn)-2)**2
    rf = cf*(1+k) * rho * 0.5* (4.115557273)**2*sref
    prntList = [['Volume Displacement',  vol], 
                ['Wetted Surface Area', sref],\
                ['$C_W$', cw],\
                ['Wave making Resistance', rw],\
                ['$C_F$ by ITTC formula', cf],\
                ['Form factor $k$', k],\
                ['Total Resistance', rf+rw]]
    print tabulate(prntList,tablefmt=fmt)
    
if __name__ == "__main__":
    
    print "Optimised Result"
    
    foldopt = r"D:\Workshop\MasterThesisDatAnal\CorrectedHull\Linear_regf\xpan_reference_8kn.config_RUN_DIR"
    out_o =  getData(foldopt, 'OUT')
    foldr = r"D:\Workshop\MasterThesisDatAnal\BP\corrected_hull_non_linear_fine\xpan_reference_8kn.config_RUN_DIR"
    #outfile_plot(out)
    tab_output(out_o,  fmt='latex_booktabs')
    
#    print "Reference Values"
#    out_r = getData(foldr,'lwave')
#    tab_output(out_r, fmt='latex_booktabs')

#
#     Plot for wave cuts
#    fig, ax = plt.subplots(nrows =3, ncols =1, sharex ='all' )
#    col = out_o.columns
#    for i in [1,0,2]:
#        x = out_o[col[2*i]]*36.145
#        y = out_o[col[2*i+1]]*36.145
#        y2 = out_r[col[2*i+1]]*36.145
#        xnew = np.linspace(x.min(),x.max(),300)
#        xnew2 = np.linspace(x.min(),x.max(),300)
#        #
#        ynew= spline(x,y,xnew)
#        yn2 = spline(x,y2,xnew2)
#        ax[i].plot(xnew,ynew,label='Linear')
#        ax[i].plot(xnew2,yn2,label='Non Linear')
#        ax[i].set_title(r'$\frac{y}{L_{PP}}=$'+col[2*i][-3:])
##        ax[i].plot(x,y,'o')
#        ymin, ymax = ax[i].get_ylim()
#        ax[i].vlines(0,ymin,ymax)
#        ax[i].text(0,ymin,r'$BOW$',ha='right')
#        ax[i].vlines(36.145,ymin,ymax)
#        ax[i].text(36.145,ymin,r'$STERN$',ha='right')
#        ax[i].legend()
#    plt.tight_layout()
#    plt.xlabel('x (m)')
#    
#        