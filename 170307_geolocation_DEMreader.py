import rhinoscriptsyntax as rs
import math
import random

#function to find cell position in space
def myPos(I, J, LISTOFCELLS):
    xPos = J*cellsize
    yPos = I*-cellsize
    zPos = LISTOFCELLS[I][J]
    if zPos == -9999:
        zPos = 0
    if geoL == True:
        xPos = xPos+xllcorner
        yPos = yPos+yllcorner+(cellsize*nrows)
    return rs.coerce3dpoint([xPos, yPos, zPos])

#function to read landscape and fill data structure
def readDEM(PATH):
    #open DEM
    DEM_file = open(PATH, 'r')
    
    #read first few lines containing DEM properties and save to list
    DEM_var = []
    for i in range (0, 6):
        line = DEM_file.readline()
        DEM_var.append(line.split())
    
    ALLDATA = []
    
    #assign variables
    NCOLS = int(DEM_var[0][1])
    NROWS = int(DEM_var[1][1])
    XLLCORNER = int(float(DEM_var[2][1]))
    YLLCORNER = int(float(DEM_var[3][1]))
    CELLSIZE = int(float(DEM_var[4][1]))
    NODATA_VALUE = int(DEM_var[5][1])
    
    #set up data structure describing landscape
    DEM_list = list(DEM_file)
    
    
    cellheights = [] #landscape data structure
    
    #fill data structure
    for i in range(len(DEM_list)):
        tempList = DEM_list[i].split()
        for j in range(len(tempList)):
            tempList[j] = float(tempList[j])
        cellheights.append(tempList)
    
    #append stuff to ALLDATA to be returned
    ALLDATA.append([NCOLS, NROWS, XLLCORNER, YLLCORNER, CELLSIZE, NODATA_VALUE])
    ALLDATA.append(cellheights)
    return ALLDATA

defaultPath = "C:/Users/Rajendra/Desktop/f141.txt"

path = rs.GetString("path:/", defaultPath)
geoL = rs.GetString("geo-locate", "Y", ["N", "Y"])
if geoL == "Y":
    geoL = True
else:
    geoL = False

DEMdata = readDEM(path)

#assign variables
ncols = DEMdata[0][0]
nrows = DEMdata[0][1]
xllcorner = DEMdata[0][2]
yllcorner = DEMdata[0][3]
cellsize = DEMdata[0][4]
NODATA_value = DEMdata[0][5]

landscape = DEMdata[1]

#draw landscape
rs.EnableRedraw(False)

srfPts = []
for i in range(len(landscape)):
    for j in range(len(landscape[i])):
        nowCellPt = myPos(i, j, landscape)
        srfPts.append(nowCellPt)

srf = rs.AddSrfPtGrid((nrows, ncols), srfPts)

rs.EnableRedraw(True)

