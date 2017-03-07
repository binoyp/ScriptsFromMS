
import re
import os

def searchparam(_fyl, param):
    """


    """
    f = open(_fyl, 'r')
    # param = "grno"

    patt = re.compile(param+"=(.*?),")
    for l in f:
        match = patt.search(l)
        if match:
            f.close()

            return match.group(1)

def searchDir():

    fldr =r"D:\Workshop\Internship-Shipflow\XpanOptim"
    fls = os.listdir(fldr)
    for fl in fls:
        curpath = os.path.join(fldr,fl)
        searchparam(curpath, "file")

if __name__ == "__main__":
    searchDir()
