import rhinoscriptsyntax as rs
import math
import random

#functions
#to draw points if necessary
def drawPts(PTLIST):
    rs.EnableRedraw(False)
    for i in range(len(PTLIST)):
        for j in range(len(PTLIST[i])):
            rs.AddPoint(PTLIST[i][j])
    rs.EnableRedraw(True)

#identify surface
srf = rs.GetObject("Select surface", 8+16) #specify surface GUID

#bounding box
bbox = rs.BoundingBox(srf)
#measure distances between points
distList = []
for i in range(len(bbox)):
    for j in range(i+1, len(bbox)):
        dist = rs.Distance(bbox[i], bbox[j])
        distList.append([i,j,dist])
#sort list - this bit might not always work
sortList = sorted(distList, key=lambda k: k[2])
distY = sortList[12][2]
distX = sortList[4][2] 

#set sample resolution
cellSizeIdeal = 10 #m

#plot 2D grid over surface
stepsY = int(distY/cellSizeIdeal)+1
stepsX = int(distX/cellSizeIdeal)+1

ptList = []
for i in range(0, stepsY):
    row = []
    for j in range(0, stepsX):
        nowPt = [j*cellSizeIdeal, -i*cellSizeIdeal, 0]
        ptOnSrf = rs.ProjectPointToSurface (nowPt, srf, [0,0,1])
        if ptOnSrf:
            row.append(ptOnSrf[0])
        else:
            print "no point!"
    ptList.append(row)

#assign variables for text file
ncols = len(ptList[3])
nrows = len(ptList)
xllcorner = 0
yllcorner = 0
cellsize = cellSizeIdeal
NODATA_value = -9999

drawPts(ptList)


#generate text file
DEM_file = open("data/141214test01.txt", "w")

#write to text file
line1 = 'ncols         '+str(ncols) +'\n'
DEM_file.write(line1)
line2 = 'nrows         '+str(nrows) +'\n'
DEM_file.write(line2)
line3 = 'xllcorner     '+str(xllcorner) +'\n'
DEM_file.write(line3)
line4 = 'yllcorner     '+str(yllcorner) +'\n'
DEM_file.write(line4)
line5 = 'cellsize      '+str(cellsize) +'\n'
DEM_file.write(line5)
line6 = 'NODATA_value  '+str(NODATA_value) +'\n'
DEM_file.write(line6)

for i in range(len(ptList)):
    newLine = ""
    for j in range(len(ptList[i])):
        strValue = str("{0:.3f}".format(ptList[i][j][2]))
        newLine = newLine + strValue + ' '
    newLine = newLine +'\n'
    DEM_file.write(newLine)

DEM_file.close()
