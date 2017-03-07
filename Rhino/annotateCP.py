import rhinoscriptsyntax as rs
surface = rs.ObjectsByType(8)[0]
print rs.SurfaceArea(surface)
points = rs.SurfacePoints(surface)



count = rs.SurfacePointCount(surface)

i = 0
j =0
for u in range(count[0]):

    for v in range(count[1]):

        #print "CV[", u, ",", v, "] = ", points[i]
 #       rs.AddPoint(points[i])
        rs.AddTextDot(str(i),points[i])

        i += 1