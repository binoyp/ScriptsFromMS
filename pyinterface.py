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


def modCsv(paramDic):
    csvFile = open('tempTRF.csv', 'r')
    dat = csvFile.read()
    outdat =  dat.format(**paramDic)
    csvFile.close()
    outcsv = open('trf.csv','w')
    outcsv.write(outdat)
    outcsv.close()
    

def shellExec(cmd):
    print "Executing:"
    print 30 * "="
    print cmd
    print 30 * "="
    
    pr = subprocess.Popen(cmd,shell= 1, stdout = subprocess.PIPE)
    #for line in pr.stdout:
    while True:
        line =  pr.stdout.readline()
        sys.stdout.write(line)
        if not line: break
    pr.wait()
    return pr.returncode
def dumFun(parDic):
    """
    dummy function to test dakota.
    """
    out = 0
    
    for (k, v) in parDic.items():
        out += float(v)
    return out
        
    
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
def main():
    # open DAKOTA parameters file for reading
    paramsfile = open(sys.argv[1], 'r')
    dictParam = readParamsIn(paramsfile)
    paramsfile.close()
    modCsv(dictParam)
    
    bSurface = shellExec("SurfaceModifier.exe")
    if bSurface:
        print "Surface Modification Failed"    
    else:
        print 30 * "*"
        print 30 * "*"
        print "Surface modified Successfully using Rhino"
        print 30 * "*"
        print 30 * "*"
        
    
    bShipflow = shellExec(r"C:\FLOWTECH\SHIPFLOW6.0.03-x86_64\bin\shipflow.bat -c c4opti")
    
    if bShipflow:
        print 30 * "-"
        print "Shipflow calculation failed, it seems"
        print 30 * "-"
    else:
        print 30 * "*"
        print 30 * "*"
        print("Shipflow calculation successful")
        print 30 * "*"
        print 30 * "*"
        
        
    optifyl = r"D:\Workshop\Dakota\script\c4opti_RUN_DIR\c4opti_OPTRES"
    sfres = shipflow_optimfile_parser(optifyl)
    outf = open(sys.argv[2], 'w')
    outf.write(str(sfres['Rt1']) + " f0")
    outf.close()
    
    #### Dummy function for testing ####
    #res = dumFun(dictParam)
    #outf = open(sys.argv[2], 'w')
    #outf.write(str(res) + " f0")
    #outf.close()
    #########################

    
if __name__ == '__main__':

    main()
