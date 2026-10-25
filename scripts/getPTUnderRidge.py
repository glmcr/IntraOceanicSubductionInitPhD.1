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

#spreadVeloMPY= 0.025 # meters/years 

#middlePointX= 1.48949e6 #1.49036e6
middlePointX= 1.49036e6
#middlePointX= 1.4925e6
#middlePointX= 1.498e6 #1.498e6 #1.495e6
#middlePointX= 1.501e6 #1.5e6
#leftLimitX= 500e3
rightLimitX= 3.0e6 - 500e3
#elevLimitY= 700e3-140e3
elevLimitY= 700e3 - 130e3 #680e3 #700e3 - 98.5e3 #100e3
#elevLimitY= 700e3-65e3

oneMyInSeconds= 86400*365*1e6
spreadVeloMPY= 0.025 # meters/years
#mantleDensSTP=3370.0

# --- Create the vtk reader object.
reader= vtk.vtkXMLUnstructuredGridReader()

reader.SetFileName(vtuFileIn)
print("aft reader.SetFileName(vtuFileIn)")

reader.Update()
print("aft reader.Update()")

dataIn= reader.GetOutput()
print("aft reader.GetOutput()")

PField= dataIn.GetPointData().GetArray("p")
TField= dataIn.GetPointData().GetArray("T")

points= dataIn.GetPoints()

PTUnderRidge= {}

#minDistFromRidge= 1.e20
#pointsElev= {}
#distInfo= {}

maxDistFromRidge= 0.0

solidusDpOnDt= 0.01650485436893204
solidusBAt273K= -22.615533980582526

for pointIdx in range(0,points.GetNumberOfPoints()):

    point= points.GetPoint(pointIdx)

    #print("point="+str(point))
    #sys.exit(0)

    distFromRidge= math.fabs(point[0] - middlePointX)

    ageInYears= (distFromRidge/spreadVeloMPY)

    #print("ageInYears="+str(ageInYears))

    ageInMy= ageInYears/1e6

    #print("ageInMy="+str(ageInMy))

    ageInMyRd= round(math.floor(ageInMy+0.5))

    #print("ageInMyRd="+str(ageInMyRd))
    #sys.exit(0)

    checkP= PField.GetTuple(pointIdx)[0]

    #if ageInMyRd > 0 or checkP > 10e9 or checkP < 0.2e9:
    if ageInMy > 0.5 or checkP > 10e9 or checkP < 0.2e9:
        continue

    TValueC= math.fabs(TField.GetTuple(pointIdx)[0]-273)

    #print("\npoint="+str(point))
    #print("distFromRidge="+str(distFromRidge))
    #print("ageInMy="+str(ageInMy))
    #print("checkP="+str(checkP))
    #print("TValueC="+str(TValueC))

    if checkP < 0.0:
        checkP= 0.0
    #sys.exit(0)

    #if TValueC < 0.0:
    #   TValueC = 

    print("\npoint="+str(point))
    print("distFromRidge="+str(distFromRidge))
    print("ageInMy="+str(ageInMy))
    print("checkP="+str(checkP))
    print("TValueC="+str(TValueC))       

    #TValue= TField.GetTuple(pointIdx)[0]

    PTUnderRidge[checkP]= TValueC
    #PTUnderRidge.append((checkP,TValue))

    if distFromRidge > maxDistFromRidge:
        maxDistFromRidge= distFromRidge
# --

del reader

csvFp= open(csvFileOut,"w")

csvFp.write("# T[C]m, P[Gpa], solidus(Gpa)\n")

for p in sorted(tuple(PTUnderRidge.keys())):

    pGpa= p/1e9

    solidusAtPT= solidusDpOnDt*(PTUnderRidge[p]+273) + solidusBAt273K

    csvFp.write(str(PTUnderRidge[p])+","+str(-pGpa)+","+str(-solidusAtPT)+"\n")
    #csvFp.write(str(-pGpa)+","+str(PTUnderRidge[p])+"\n")

# --

print("maxDistFromRidge="+str(maxDistFromRidge))

csvFp.close()
