
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

_BOW ="""
36.00000          0.00000          0.81536          1
36.00316          0.00000          0.84099          0
36.00599          0.00000          0.86663          0
36.00852          0.00000          0.89228          0
36.01078          0.00000          0.91793          0
36.01277          0.00000          0.94359          0
36.01453          0.00000          0.96926          0
36.01606          0.00000          0.99493          0
36.01739          0.00000          1.02060          0
36.01854          0.00000          1.04628          0
36.01951          0.00000          1.07197          0
36.02034          0.00000          1.09766          0
36.02102          0.00000          1.12335          0
36.02158          0.00000          1.14904          0
36.02204          0.00000          1.17474          0
36.02240          0.00000          1.20044          0
36.02269          0.00000          1.22614          0
36.02291          0.00000          1.25184          0
36.02308          0.00000          1.27754          0
36.02322          0.00000          1.30325          0
36.02335          0.00000          1.32895          0
36.02347          0.00000          1.35466          0
36.02359          0.00000          1.38036          0
36.02373          0.00000          1.40607          0
36.02388          0.00000          1.43177          0
36.02404          0.00000          1.45748          0
36.02422          0.00000          1.48318          0
36.02440          0.00000          1.50888          0
36.02459          0.00000          1.53459          0
36.02480          0.00000          1.56029          0
36.02501          0.00000          1.58599          0
36.02524          0.00000          1.61170          0
36.02547          0.00000          1.63740          0
36.02572          0.00000          1.66310          0
36.02598          0.00000          1.68880          0
36.02624          0.00000          1.71450          0
36.02652          0.00000          1.74020          0
36.02680          0.00000          1.76591          0
36.02709          0.00000          1.79161          0
36.02740          0.00000          1.81731          0
36.02771          0.00000          1.84301          0
36.02803          0.00000          1.86871          0
36.02836          0.00000          1.89441          0
36.02869          0.00000          1.92011          0
36.02904          0.00000          1.94581          0
36.02939          0.00000          1.97151          0
36.02975          0.00000          1.99721          0
36.03012          0.00000          2.02290          0
36.03050          0.00000          2.04860          0
36.03088          0.00000          2.07430          0
36.03127          0.00000          2.10000          0""".strip()+'\n'
_STERN="""0.00000          0.00000          0.00000          1
-0.00000          0.00000          0.03812          0
-0.00001          0.00000          0.07623          0
-0.00002          0.00000          0.11435          0
-0.00006          0.00000          0.15246          0
-0.00011          0.00000          0.19056          0
-0.00020          0.00000          0.22865          0
-0.00032          0.00000          0.26674          0
-0.00049          0.00000          0.30481          0
-0.00071          0.00000          0.34286          0
-0.00099          0.00000          0.38090          0
-0.00135          0.00000          0.41892          0
-0.00179          0.00000          0.45691          0
-0.00233          0.00000          0.49488          0
-0.00297          0.00000          0.53282          0
-0.00374          0.00000          0.57072          0
-0.00465          0.00000          0.60858          0
-0.00571          0.00000          0.64640          0
-0.00695          0.00000          0.68417          0
-0.00839          0.00000          0.72189          0
-0.01004          0.00000          0.75954          0
-0.01193          0.00000          0.79713          0
-0.01409          0.00000          0.83464          0
-0.01656          0.00000          0.87206          0
-0.01935          0.00000          0.90940          0
-0.02252          0.00000          0.94663          0
-0.02611          0.00000          0.98374          0
-0.03015          0.00000          1.02072          0
-0.03471          0.00000          1.05756          0
-0.03985          0.00000          1.09424          0
-0.04563          0.00000          1.13073          0
-0.05213          0.00000          1.16702          0
-0.05945          0.00000          1.20309          0
-0.06768          0.00000          1.23890          0
-0.07696          0.00000          1.27441          0
-0.08742          0.00000          1.30959          0
-0.09923          0.00000          1.34440          0
-0.11259          0.00000          1.37876          0
-0.12768          0.00000          1.41265          0
-0.14465          0.00000          1.44600          0
-0.16366          0.00000          1.47879          0
-0.18487          0.00000          1.51095          0
-0.20844          0.00000          1.54246          0
-0.23456          0.00000          1.57324          0
-0.26338          0.00000          1.60327          0
-0.29504          0.00000          1.63251          0
-0.32961          0.00000          1.66092          0
-0.36713          0.00000          1.68851          0
-0.40750          0.00000          1.71530          0
-0.45051          0.00000          1.74135          9
"""

