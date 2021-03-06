
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
-0.00001          0.00000          0.09848          0
-0.00012          0.00000          0.19687          0
-0.00044          0.00000          0.29509          0
-0.00110          0.00000          0.39302          0
-0.00226          0.00000          0.49051          0
-0.00412          0.00000          0.58740          0
-0.00693          0.00000          0.68349          0
-0.01096          0.00000          0.77852          0
-0.01657          0.00000          0.87220          0
-0.02416          0.00000          0.96418          0
-0.03425          0.00000          1.05403          0
-0.04743          0.00000          1.14122          0
-0.06440          0.00000          1.22516          0
-0.08601          0.00000          1.30513          0
-0.11323          0.00000          1.38029          0
-0.14683          0.00000          1.44998          0
-0.18703          0.00000          1.51402          0
-0.23381          0.00000          1.57241          0
-0.28694          0.00000          1.62536          0
-0.34593          0.00000          1.67329          0
-0.40999          0.00000          1.71687          0
-0.47807          0.00000          1.75701          0
-0.54890          0.00000          1.79479          0
-0.62111          0.00000          1.83139          0
-0.69340          0.00000          1.86792          0
-0.76528          0.00000          1.90481          0
-0.83677          0.00000          1.94202          0
-0.90791          0.00000          1.97953          0
-0.97874          0.00000          2.01732          0
-1.04928          0.00000          2.05535          0
-1.11957          0.00000          2.09359          0
-1.18964          0.00000          2.13203          0
-1.25950          0.00000          2.17063          0
-1.32920          0.00000          2.20939          0
-1.39875          0.00000          2.24827          0
-1.46816          0.00000          2.28726          0
-1.53747          0.00000          2.32635          0
-1.60667          0.00000          2.36552          0
-1.67580          0.00000          2.40477          9
""".strip()+'\n'

def stationoffset(srfid, _fore, _end, _zmin, _zmax, nz = 30, nx = 800 ,fname = "stoffset", vof =None):
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
                        
    print "Offset file Generated"            

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
        #print getrc
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
            
    modsur = doc.Objects.GripUpdate(_robj,0)  #  0 -> creates new surface
    
    
    _robj.GripsOn = 0
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

def readCsv(_fname):
    _fyl = open(_fname, 'r')
    lstTup =[]
    for l in _fyl:
        
        [u, v, x, y, z] = map(float,l.strip().split(','))
        lstTup.append((u,v,(x, y, z)))
    _fyl.close()
    return lstTup
            
            
    


def dacotamain():
    """
    function to be used with dacota 
    """
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    flgFile = open('_flgMsur','w')
    if obj:
        surfguid = obj[0]
        surfobj = _objref(surfguid)
        #basenurb = surfobj.Surface().ToNurbsSurface()
        #Generate initial surface files
        #surfaceAnal(surfguid, outfname="init", _LPP= 36000 )
        # Modify the surface
        _csvfile = rs.OpenFileName(" Select the transformation csv")
        lstTup = readCsv(_csvfile)
        modsur = modSurface(surfobj, lstTup =lstTup)
        
        if modsur:
            print "Surface modified"
            guidMod = modsur.Id
            rs.ObjectColor(guidMod,(0,255,0))
            #surfaceAnal(guidMod, outfname="mod"+str(n*100),_LPP= 36000)
            flgFile.write(str(1))
            #stationoffset(guidMod,_fore= 35956, _end=50, _zmin=-20, _zmax=5000,fname=r"C:\binSys\Optimisation\ForNAft\off_xpan_mod")
            #rs.DeleteObject(guidMod)
        else:
            flgFile.write(str(0))
    flgFile.close()
    
 
    


    

if __name__ == "__main__":
    dacotamain()





