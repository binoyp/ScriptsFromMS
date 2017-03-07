# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 16:05:39 2015

@author: Binoy
"""

from xlwings import Workbook, Sheet, Range

wb = Workbook(r"C:\Users\Binoy\Google Drive\Academics\General Pyscripts\Scripts-Intern\slfow.xlsx")

rg = Range('Sheet3','A1').table

s =""
for v in rg.value:
    
    vs = str(v).strip()
    if len(vs)> 4:
        s += vs +","+ vs[:4]+","
    else:
        s += vs+","
print s