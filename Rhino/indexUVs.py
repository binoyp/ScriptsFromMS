
import rhinoscriptsyntax as rs
from scriptcontext import doc
import Rhino
import operator
import  Rhino.DocObjects.ObjRef as _objref
from Rhino.Geometry import Point3d as _pt3d
from Rhino.Geometry import Line, Vector3d, Point3d, Plane
from Rhino.Geometry.Intersect.Intersection import BrepPlane as _IntPlaneSurf
def main():
    """
    first generate parameters for the input surface
    """
    obj = rs.ObjectsByType (8|16, select=0, state=0)
    if obj:
        surfguid = obj[0]
        surfobj = _objref(surfguid)
        modSurface(surfobj)
        
        
        
def modSurface(nurbSur, dist = 500, minZ = 500, traVec =(0,1,0), col = 2, _LPP = 36.145):
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
    uc = points.CountU
    for i in range(uc):
        for j in range(vc):
            rs.AddTextDot(str(i)+","+str(j), points.GetControlPoint(i, j).Location)
            
main()