"""
script to interface dakota with shipflow
with modid  
"""
import re
import os
import sys
import subprocess
import shutil, errno

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
    return paramsdict


def modCsv(paramDic):
    ################################################
    # Generate transfer csv file for rhino to read #
    # and modify hull                              #
    ################################################
    csvFile = open('translation_template.csv', 'r')
    dat = csvFile.read()
    outdat =  dat.format(**paramDic)
    csvFile.close()
    outcsv = open('trf.csv','w')
    outcsv.write(outdat)
    outcsv.close()
    

def shellExec(cmd):
    ###########################
    # Execute shell command   #
    # prints output to stdout #
    ###########################
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

def writeDatacsv(inpdic):
    #######################################################
    # Just to store values from optres of  each iteration #
    #######################################################
    f
    _file = open('Optimtrack.csv','a')
    for (k,v) in inpdic.items():
        _file.write(str(k)+","+str(v)+",")
        #_file.write('\n')
    _file.write('\n')
    _file.close()
    
def shipflow_optimfile_parser(fyl):
    #################################
    # Read the optres file          #
    # return values in a dictionary #
    #################################
    try:
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
    except:
        return None
    return outDic

def copyDir(src, dst):
    #####################
    # Copoy recursively #
    #####################
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


def main():
    # open DAKOTA parameters file for reading
    paramsfile = open(sys.argv[1], 'r')
    dictParam = readParamsIn(paramsfile)
    paramsfile.close()
    modCsv(dictParam)

    #############################
    # Rhino Hull Modification   #
    # And New Offset Generation #
    #############################
  
    bSurface = shellExec("SurfaceModifier.exe")
    if bSurface:
        print "Surface Modification Failed"    
    else:
        print 30 * "*"
        print 30 * "*"
        print "Surface modified Successfully using Rhino"
        print 30 * "*"
        print 30 * "*"
    #####################
    # ShipFlow Analysis #
    #####################
    outf = open(sys.argv[2], 'w')
    try:
        flgFyl = open('_flgMsur', 'r')
        # res is created by Rhino
        # res is 1 if offset file generation is succesful
        res = int(flgFyl.read())
        
    except:
        res = 0
    if res: 
        bShipflow = shellExec(r"C:\FLOWTECH\SHIPFLOW6.0.03-x86_64\bin\shipflow.bat -c conf_opts")
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
        
        # Optifyl path to optres file
        optifyl = r"C:\binSys\Optimisation\OptimFinale\conf_opts_RUN_DIR\conf_opts_OPTRES"

        try:
            # sfres is a dictionary with optres values
            sfres = shipflow_optimfile_parser(optifyl)
            writeDatacsv(sfres)
        except:
            print "ERROR IN SFLOW CALCULATION"
            outf.write( "FAIL")
            



          ######################################################################
          # _DEST is the location of folder where the output files of each     #
          # iteration are copied                                               #
          #  insdie _DEST creat  a file "count.txt" , write 0 in the file      #
          # count.txt tracks number of iterations                            # #
          # RunFold copies the output of each iteration for future reference # #
          ######################################################################
         
        _DEST = r"C:\binSys\Optimisation\OptimFinale\RunFold"
        _countFile = open(r"C:\binSys\Optimisation\OptimFinale\RunFold\count.txt", 'r')
        
        _Count = int(_countFile.read())
        _countFile.close()
        _DESTFOLD = os.path.join(_DEST,str(_Count))
        # copying outputs to runfold
        copyDir(r"C:\binSys\Optimisation\OptimFinale\conf_opts_RUN_DIR",_DESTFOLD)
        _countFile = open(r"C:\binSys\Optimisation\OptimFinale\RunFold\count.txt", 'w')
        _countFile.write(str(_Count+1))
        _countFile.close()
        # To avoid shipflow file read error, each output is deleted
        try:
            shutil.rmtree(r"C:\binSys\Optimisation\OptimFinale\conf_opts_RUN_DIR")
            os.remove("conf_opts.cgns")
        except:
            print("DIRECTORY DELETE FAILED")
        

        if sfres:
            outf.write(str(sfres['cw']) + " f0")
        else:
            outf.write( "FAIL")
            
    else:

        print "ERROR IN SFLOW CALCULATION"
        outf.write( "FAIL")
    outf.close()
    
    #### Dummy function for testing ####
    # res = dumFun(dictParam)
    # outf = open(sys.argv[2], 'w')
    # outf.write(str(res) + " f0")
    # outf.close()
    #########################
    
if __name__ == '__main__':

    main()
