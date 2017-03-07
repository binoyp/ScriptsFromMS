
# -*- coding: utf-8 -*-
#############################
# Author Binoy Pilakkat     #
#                           #
# binoypilakkat@outlook.com #
#############################

import rhinoscriptsyntax as rs
import scriptcontext
import Rhino
import math
import operator
import  Rhino.DocObjects.ObjRef as _objref
from Rhino.Geometry import Point3d as _pt3d
from Rhino.Geometry import Line, Vector3d

_LPP = 38000                    #  Lpp in millimeters

def nurbcurvelist():
    """
    return nurbcurvelist in the dic {z_val:nurb cur,...}
    curves should not be hidden
    """
    obj = rs.ObjectsByType (4, select=0, state=0)
    nurbCurves = {}
    for o in obj:
       nobj = _objref(o).Curve()
       stpt = nobj.GrevillePoints()[0]
       nurbCurves[stpt.Z] = nobj
    return nurbCurves
    
def tangentVec(nurbCur):
    """
    nurbCur = single curve object
    return {0:x , 1:y, 2:z}
    Modification for aft end is to be implemented
    """
    ############################################
    # The forward tangent vector is calculated #
    ############################################
    st = nurbCur.PointAtStart
    pt2 =nurbCur.Points[1].Location
    _end = nurbCur.PointAtEnd
    d = st.DistanceTo(pt2)
    outdic={}
    if _end.X < st.X:
        tang = nurbCur.TangentAtStart
    else:
        nurbCur.Reverse()
        tang = nurbCur.TangentAtStart
    for i,ang in enumerate(tang):
        
        outdic[i] = ang
    return outdic
    
def genTanGenFile(fname, curlist):
    """
    ######################################
    # fname is the file name for saving  #         
    # curlist is a dictionary 
    # as given by nurbcurvelist
    # Generates files with tangent data  #
    # z ang1, ang2, ang3                 #
    ######################################
    """
    _file = open(fname,'w')
    _file.write('h\tx\ty\tz\n')  # header line
    
    curTans ={}
    for (z, cur) in sorted(curlist.items(), key=operator.itemgetter(0)):

        tang = tangentVec(cur)
        curTans[z]={0:tang[0],1:tang[1], 2:tang[2]}
        _file.write('{}\t{:.5f}\t{:.5f}\t{:.5f}\n'.format(z ,tang[0],tang[1],tang[2]))
    _file.close()
    
def modSurface(nurbSur, dist = 500, minZ = 50, traVec =(0,1,0), col = 2):
    """
    nurbSur should be Rhino.DocObjects.ObjRef
    minZ = minimum z value above which ctrl points are modified
    traVec = Translation direction vector
    dist = distance to be translated
    col = column number of the control pointt to be modified
    
    """
    scriptcontext.doc.Views.Redraw()
    
    _robj = nurbSur.Object()
    _robj.GripsOn = 1
    grips = _robj.GetGrips()
    _snurb = nurbSur.Surface().ToNurbsSurface()
    points = _snurb.Points
    uc =  points.CountU

    vc = points.CountV
    for g in range(grips.Length):
        curgrip = grips[g]
        getrc, curu, curv = _snurb.ClosestPoint(curgrip.CurrentLocation)
        # rs.AddPoint(curgrip.CurrentLocation)
        for j in range(vc):
            curCp = points.GetControlPoint(col,j)  # set the column to be modified here
            _dis = curCp.Location.DistanceTo(curgrip.CurrentLocation)
            if curCp.Location.Z > minZ:
                if abs(_dis) < 0.0001:
                    # rs.AddPoint(curgrip.CurrentLocation)
                    mVec = Vector3d(traVec[0],traVec[1],traVec[2])
                    mVec.Unitize()
                    mVec = mVec * dist
                    curgrip.Move(mVec)
    modsur = scriptcontext.doc.Objects.GripUpdate(_robj,0)  #  0 -> creates new surface
    scriptcontext.doc.Views.Redraw()
    return modsur

def surfaceAnal(obj,outfname = "tan"):
    """
    obj - guid of a surface 
    generates two files iso curves tangent data and
    corresponding water line tangent data
    """
    ###obj = rs.ObjectsByType (8|16, select=0, state=0)
    _snurb = _objref(obj).Surface().ToNurbsSurface()
    points = _snurb.Points
    # uc =  points.CountU
    vc = points.CountV
    wlcurs = {}                 # List for water lines
    isocurs = {}                # List for iso curvews
    for j in range(vc):
        gpt0 =  points.GetGrevillePoint(0,j) 
        pt0 = _snurb.PointAt(gpt0[0], gpt0[1]) 
        if pt0.Z > 50:
            lpt1 = pt0 + _pt3d(-1 * _LPP/2, -100, 0)
            lpt0 = pt0 + _pt3d(100, -100, 0)
            _curL = Line(lpt0, lpt1)
            lguid = scriptcontext.doc.Objects.AddLine(_curL)
            wl = rs.ProjectCurveToSurface(lguid, obj, (0,1,0))  # Draw Water Line
            rs.DeleteObject(lguid)
            if len(wl) == 1:
                wlcurs[pt0.Z] = wl[0]
                rs.DeleteObject(lguid)
                curIso = _snurb.IsoCurve(0,j)
                isocurs[pt0.Z]=curIso
                #scriptcontext.doc.Objects.AddCurve(isocurs[pt0.Z])
    wlNurbs = {}
    for id in wlcurs:
        wlNurbs[id] = _objref(wlcurs[id]).Curve()
    genTanGenFile(outfname+'-wl', wlNurbs)
    genTanGenFile(outfname+'-iso', isocurs)
    for gid in wlcurs:
        rs.DeleteObject(wlcurs[gid])
    

def main():
    """
    first generate parameters for the input surface
    """
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    if obj:
        surfguid = obj[0]
        surfobj = _objref(surfguid)
        #basenurb = surfobj.Surface().ToNurbsSurface()
      #Generate initial surface files
    surfaceAnal(surfguid, "init")
    # Modify the surface
    for n in [-4, -5]:
        modsur = modSurface(surfobj, col =1, dist = n*100, traVec=(1,0,0))
        
        if modsur:
            guidMod = modsur.Id
            surfaceAnal(guidMod, "mod"+str(n*100))
            #rs.DeleteObject(guidMod)
    # Generate Modify Surface
    
    


    

if __name__ == "__main__":
    main()
else:
    print range(-5,5)




