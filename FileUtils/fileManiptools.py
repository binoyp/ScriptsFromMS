# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 20:52:50 2015

@author: Binoy
"""

import os
 # Moving results
def batchmove(results, dest, errlog=None):
 
    # List of results that produce errors
    errors = []
 
    # Make sure dest is a directory!
    if os.path.isfile(dest):
        print("The move destination '%s' already exists as a file!" % dest)
        exit(input('Press enter to exit...'))
    elif not os.path.isdir(dest):
        try:
            os.mkdir(dest)
        except:
            print("Unable to create '%s' folder!" % dest)
            exit(input('Press enter to exit...'))
        else:
            print("'%s' folder created" % dest)
 
    # Loop through results, moving every file to dest directory
    for paths in results.values():
        for path in paths:
            path = os.path.realpath(path)
            try:
                # move file to dest
                move(path, dest)
            except:
                errors.append(path)
    print('File move complete')
 
    # log errors, if any
    if errlog and errors:
        logerr(errlog, errors, 'move')
        print("Check '%s' for errors." % errlog)
    exit(input('Press enter to exit...'))
    
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
    
    
# Deleting results -- USE WITH CAUTION!
def batchdel(results, errlog=None):
    # List of results that produce errors
    errors = []
 
    # Loop thru results, DELETING every file!
    for paths in results.values():
        for path in paths:
            path = os.path.realpath(path)
            try:
                # Delete file
                os.remove(path)
            except:
                errors.append(path)
    print('File deletion complete')
 
    # Log errors, if any
    if errlog and errors:
        logerr(errlog, errors, 'delete')
    exit(input('Press enter to exit...'))    
    
    
# The top argument for name in files
topdir = '.'
 
extens = ['txt', 'pdf', 'doc']  # the extensions to search for
 
found = {x: [] for x in extens} # lists of found files
 
# Directories to ignore
ignore = ['docs', 'doc']
 
logname = "findfiletypes.log"
 
print('Beginning search for files in %s' % os.path.realpath(topdir))
 
# Walk the tree
for dirpath, dirnames, files in os.walk(topdir):
    # Remove directories in ignore
    # directory names must match exactly!
    for idir in ignore:
        if idir in dirnames:
            dirnames.remove(idir)
 
    # Loop through the file names for the current step
    for name in files:
        # Split the name by '.' & get the last element
        ext = name.lower().rsplit('.', 1)[-1]
 
        # Save the full name if ext matches
        if ext in extens:
            found[ext].append(os.path.join(dirpath, name))
 
# The header in our logfile
loghead = 'Search log from filefind for files in {}\n\n'.format(
              os.path.realpath(topdir)
          )
# The body of our log file
logbody = ''
 
# loop thru results
for search in found:
    # Concatenate the result from the found dict
    logbody += "<< Results with the extension '%s' >>" % search
    logbody += '\n\n%s\n\n' % '\n'.join(found[search])
 
# Write results to the logfile
with open(logname, 'w') as logfile:
    logfile.write('%s\n%s' % (loghead, logbody))