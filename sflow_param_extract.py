# -*- coding: utf-8 -*-
import re
import os
import pandas as pd

def searchparam(plist):
    patt1 = re.compile("(.*)\s*\w*[:=]{1}\s*([-]?\w*\.?\w*E*[+-]?\w*)")
    for line in plist:
        #print line
        mat = patt1.search(line)
        if mat:
            # print(line)
            # print mat.group(1),"##",mat.group(2), '\n'
            yield mat.group(1), mat.group(2)
        
    



        
def SplitOutFile(fyl):
    _file = open(fyl, 'r')
    outdic = {}
    
    
    kywrds = " - COMMANDS AND KEYWORDS FOR (XFLOW|XMESH|XGRID|XPAN|XCHAP|XBOU|XPOST)"
    patt = re.compile(kywrds +"(.*)?",re.DOTALL)

    
    _FLG = 0
    for l in _file:
        #print l
        
        match = patt.search(l)
        if match:
            kurkey = match.group(1)
            outdic[kurkey] =[]
            _FLG = 1
        else:
            if _FLG:
                outdic[kurkey].append(l.strip())
        #print outdic.keys()
    # searchparam(outdic['XMESH'])
    _file.close()
    return outdic

def getParam_sub1(dic1, k):
    content = dic1[k]
    pattHdr = re.compile('^- (\w*)$')
    outdic ={}
    _FLG = 0
    itCount = 0
    for l in content:
        mat = pattHdr.search(l)

        if mat:
            #print(l)
            #print mat.group(1)
            kurkey = mat.group(1)
            outdic[itCount] ={kurkey:[]}
            itCount += 1
            _FLG = 1
        else:
            if _FLG:
                if l:
                    outdic[itCount-1][kurkey].append(l)
    return outdic
    
    

        
        



def searchDir():
    
    fldr =r"D:\Workshop\Internship-Shipflow\XpanOptim"
    fls = os.listdir(fldr)
    for fl in fls:
        curpath = os.path.join(fldr,fl)
        searchparam(curpath, "file")

if __name__ == "__main__":
    dic1 = SplitOutFile(r"D:\Workshop\Internship-Shipflow\Reference_XPan_Run\conf_opts_OUTPUT")
    import xlsxwriter as _xl
    wb = _xl.Workbook('slfow.xlsx')
    bold = wb.add_format({'bold':True})
    for prog in dic1:
        curRow = 0
        wsht = wb.add_worksheet()
        wsht.write(curRow,0, prog,bold)
        curRow += 1
        dict2 = getParam_sub1(dic1, prog)
        for k in dict2.keys():
            # wsht.write(curRow,0, k, bold)
            # curRow += 1
            for k2 in  dict2[k].keys():
                wsht.write(curRow,0, k2, bold)
                curRow += 1
                curList = dict2[k][k2]
                for (wd, val) in searchparam(dict2[k][k2]):
                    wsht.write(curRow, 0, wd)
                    wsht.write(curRow, 1, val)
                    curRow += 1
                    print wd ,'\t', val

    wb.close()
