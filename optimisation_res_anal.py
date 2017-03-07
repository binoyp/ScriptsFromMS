# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 23:57:51 2015

@author: Binoy
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.style.use('ggplot')
from matplotlib import pyplot as plt
def readParamsIn(_filein):
    # ----------------------------
    # Parse DAKOTA parameters file
    # ----------------------------
    # setup regular expressions for parameter/label matching
    e = '-?(?:\\d+\\.?\\d*|\\.\\d+)[eEdD](?:\\+|-)?\\d+' # exponential notation
    f = '-?\\d+\\.\\d*|-?\\.\\d+'                        # floating point
    i = '-?\\d+'                                         # integer
    value = e+'|'+f+'|'+i                                # numeric field
    tag = '\\w+(?::\\w+)*'                               # text tag field
    # regular expression for aprepro parameters format
    aprepro_regex = re.compile('^\s*\{\s*(' + tag + ')\s*=\s*(' + value +')\s*\}$')
    # regular expression for standard parameters format
    standard_regex = re.compile('^\s*(' + value +')\s+(' + tag + ')$')
    # extract the parameters from the file and store in a dictionary
    paramsdict = {}
    
    for line in _filein:
        m = aprepro_regex.match(line)
        if m:
            paramsdict[m.group(1)] = m.group(2)
        else:
            m = standard_regex.match(line)
            if m:
                paramsdict[m.group(2)] = m.group(1)
#    print sys.argv
#    print paramsdict
    return paramsdict


def modCsv(paramDic):
    ################################################
    # Generate transfer csv file for rhino to read #
    # and modify hull                              #
    ################################################
    csvFile = open(r"D:\Workshop\MasterThesisDatAnal\fornaft1\translation_template.csv", 'r')
    dat = csvFile.read()
    outdat =  dat.format(**paramDic)
    csvFile.close()
    outcsv = open(r"C:\Users\Binoy\Google Drive\Academics\General Pyscripts\Scripts-Intern\Rhino\trf.csv",'w')
    outcsv.write(outdat)
    outcsv.close()

def row2dic(row):
    cols = row.columns
    outdic = {}
    for c in cols:
        outdic[c] = float(row[c])
        print row[c]
    return outdic

if __name__ == "__main__":
    
    df = pd.read_csv(r"D:\Workshop\MasterThesisDatAnal\fornaft1\hull_ea_algorithm_out.dat", header=0,\
      quotechar='"',sep='\t')
    df.drop('interface', axis=1, inplace=True)
    df.rename(columns={'%eval_id':'id'}, inplace=True)
    df2 =df[df['obj_fn'] <= 1.0]
    df3 = df2.drop('id', axis=1)
    
    sel_row = df2[df['id'] == 634]
#    df2.plot(x='id', y='obj_fn')
    
    _id= np.array(df2['id'])
    _cw = np.array(df2['obj_fn'])
    plt.plot(_id,_cw)
    plt.title('Optimisation using Genetic algorithm')
    plt.xlabel('Iteration')
    plt.ylabel('$C_W$')
    plt.tight_layout()
#    d_par =  row2dic(sel_row)
#    modCsv(d_par)

#    plt.matshow(df3.corr(), cmap = matplotlib.cm.spectral_r)
#    cl = df3.columns.tolist()
#    plt.xticks(np.arange(len(cl)), cl)
#    plt.yticks(np.arange(len(cl)), cl)
#    plt.colorbar()
