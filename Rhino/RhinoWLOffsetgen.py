import rhinoscriptsyntax as rs
def getSurfaces():
    surface = rs.ObjectsByType(8)
    hidobj = rs.HiddenObjects()
    if hidobj:
        for obj in hidobj:
            rs.ShowObject(obj)
    outDic = {'mod' : None, 'Hull' : None}
    for srf in surface:
        print rs.ObjectName(srf)
        if rs.ObjectName(srf) == "Hull":
            #rs.HideObject(srf)
            outDic['Hull'] = srf
        elif rs.ObjectName(srf) == "mod":
            outDic['mod'] = srf   
        else:
            rs.DeleteObject(srf)
    return outDic


filename = "WL"
###
file = open( filename, "w" )
file.write("hull \n")
srfdic = getSurfaces()
surface = srfdic['Hull']
n =15
for i in range(1,int(n)):
    flg_stn = 1
    c1= (25000, 5000,i*200)
    c2= (45000, 5000, i*200)
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

        if rs.CurveStartPoint(lstCur[0])[2] < rs.CurveEndPoint(lstCur[0])[2]:
            sp = rs.CurveStartPoint(lstCur[0])
            lp = rs.CurveEndPoint(lstCur[0])
        else:
            lp = rs.CurveStartPoint(lstCur[0])
            sp = rs.CurveEndPoint(lstCur[0])
            
        points = rs.CurveContourPoints( lstCur[0], sp, lp)
        npts = len(points)
        cpt  =  1
        for pt in points:
            #print(str(pt.X)+","+str(pt.Y)+","+str(pt.Z))
            file.write( "{:.5f}".format(pt.X/1000.0))
            file.write( " " * 10)
            file.write( "{:.5f}".format(abs(pt.Y)/1000.0) )
            file.write( " " * 10)
            file.write( "{:.5f}".format(pt.Z/1000.0) )
            file.write( " " * 10)
            file.write( str(flg_stn) )
            file.write( "\n" )
            flg_stn = 0
            cpt += 1

#    rs.DeleteObject(lstCur[0])

file.write("end")
file.close()        