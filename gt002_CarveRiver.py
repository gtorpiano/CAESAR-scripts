import rhinoscriptsyntax as rs

crv = "a6f3a052-1493-47c3-a040-08e8c05b9ee3"
srf = "f2640092-38ce-4bbe-bf09-b465381b0069"

#project crv to srf
newCrv = rs.ProjectCurveToSurface(crv, srf, [0,0,1])[0]

srfPts = []
uRes = 100
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
        parCrv = rs.CurveClosestPoint(newCrv, nowPt)
        onCrv = rs.EvaluateCurve(newCrv, parCrv)
        if (rs.Distance(nowPt, onCrv)<40):
            nowPt[2] = 0
        ptList.append(nowPt)

#generate surface
newSrf = rs.AddSrfPtGrid((uRes+1, vRes+1), ptList)

#print newSrf

#delete projected curve
rs.DeleteObject(newCrv)