def stationoffset(srfid, _fore, _end, _zmin, _zmax, nz = 30, nx = 1000,fname = "stoffset", vof =None):
    brep = rs.coercebrep(srfid)
    dx = (_fore -_end) / nx
    _file = open(fname, 'w')
    
    _file.write("hull\n")
    _file.write(_BOW)
    
    for i in range(nx +1):
        # for j in range(nz + 1):
        stpt0 = Point3d(_fore - i*dx, -10, _zmin )
        cPlane = Plane(stpt0, Vector3d(1,0,0))
        #stpt1 = Point3d(_fore - i*dx, -10, _zmax )
        #curL = Line(stpt0, stpt1)
        #lCur = LineCurve(curL)
        #curList = _PrjCur(lCur, brep, Vector3d(0,1,0), doc.ModelAbsoluteTolerance)
        (res, curList, ptList) = _IntPlaneSurf(brep, cPlane, doc.ModelAbsoluteTolerance)
        if res and len(curList) == 1:
            #print len(curList)
            for cur in curList:
                
                _curLength =  cur.GetLength()
                endpt = cur.PointAtLength(_curLength)
                st0 = cur.PointAtLength(0)
                
                dz = _curLength/nz
                if st0.Z > endpt.Z:
                    cur.Reverse()
                #doc.Objects.AddCurve(cur)
                
                for j in range(nz+1):
                    #print j*dz

                    # offpt = cur.PointAtLength(_curLength - j*dz)
                    # else:
                    if j != nz:
                        offpt = cur.PointAtLength(j*dz)
                    else:
                        offpt = cur.PointAtEnd
                    if offpt.IsValid:
                        _file.write( "{:.5f}".format(offpt.X/1000.0) )
                        _file.write( " " * 10)
                        _file.write( "{:.5f}".format(abs(offpt.Y)/1000.0) )
                        _file.write( " " * 10)
                        _file.write( "{:.5f}".format(offpt.Z/1000.0) )
                        _file.write( " " * 10)
                        if j == 0:
                            #doc.Objects.AddPoint(offpt)
                            _file.write("1")
                        elif (j ==nz):
                            if i == nx:
                                if vof:  # grid for vof method last line
                                    _file.write("0\n")
                                    _file.write( "{:.5f}".format(offpt.X/1000.0) )
                                    _file.write( " " * 10)
                                    _file.write( "{:.5f}".format(abs(offpt.Y)/1000.0) )
                                    _file.write( " " * 10)
                                    _file.write( "{:.5f}".format(float(vof)) )
                                    _file.write( " " * 10)
                                    _file.write("0")
                                else:
                                    _file.write("0")
                            else:
                                _file.write("0")
                                if vof:
                                    _file.write( "\n{:.5f}".format(offpt.X/1000.0) )
                                    _file.write( " " * 10)
                                    _file.write( "{:.5f}".format(abs(offpt.Y)/1000.0) )
                                    _file.write( " " * 10)
                                    _file.write( "{:.5f}".format(float(vof)) )
                                    _file.write( " " * 10)
                                    _file.write("0")

                        else:
                            _file.write("0")
                        if j == nz:
                            pass
                            #print  offpt.IsValid
                            #doc.Objects.AddPoint(offpt)
                        _file.write("\n")
    _file.write(_STERN)
    _file.write("end")           
    _file.close()
                        
                

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
    
def modSurface(nurbSur, dist = 500, minZ = 500, traVec =(0,1,0), col = [2], _LPP = 36.145, rows = range(20)):
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
    modsur = doc.Objects.GripUpdate(_robj,0)  #  0 -> creates new surface
    doc.Views.Redraw()
    return modsur

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
    surfaceAnal(surfguid, outfname="init", _LPP= 36000 )
    # Modify the surface
    for n in (-4,-3.5,-2,-1.5,-1,-0.5):
        # Generate Modify Surface
        modsur = modSurface(surfobj, col =1, dist = n*100, minZ= 30)
        
        if modsur:
            guidMod = modsur.Id
            surfaceAnal(guidMod, outfname="mod"+str(n*100),_LPP= 36000)
            
            stationoffset(guidMod,_fore= 35956, _end=50,_zmin=0, _zmax=5000,fname="xpan-"+str(n*100))
            #rs.DeleteObject(guidMod)
    
def dacotamain():
    """
    function to be used with dacota 
    """
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    if obj:
        surfguid = obj[0]
        surfobj = _objref(surfguid)
        #basenurb = surfobj.Surface().ToNurbsSurface()
      #Generate initial surface files
    surfaceAnal(surfguid, outfname="init", _LPP= 36000 )
    # Modify the surface
    
 
    


    

if __name__ == "__main__":
    main()
else:
    print range(-5,5)




