# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 20:47:32 2015

@author: Binoy
"""

# Copying results
def batchcopy(results, dest, errlog=None):
    # List of results that produce errors
    errors = []
 
    # Make sure dest is a directory!
    if os.path.isfile(dest):
        print("The copy destination '%s' already exists as a file!" % dest)
        exit(input('Press enter to exit...'))
    elif not os.path.isdir(dest):
        try:
            os.mkdir(dest)
        except:
            print("Unable to create '%s' folder!" % dest)
            exit(input('Press enter to exit...'))
        else:
            print("'%s' folder created" % dest)
 
    # Loop thru results, copying every file to dest directory
    for paths in results.values():
        for path in paths:
            path = os.path.realpath(path)
            try:
                # copy file to dest
                copy2(path, dest)
            except:
                errors.append(path)
    print('File copying complete')
 
    # Log errors, if any
    if errlog and errors:
        logerr(errlog, errors, 'copy')
    exit(input('Press enter to exit...'))
    
    

            
# We only need to import this module
import os.path
 
# The top argument for walk. The
# Python27/Lib/site-packages folder in my case
 
topdir = r"C:\Users\binoy\Desktop\Linear_regf"
 
# The arg argument for walk, and subsequently ext for step
exten = '.config'
 
def step(ext, dirname, names):
    ext = ext.lower()
 
    for name in names:
        if name.lower().endswith(ext):
            fname = os.path.join(dirname, name)
            print(os.path.join(dirname, name))
            inplace_change(fname, 'nonl','line' )
            
            
def inplace_change(filename, old_string, new_string):
        s=open(filename).read()
        if old_string in s:
                print 'Changing "{old_string}" to "{new_string}"'.format(**locals())
                s=s.replace(old_string, new_string)
#                print s
                f=open(filename, 'w')
                f.write(s)
                f.flush()
                f.close()
        else:
                print 'No occurances of "{old_string}" found.'.format(**locals())
 
# Start the walk
os.path.walk(topdir, step, exten)
