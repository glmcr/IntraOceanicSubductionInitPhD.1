#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import json
import numpy as np
import pathlib
from vtk.util.numpy_support import vtk_to_numpy

vtuFileIn= sys.argv[1]

csvFileOut= sys.argv[2]

spreadVeloMPY= 0.025 # meters/years 

#middlePointX= 1.48949e6 #1.49036e6
middlePointX= 1.49036e6
#middlePointX= 1.4925e6
#middlePointX= 1.498e6 #1.498e6 #1.495e6
#middlePointX= 1.501e6 #1.5e6
#leftLimitX= 500e3
rightLimitX= 3.0e6 - 500e3
#elevLimitY= 700e3-140e3
elevLimitY= 690e3 #700e3 - 98.5e3 #100e3
#elevLimitY= 700e3-65e3

oneMyInSeconds= 86400*365*1e6

#mantleDensSTP=3370.0

# --- Create the vtk reader object.
reader= vtk.vtkXMLUnstructuredGridReader()

reader.SetFileName(vtuFileIn)
print("aft reader.SetFileName(vtuFileIn)")

reader.Update()
print("aft reader.Update()")

dataIn= reader.GetOutput()
print("aft reader.GetOutput()")

heatFluxMapField= dataIn.GetPointData().GetArray("heat_flux_map")

points= dataIn.GetPoints()

minDistFromRidge= 1.e20

pointsElevHeatFluxByAge= {}
distInfo= {}

for pointIdx in range(0,points.GetNumberOfPoints()):

    point= points.GetPoint(pointIdx)

    #print("point="+str(point))
    #sys.exit(0)

    # --- Only integrate from the middle point at ridge
    if point[0] < middlePointX or point[0] > rightLimitX or point[1] < elevLimitY:
        continue
    # ---

    heatFluxAtPoint= heatFluxMapField.GetTuple(pointIdx)[0]

    if heatFluxAtPoint < 0.0005:
       continue

    distFromRidge= point[0] - middlePointX

    #distInfo[ageInMyRd].append(distFromRidge)
    #depth= 700e3-point[1]

    print("distFromRidge="+str(distFromRidge))

    if distFromRidge < minDistFromRidge:
        minDistFromRidge= distFromRidge

    ageInYears= (distFromRidge/spreadVeloMPY)

    print("ageInYears="+str(ageInYears))

    ageInMy= ageInYears/1e6

    print("ageInMy="+str(ageInMy))

    ageInMyRd= round(math.floor(ageInMy+0.5))

    print("ageInMyRd="+str(ageInMyRd))
    #sys.exit(0)

    if ageInMyRd not in distInfo:
        distInfo[ageInMyRd]= []
    # ---
    
    distInfo[ageInMyRd].append(distFromRidge)

    if ageInMyRd not in pointsElevHeatFluxByAge:
       pointsElevHeatFluxByAge[ageInMyRd]= [] #{}
       #pointsElevHeatFluxByAge[ageInMyRd][point[1]]= []
    # ---

    pointsElevHeatFluxByAge[ageInMyRd].append(heatFluxAtPoint)
    #pointsElevHeatFluxByAge[ageInMyRd][point[1]]= heatFluxAtPoint

# ---
del reader

csvFp= open(csvFileOut,"w")
csvFp.write("#age[My], meanDistFromRidge[Km], heatFlow[W/m/m], log10(heatFlow[W/m/m])\n")

for age in sorted(pointsElevHeatFluxByAge):

    #maxElev= sorted(tuple(pointsElevHeatFluxByAge[age].keys()),reverse= True)[0]
    sortedHeatFlow= sorted(pointsElevHeatFluxByAge[age],reverse= True)

    maxHeatFlow= sortedHeatFlow[0]
    minHeatFlow= sortedHeatFlow[-1]

    meanHeatFlow= np.mean(sortedHeatFlow)

    meanDistFromRidge= np.mean(distInfo[age])

    print("\nAge="+str(age))
    print("maxHeatFlow="+str(maxHeatFlow))
    print("minHeatFlow="+str(minHeatFlow))
    print("meanHeatFlow="+str(meanHeatFlow))
    print("meanDistFromRidge="+str(meanDistFromRidge))
    #sys.exit(0)

    csvFp.write(str(age)+","+str(meanDistFromRidge)+","+str(meanHeatFlow)+","+str(math.log10(meanHeatFlow))+"\n")
# ---

csvFp.close()    
