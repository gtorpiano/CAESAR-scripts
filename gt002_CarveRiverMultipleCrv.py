import rhinoscriptsyntax as rs

crv = rs.GetObjects("crv")
srf = rs.GetObject("srf")

#project crv to srf
newCrv = []
for i in range (len(crv)):
    newCrv.append(rs.ProjectCurveToSurface(crv[i], srf, [0,0,1])[0])

srfPts = []
uRes = 180       
vRes = 100
uDom = rs.SurfaceDomain(srf,0)
uDom = uDom[1]-uDom[0]
vDom = rs.SurfaceDomain(srf,1)
vDom = vDom[1]-vDom[0]

#sample surface

ptList = []
for i in range(uRes+1):
    for j in range(vRes+1):
        nowU = i*(uDom/uRes)
        nowV = j*(vDom/vRes)
        nowPt = rs.EvaluateSurface(srf, nowU, nowV)
        for j in range(len(newCrv)):
            parCrv = rs.CurveClosestPoint(newCrv[j], nowPt)
            onCrv = rs.EvaluateCurve(newCrv[j], parCrv)
            if (rs.Distance(nowPt, onCrv)<10):
                nowPt[2] = 0
        ptList.append(nowPt)

#generate surface
newSrf = rs.AddSrfPtGrid((uRes+1, vRes+1), ptList)



#delete projected curves
for i in range(len(newCrv)):
    rs.DeleteObject(newCrv[i])