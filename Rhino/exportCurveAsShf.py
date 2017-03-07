
import rhinoscriptsyntax as rs



def export_shf(file,object_id):
#    object_id = rs.GetObject("Select curve", rs.filter.curve)
    if( object_id==None ): return

    #Get the filename to create

#    if( filename==None ): return
    if rs.IsCurveClosed(object_id):
        start_point = rs.GetPoint("Base point of center line")
    
        end_point = rs.GetPoint("Endpoint of center line", start_point)
        
        points = rs.CurveContourPoints(object_id, start_point, end_point)
    else:
        if rs.CurveStartPoint(object_id)[2] < rs.CurveEndPoint(object_id)[2]:
            sp = rs.CurveStartPoint(object_id)
            lp = rs.CurveEndPoint(object_id)
        else:
            lp = rs.CurveStartPoint(object_id)
            sp = rs.CurveEndPoint(object_id)
            
        points = rs.CurveContourPoints(object_id,sp,lp)
    npts = len(points)
#    cpt  =  1
    flg_stn = 1
    rs.ObjectColor(object_id,(255,0,0))
    for pt in points:
        print(str(pt.X)+","+str(pt.Y)+","+str(pt.Z))
        file.write( "{:0.5f}".format(pt.X/1000.0) )
        file.write( " " * 10)
        file.write( "{:0.5f}".format(abs(pt.Y)/1000.0) )
        file.write( " " * 10)
        file.write( "{:0.5f}".format(pt.Z/1000.0) )
        file.write( " " * 10)
#        if i == n-1 and  cpt == npts:
#            flg_stn = 9
        file.write( str(flg_stn) )
        flg_stn = 0
        file.write( "\n" )



filter = "Text File (*.shf)|*.shf|All Files (*.*)|*.*||"
filename = rs.SaveFileName("Save point coordinates as", filter)
curcurve = rs.GetObject("Select curve", rs.filter.curve)
file = open(filename,'w')
file.write("hull \n")
while curcurve <> None:
    export_shf(file,curcurve)
    curcurve = rs.GetObject("Select curve", rs.filter.curve)
file.write('end')

file.close()
rs.MessageBox("File saved as '"+filename +"'\n Please edit manually to put flag 9")
    