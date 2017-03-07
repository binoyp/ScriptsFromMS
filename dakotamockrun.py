"""
script to interface dakota with shipflow
with modid  
"""
import re
import os
import sys
import subprocess


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


def dumFun(parDic):
    """
    dummy function to test dakota.
    """
    out = 0
    
    for (k, v) in parDic.items():
        out += float(v)
    return out
        
    
def main():
    # open DAKOTA parameters file for reading
    paramsfile = open(sys.argv[1], 'r')
    dictParam = readParamsIn(paramsfile)
    paramsfile.close()
 
    
   
    #### Dummy function for testing ####
    res = dumFun(dictParam)
    outf = open(sys.argv[2], 'w')
    outf.write(str(res) + " f0")
    outf.close()
    #########################

    
if __name__ == '__main__':

    main()
