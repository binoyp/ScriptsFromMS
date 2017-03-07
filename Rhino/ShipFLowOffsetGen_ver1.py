import rhinoscriptsyntax as rs
from  Rhino.Geometry.Curve import ProjectToBrep as _PrjCur
from Rhino.Geometry.Intersect.Intersection import BrepPlane as _IntPlaneSurf
from Rhino.Geometry import Point3d, Plane
from Rhino.Geometry import Line, Vector3d, Ray3d, LineCurve
from scriptcontext import doc

def stationoffset(srfid, _fore, _end, _zmin, _zmax, nz = 20, nx = 1000,fname = "stoffset", vof =None):
    brep = rs.coercebrep(srfid)
    dx = (_fore -_end) / nx
    _file = open(fname, 'w')
    _file.write("hull\n")
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
                doc.Objects.AddCurve(cur)
                
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
                                    _file.write("9")
                                else:
                                    _file.write("9")
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

    _file.write("end")           
    _file.close()
                        
                
                
                
                
                # doc.Objects.AddPoint(endpt)
                # doc.Objects.AddPoint(st0)
        
            
            #############################################################################
            # point = _Prj([brep],[stpt0], Vector3d(0,1,0), doc.ModelAbsoluteTolerance) #
            # if len(point):                                                            #
            #     # print point[0].X, len(point)                                        #
            #     doc.Objects.AddPoint(point[0])                                        #
            #############################################################################
            
        
        
    

if __name__ == "__main__":
    # LPP  = rs.StringBox (message="Enter LPP in current units",\
    #                      default_value=None, title="LPP")
    # LPP = float(LPP)
    LPP = 35956
    AFTEND = 50
    # minZ =rs.StringBox (message="Min Z Value", default_value=None, title="MinZ")
    minZ = 0
    minZ = float(minZ)
    # maxZ = rs.StringBox (message="Max Z", default_value=None, title="Maximum Z")
    maxZ = 5000
    maxZ = float(maxZ)
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    if obj:
        surfguid = obj[0]
        
        stationoffset(surfguid, LPP,AFTEND, minZ, maxZ, vof = 3.5, fname=offname)
    doc.Views.Redraw()
