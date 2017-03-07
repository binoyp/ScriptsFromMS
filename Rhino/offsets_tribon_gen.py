import rhinoscriptsyntax as rs
from  Rhino.Geometry.Curve import ProjectToBrep as _PrjCur
from Rhino.Geometry.Intersect.Intersection import BrepPlane as _IntPlaneSurf
from Rhino.Geometry import Point3d, Plane
from Rhino.Geometry import Line, Vector3d, Ray3d, LineCurve
from scriptcontext import doc
import os 
def stationoffset(srfid, _fore, _end, _zmin, _zmax, nz = 40, nx = 250,fname = "stoffset", vof =None):
    brep = rs.coercebrep(srfid)
    dx = (_fore -_end) / nx
    _file = open(fname, 'w')
    
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

                ptno = 1
                curpliname = 'pli'+str(i)
                curdatfile = open(curpliname,'w')
                macdata = "create pli cur /file="+str(curpliname)+"\nPrefit\nDisplay Points \nDIS CUR \nACCEPT SEC "+str(stpt0.X/1000)
                _file.write(macdata)
                for j in range(nz+1):
                    
                    if j != nz:
                        offpt = cur.PointAtLength(j*dz)
                    else:
                        offpt = cur.PointAtEnd
                    if offpt.IsValid:
                        curdatfile.write( "{:.5f}".format(offpt.X/1000.0) )
                        curdatfile.write( " " * 10)
                        curdatfile.write( "{:.5f}".format(abs(offpt.Y)/1000.0) )
                        curdatfile.write( " " * 10)
                        curdatfile.write( "{:.5f}".format(offpt.Z/1000.0) )
                        curdatfile.write( " " * 10)
                        if j == 0:
                            #doc.Objects.AddPoint(offpt)
                            curdatfile.write("Knuckle\t\t"+str(ptno))
                        elif (j ==nz):

                            curdatfile.write("Knuckle\t\t"+str(ptno))
                                
                        else:
                            curdatfile.write("Ordinary\t\t"+str(ptno))
                        ptno += 1
                    curdatfile.write('\n')
                                
                _file.write("\n")
                curdatfile.close()


    _file.close()


if __name__ == "__main__":
    # LPP  = rs.StringBox (message="Enter LPP in current units",\
    #                      default_value=None, title="LPP")
    # LPP = float(LPP)
    LPP = 36046.0
    AFTEND = -2433
    # minZ =rs.StringBox (message="Min Z Value", default_value=None, title="MinZ")
    minZ = 0
    minZ = float(minZ)
    # maxZ = rs.StringBox (message="Max Z", default_value=None, title="Maximum Z")
    maxZ = 5000
    maxZ = float(maxZ)
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    if obj:
        surfguid = obj[0]
        offname = rs.SaveFileName("macro name")
        stationoffset(surfguid, LPP,AFTEND, minZ, maxZ, vof = None, fname=offname)
    doc.Views.Redraw()
