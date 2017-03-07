
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
from Rhino.Geometry import Point2d as _pt2d
from Rhino.Geometry import Line, Vector3d, Intersect, ControlPoint
from Rhino.DocObjects.Tables import ObjectTable

_LPP = 38000                    #  Lpp in millimeters




# Getting Data points on the curve
# the curve is 3D not 2D as desired.
#for i in  testcur.GrevillePoints(): rs.AddPoint(i)

#Control Points
#for i in  testcur.Points:
#    rs.AddPoint(i.Location)


#rs.AddPoint(testcur.Points[1].Location)

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
#       rs.AddPoint(stpt)
#       print stpt
       nurbCurves[stpt.Z] = nobj

    return nurbCurves
    
def tangentVec(nurbCur):
    """
    nurbCur = single curve object
    return {0:x , 1:y, 2:z}
    """
    ############################################
    # The forward tangent vector is calculated #
    ############################################
    
    st = nurbCur.PointAtStart
    pt2 =nurbCur.Points[1].Location
    _end = nurbCur.PointAtEnd
    
#    rs.AddPoint(st)
#    rs.AddPoint(pt2)
    d = st.DistanceTo(pt2)
    outdic={}
    if _end.X < st.X:
        tang = nurbCur.TangentAtStart
    else:
        tang = nurbCur.TangentAtEnd
    for i,ang in enumerate(tang):
        
        outdic[i] = ang
#         print 1*'\n'
#         print (pt2[i] - st[i])
# #        print ang
        # print math.degrees(math.acos(ang))
    return outdic
    
def genTanGenFile(fname, curlist):
    """
    ######################################
    # fname is the file name             #
    # Generates files with tangent data  #
    # z ang1, ang2, ang3                 #
    ######################################
    
    """
    _file = open(fname,'w')
    _file.write('h\tx\ty\tz\n')  # header line
    
    # curlist = nurbcurvelist()
#    print curlist

    curTans ={}
    for (z, cur) in sorted(curlist.items(), key=operator.itemgetter(0)):

        tang = tangentVec(cur)
        curTans[z]={0:tang[0],1:tang[1], 2:tang[2]}
        _file.write('{}\t{:.5f}\t{:.5f}\t{:.5f}\n'.format(z ,tang[0],tang[1],tang[2]))
       
    _file.close()
        
        
def curvAnal():
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    _snurb = _objref(obj[0]).Surface().ToNurbsSurface()

    
    _robj = _objref(obj[0]).Object()
    _robj.GripsOn = 1
    scriptcontext.doc.Views.Redraw()

    _brep = _objref(obj[0]).Surface().ToBrep()
    points = _snurb.Points
    uc =  points.CountU
    vc = points.CountV



    ########################################################
    # When surface direction is from fore to aft           #
    # the following loop will calculate the tangent        #
    # at for v points and then calculate the corresponding #
    # data points.                                         #
    ########################################################


    wlcurs = {}                 # List for water lines
    isocurs = {}                # List for iso curvews
    for j in range(vc):
        # rs.AddPoint( points.GetGrevillePoint(1, j).Location)
        
        gpt0 =  points.GetGrevillePoint(0,j)
        
        pt0 = _snurb.PointAt(gpt0[0], gpt0[1])
        if pt0.Z > 50:
            
            lpt1 = pt0 + _pt3d(-1 * _LPP/2, -100, 0)
            lpt0 = pt0 + _pt3d(100, -100, 0)
            _curL = Line(lpt0, lpt1)

            lguid = scriptcontext.doc.Objects.AddLine(_curL)
            wl = rs.ProjectCurveToSurface(lguid, obj[0], (0,1,0))
            if len(wl) == 1:
                wlcurs[pt0.Z] = wl[0]
                rs.DeleteObject(lguid)
                curIso = _snurb.IsoCurve(0,j)
                isocurs[pt0.Z]=curIso

                scriptcontext.doc.Objects.AddCurve(isocurs[pt0.Z])

                
    
    grips = _robj.GetGrips()
    for g in range(grips.Length):
        curgrip = grips[g]
        getrc, curu, curv = _snurb.ClosestPoint(curgrip.CurrentLocation)
        # rs.AddPoint(curgrip.CurrentLocation)
        for j in range(vc):
            curCp = points.GetControlPoint(uc-2,j)
            _dis = curCp.Location.DistanceTo(curgrip.CurrentLocation)
            if curCp.Location.Z > 500:
                if abs(_dis) < 0.0001:
                    rs.AddPoint(curgrip.CurrentLocation)
                    mVec = Vector3d(0,1,0)
                    print mVec.Unitize()
                    mVec = mVec * 500
                    curgrip.Move(mVec)
                
                
    scriptcontext.doc.Objects.GripUpdate(_robj,1)
    scriptcontext.doc.Views.Redraw()
      ###############################################################
      # GripObject[] grips = obj.GetGrips();                        #
      # for (int i = 0; i < grips.Length; i++)                      #
      # {                                                           #
      #   GripObject grip = grips[i];                               #
      #   double u, v;                                              #
      #   if (srf.ClosestPoint(grip.CurrentLocation, out u, out v)) #
      #   {                                                         #
      #     Vector3d dir = srf.NormalAt(u, v);                      #
      #     dir.Unitize();                                          #
      #     dir *= 0.5;                                             #
      #     grip.Move(dir);                                         #
      #   }                                                         #
      # }                                                           #
      #                                                             #
      # doc.Objects.GripUpdate(obj, false);                         #
      # doc.Views.Redraw();                                         #
      ###############################################################





      
    # for j in range(vc):
    #     _curcp = _snurb.Points.GetControlPoint(2,j).Location + _pt3d(0,8500,0)
    #     _ctrlpt = ControlPoint(_curcp)
    #   
        # _pts = [pt0 + _pt3d(-i*100, 0, 0) for i in range(1500)]
        # pts = Intersect.Intersection.ProjectPointsToBreps( [_brep], _pts, Vector3d(0, 1, 0), scriptcontext.doc.ModelAbsoluteTolerance)
        
        # if pts != None and pts.Length > 0:
            # pass
            # for pt in pts:
            #     scriptcontext.doc.Objects.AddPoint(pt)

  
    wlNurbs = {}
    for id in wlcurs:
        wlNurbs[id] = _objref(wlcurs[id]).Curve()

    genTanGenFile('wl', wlNurbs)
    genTanGenFile('iso', isocurs)

    


if __name__ == "__main__":
    curvAnal()





