import rhinoscriptsyntax as rs
import math


# This script can be used to generate shipflow offsets from rhino surface
# ---------------------------
#|                          |
#|                          |
#AP-------------------------FP

#x2_________________________x1
# the points x1 and x2 should be below the base line

#x1 should be the foreend of the hull surface
#x2 Aft End

x1 = rs.GetPoint("Pick start point")
x2 = rs.GetPoint("Pick end point")
h = rs.GetPoint("Pick a point above deck")
n = rs.GetInteger("Number of stations", 30, 0)
dx = rs.Distance(x1,x2)/ n


#  file for saving shf file
surface = rs.GetObject("Select surface to project onto", rs.filter.surface)
filter = "Text File (*.shf)|*.shf|All Files (*.*)|*.*||"
filename = rs.SaveFileName("Save point coordinates as", filter)
###

file = open( filename, "w" )
file.write("hull \n")

for i in range(1,n):
    flg_stn = 1
    c1= (x1[0] - i*dx, x1[1], x1[2])
    c2= (x1[0] - i*dx, x1[1], h[2])
    curp1= rs.AddPoint(c1)
    curp2= rs.AddPoint(c2)
    curl = rs.AddLine(curp1, curp2)
    rs.DeleteObject(curp1)
    rs.DeleteObject(curp2)
    lstCur = rs.ProjectCurveToSurface(curl, surface, (0,1,0))
    rs.DeleteObject(curl)
    if len(lstCur) <> 1 :
        print "Error in Projection"
    else:
        if rs.IsCurveClosed(lstCur[0]):
            start_point = rs.GetPoint("Base point of center line")
        
            end_point = rs.GetPoint("Endpoint of center line", start_point)
            
            points = rs.CurveContourPoints(lstCur[0], start_point, end_point)
        else:
            if rs.CurveStartPoint(lstCur[0])[2] < rs.CurveEndPoint(lstCur[0])[2]:
                sp = rs.CurveStartPoint(lstCur[0])
                lp = rs.CurveEndPoint(lstCur[0])
            else:
                lp = rs.CurveStartPoint(lstCur[0])
                sp = rs.CurveEndPoint(lstCur[0])
                
            points = rs.CurveContourPoints(lstCur[0],sp,lp)
        npts = len(points)
        cpt  =  1
        for pt in points:
            print(str(pt.X)+","+str(pt.Y)+","+str(pt.Z))
            file.write( "{:.5f}".format(pt.X/1000.0) )
            file.write( " " * 10)
            file.write( "{:.5f}".format(abs(pt.Y)/1000.0) )
            file.write( " " * 10)
            file.write( "{:.5f}".format(pt.Z/1000.0) )
            file.write( " " * 10)
            if i == n-1 and  cpt == npts:
                flg_stn = 9
            file.write( str(flg_stn) )
            file.write( "\n" )
            flg_stn = 0
            cpt += 1
    
        rs.DeleteObject(lstCur[0])
file.write("end")
file.close()