# -*- coding: utf-8 -*-
############################################
# Code Developed by Binoy Pilakkat         #
# binoypilakkat@outlook.com                #
# To process batch run output of           #
# shipflow config files                    #
# Runs should be made inside a root folder #
############################################

import os
import re
from config_param_search import searchparam

import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


def FindRunDir(rootFold):
    for fold in os.listdir(rootFold):
        if "_RUN_DIR" in fold:
            patt = re.compile( "(.*)_RUN_DIR")
            match = patt.search(fold)
            # print match.group()
            configfile = os.path.join(rootFold, fold, match.group(1))
            #
            yield (configfile, os.path.join(rootFold,fold))

def shipflow_optimfile_parser(fyl):
    _file = open(fyl)
    fdata=  _file.readlines()
    line1 = fdata[0].split()
    line2 = fdata[1].split()
    outDic ={}
    outDic['cw']= line1[0]
    outDic['Rw']= line1[1]
    outDic['Rt1']= line1[2]
    outDic['Rt2']= line1[3]
    outDic['disp']= line2[0]
    outDic['lcb']= line2[1] 
    outDic['wsa']= line2[2] 
    _file.close()
    return outDic

def ParseOptRes(_runDir):
    fyls = os.listdir(_runDir)
    for f in fyls:
        if "_OPTRES" in f:
            return shipflow_optimfile_parser(os.path.join(_runDir,f))

def getRes(RootFold):
    out = []
    for (config_file, rundir) in FindRunDir(RootFold):
        dicRes = ParseOptRes(rundir)
        _offsetfile = searchparam(config_file, "file")
        out.append((_offsetfile, dicRes))
    return out

def writeResistances():
    fldr = r"D:\Workshop\MasterThesisDatAnal\opt_hulls"
    outfile = open(os.path.join(fldr,"opt_hull_result.csv"), 'w')
    header = 1
    for f, d in getRes(fldr):
        if header:
            outfile.write("offset")
            for k in d.keys():
                outfile.write(","+k)
            header = 0
            outfile.write("\n")
        outfile.write(f)
        for k in d.keys():
            outfile.write(","+d[k])
        outfile.write("\n")
    outfile.close()


#
df1 = pd.DataFrame.from_csv(r"D:\Workshop\MasterThesisDatAnal\BP\corrected_hull_non_linear_fine\initAnalResult.csv",\
index_col=None)
#writeResistances()

df2 = pd.DataFrame.from_csv(r"D:\Workshop\MasterThesisDatAnal\opt_hulls\opt_hull_result.csv", index_col = None)

vel = np.array(df1['vel'])
cw0 = np.array(df1['cw'])
cw1 = np.array(df2['cw'])

plt.plot(vel,cw0, label='Base Hull', marker='D')
plt.plot(vel,cw1, label= 'Optimised', marker = 'o')
plt.xlabel('Velocity in Knots')
plt.title('$C_W$ comparison')
plt.legend()
plt.ylabel('$C_W$')