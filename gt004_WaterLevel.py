import rhinoscriptsyntax as rs
import math
import random
import gt001_DEMreader as gt001

#function to find neighbours
def find_my_neighb(I, J):
    cell0 = [I-1, J-1]
    cell1 = [I-1, J]
    cell2 = [I-1, J+1]
    cell3 = [I, J+1]
    cell4 = [I+1, J+1]
    cell5 = [I+1, J]
    cell6 = [I+1, J-1]
    cell7 = [I, J-1]
    NEIGHBCELLS = [cell0, cell1, cell2, cell3, cell4, cell5, cell6, cell7]
    return NEIGHBCELLS


#read water DEM
DEMwaterdata = gt001.readDEM('data/waterdepth.txt')

#assign variables
ncols = DEMwaterdata[0][0]
nrows = DEMwaterdata[0][1]
xllcorner = DEMwaterdata[0][2]
yllcorner = DEMwaterdata[0][3]
cellsize = DEMwaterdata[0][4]
NODATA_value = DEMwaterdata[0][5]

#assign data
water = DEMwaterdata[1]

#read land DEM
DEMlanddata = gt001.readDEM('data/elev.txt')
landscape = DEMlanddata[1]


#draw points for water
rs.EnableRedraw(False)
for i in range(len(water)):
    for j in range(len(water[i])):
        if water[i][j] != NODATA_value:
            nowPt = gt001.myPos(i, j, water)
            #add landscape elevation
            nowPt[2] = nowPt[2] + landscape[i][j]
            rs.AddPoint(nowPt)
rs.EnableRedraw(True)


#to extract lines

#read through water data
#store any pts that do not contain water but which touch water
rs.EnableRedraw(False)
edgePts = []
for i in range(len(water)-1):
    for j in range(len(water[i])-1):
        #if pt does not contain water
        if water[i][j] == NODATA_value:
            #check surrounding cells for water
            #if not any of edges
            if (i!=0 or j!=0 or i!=len(water)-1 or j!=len(water[i])-1):
                #find neighbours - von Neumann neighbourhood
                cell1 = water[i-1][j]
                cell3 = water[i][j+1]
                cell5 = water[i+1][j]
                cell7 = water[i][j-1]
                neighbCells = [cell1, cell3, cell5, cell7]
                #check neighbours
                check = False
                for k in range(len(neighbCells)):
                    if neighbCells[k]!=NODATA_value:
                        check = True
                if check==True:
                    ptPos = gt001.myPos(i, j, water)
                    ptPos[2] = landscape[i][j]
                    edgePts.append([i,j])
                    #rs.AddPoint(ptPos)


#find end points
endPts = []
for k in range(len(edgePts)):
    #find neighbour Ids - complete neighbourhood
    i = edgePts[k][0]
    j = edgePts[k][1]
    neighbCells = find_my_neighb(i, j)
    tally = 0
    #check if neighbour Ids match any in list of water edge points
    for l in range(len(edgePts)):
        for m in range(len(neighbCells)):
            if neighbCells[m]==edgePts[l]:
                tally = tally + 1
    if tally==1:
        endPts.append(edgePts[k])

# draw end points
"""
for k in range(len(endPts)):
    i = endPts[k][0]
    j = endPts[k][1]
    ptPos = gt001.myPos(i, j, water)
    ptPos[2] = landscape[i][j]
    rs.AddPoint(ptPos)
"""


#collect points to draw lines starting from end points
chains = []
for k in range(len(endPts)):
    newLine = []
    i = endPts[k][0]
    j = endPts[k][1]
    #append first point index
    newLine.append([i,j])
    #previous cell check must be given a value
    prevcell = endPts[k]
    #check refers to existence of a next cell in chain
    check = True
    while (check == True):
        check = False
        #find neighbours
        neighbCells = find_my_neighb(i, j)
        nextCells = []
        #find possible next cells
        for l in range(len(edgePts)):
            for m in range(len(neighbCells)):
                if neighbCells[m]==edgePts[l]:
                    nextcell = edgePts[l]
                    #append cell to possible next cells
                    nextCells.append(nextcell)
                    check = True
        #select next cell from possible options
        counter = 0
        existsAlready = True
        found = False
        while (counter<len(nextCells)) and (existsAlready==True) and (check==True):
            found = False #next step identified
            nowCell = nextCells[counter]
            #check if already in list
            if nowCell in newLine:
                existsAlready = True
                found = False
            else:
                existsAlready = False
                found = True
            counter = counter+1
        if (found==False):
            check = False
        else:
            #reset i,j
            i = nowCell[0]
            j = nowCell[1]
            newLine.append(nowCell)
        
        #added ability to bridge close gaps
        if (check==False):
            lastPtPos = gt001.myPos(i, j, landscape)
            lastPtPos[2] = 0
            otherPossible = []
            #measure distance on 2D grid to nearby points
            for l in range(len(edgePts)):
                ptPos = gt001.myPos(edgePts[l][0], edgePts[l][1], landscape)
                ptPos[2] = 0
                dist = rs.Distance(lastPtPos, ptPos)
                nowCell = edgePts[l]
                if dist<25:
                    if nowCell not in newLine:
                        otherPossible.append([edgePts[l], dist])
                        
            if len(otherPossible)>0:
                #sort options by distance
                sortedList = sorted(otherPossible, key=lambda k: k[1])
                nowCell = sortedList[0][0]
                #reset i,j
                i = nowCell[0]
                j = nowCell[1]
                newLine.append(nowCell)
                check = True
    chains.append(newLine)
    

#attempt to draw lines
for i in range(len(chains)):
    #convert indices to points
    ptList = []
    for j in range(len(chains[i])):
        pt = gt001.myPos(chains[i][j][0], chains[i][j][1], landscape)
        ptList.append(pt)
    rs.AddInterpCurve(ptList)

rs.EnableRedraw(True)