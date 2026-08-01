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

middlePointX= 1.49036e6
#leftLimitX= 500e3
rightLimitX= 3.0e6 - 500e3
elevLimitY= 700e3-140e3

oneMyInSeconds= 86400*365*1e6

# --- Create the vtk reader object.
reader= vtk.vtkXMLUnstructuredGridReader()

reader.SetFileName(vtuFileIn)
print("aft reader.SetFileName(vtuFileIn)")

reader.Update()
print("aft reader.Update()")

dataIn= reader.GetOutput()
print("aft reader.GetOutput()")

TField= dataIn.GetPointData().GetArray("T")

olmMrbField= dataIn.GetPointData().GetArray("oceanicLithMantleMRB")

points= dataIn.GetPoints()

#DepthsForT= {100.0: None, 200.0: None, 300: None, 400: None, 500:
#             None, 600: None, 700: None, 800: None, 900: None, 1000: None, 1100: None, 1200: None, 1300: None }
#DepthsForTAt= { 5e6: DepthsForT, 10e6: DepthsForT, 15e6: DepthsForT, 20e6: DepthsForT, 25e6: DepthsForT, 30e6: DepthsForT, 35e6: DepthsForT, 40e6: DepthsForT }
#depthsForTAtAges= {}

#TDef= (100.0,200.0,300.0,400.0,500.0,600.0,700.0,800.0,900.0,1000.0,1100.0,1200.0,1300.0)

TInfos= { 100.0: [], 200.0: [], 300.0: [],
          400.0: [], 500.0: [], 600.0: [],
          700.0: [], 800.0: [], 900.0: [],
          1000.0: [], 1100.0: [], 1200.0: [], 1300.0: [] }

TInfosKeys= tuple(TInfos.keys())

for pointIdx in range(0,points.GetNumberOfPoints()):

    point= points.GetPoint(pointIdx)

    #print("point="+str(point))
    #sys.exit(0)

    if point[0] < middlePointX or point[0] > rightLimitX or point[1] < elevLimitY:
        continue
    # ---

    checkT= TField.GetTuple(pointIdx)[0] - 273.0

    #print("checkT="+str(checkT))

    if checkT > 1300:
        continue
    # ---

    print("\npoint="+str(point))
    print("checkT="+str(checkT))

    distFromRidge= point[0] - middlePointX
    depth= 700e3-point[1]

    print("distFromRidge="+str(distFromRidge))
    print("depth="+str(depth))

    ageInYears= (distFromRidge/spreadVeloMPY)

    print("ageInYears="+str(ageInYears))

    ageInMy= ageInYears/1e6

    print("ageInMy="+str(ageInMy))

    #depthsForTAtAges[ageInMy]= checkT

    for Tc in TInfosKeys:

        TDiffCheck= math.fabs(Tc-checkT)

        if TDiffCheck < 5.0:

            TInfos[Tc].append({ "ageInMy": ageInMy, "depthKM": -(depth/1000.0), "distKmFromRidge": distFromRidge })
            #print("TInfos="+str(TInfos))
            #sys.exit(0)
        # ---
    # ---
# ---

for Tc in TInfosKeys:

    csvFp= open(str(Tc)+"-"+csvFileOut,"w")

    print("Tc="+str(Tc)+", nb. data="+str(len( TInfos[Tc])))

    csvFp.write("#age[My],depth(Km),distFromRidge(Km)\n")

    for TcInfo in TInfos[Tc] :

        csvFp.write(str(TcInfo["ageInMy"])+","+str(TcInfo["depthKM"])+","+str(TcInfo["distKmFromRidge"])+"\n")

    csvFp.close()
    
del reader
#csvFp.close()
