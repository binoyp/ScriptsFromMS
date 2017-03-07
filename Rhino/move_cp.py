
# -*- coding: utf-8 -*-
#############################
# Author Binoy Pilakkat     #
#                           #
# binoypilakkat@outlook.com #
#############################

import rhinoscriptsyntax as rs
from scriptcontext import doc
import Rhino
import operator
import  Rhino.DocObjects.ObjRef as _objref
from Rhino.Geometry import Point3d as _pt3d
from Rhino.Geometry import Line, Vector3d, Point3d, Plane
from Rhino.Geometry.Intersect.Intersection import BrepPlane as _IntPlaneSurf



                

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
    
def modSurface(nurbSur,  _LPP = 36.145, lstTup=()):
    """
    nurbSur should be Rhino.DocObjects.ObjRef
    minZ = minimum z value above which ctrl points are modified
    traVec = Translation direction vector
    dist = distance to be translated
    col = column number of the control pointt to be modified
    
    """
    doc.Views.Redraw()
    
    _robj = nurbSur.Object()
    _robj.GripsOn = 1
    grips = _robj.GetGrips()
    _snurb = nurbSur.Surface().ToNurbsSurface()
    points = _snurb.Points
    print "Modify"

    #vc = points.CountV
    for g in range(grips.Length):
        curgrip = grips[g]
        
        getrc, curu, curv = _snurb.ClosestPoint(curgrip.CurrentLocation)
        print getrc
        # rs.AddPoint(curgrip.CurrentLocation)
        for (_u, _v, _vectTup) in lstTup:
            
            
            curCp = points.GetControlPoint(_u, _v)  # set the column to be modified here
            _dis = curCp.Location.DistanceTo(curgrip.CurrentLocation)
            # if curCp.Location.Z > minZ:
            if abs(_dis) < 0.0001:
                # rs.AddPoint(curgrip.CurrentLocation)
                
                mVec = Vector3d(_vectTup[0],_vectTup[1],_vectTup[2])
#                mVec.Unitize()
#                mVec = mVec * dist
                curgrip.Move(mVec)
            
    modsur = doc.Objects.GripUpdate(_robj,1)  #  0 -> creates new surface
    
    
    _robj.GripsOn = 0
    doc.Views.Redraw()

def surfaceAnal(obj,_LPP, outfname = "tan"):
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
            lguid = doc.Objects.AddLine(_curL)
            wl = rs.ProjectCurveToSurface(lguid, obj, (0,1,0))
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

def readCsv(_fname):
    _fyl = open(_fname, 'r')
    lstTup =[]
    for l in _fyl:
        
        [u, v, x, y, z, d] = map(float,l.strip().split(','))
        lstTup.append((u,v,(x, y, z), d))
    _fyl.close()
    return lstTup
            
            
    


def movecp():
    """
    function to be used with dacota 
    """
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    if obj:
        surfguid = obj[0]
        surfobj = _objref(surfguid)
        #basenurb = surfobj.Surface().ToNurbsSurface()
        #Generate initial surface files
        #surfaceAnal(surfguid, outfname="init", _LPP= 36000 )
        # Modify the surface
        xt = 1000
        yt = 800
        zt = 100
        lstTup = [(8,i,(xt,yt,zt)) for i in range(2,3)]
        modsur = modSurface(surfobj, lstTup =lstTup)
        if modsur:
            guidMod = modsur.Id
            #surfaceAnal(guidMod, outfname="mod"+str(n*100),_LPP= 36000)
            
            #stationoffset(guidMod,_fore= 35956, _end=50, _zmin=-20, _zmax=5000,fname="off_xpan_mod")
            rs.DeleteObject(guidMod)
            #rs.ObjectColor( guidMod, (0,255,0))
      
    
    
 
    


    

if __name__ == "__main__":
    movecp()





