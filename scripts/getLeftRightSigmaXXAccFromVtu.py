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

vtuFileIn=sys.argv[1]

# --- Create the vtk reader and writer objects.
reader= vtk.vtkXMLUnstructuredGridReader()
#writer= vtk.vtkXMLUnstructuredGridWriter()


reader.SetFileName(vtuFileIn)
print("aft reader.SetFileName(vtuFileIn)")

reader.Update()
print("aft reader.Update()")

dataIn= reader.GetOutput()
print("aft reader.GetOutput()")

#print(dir(reader))

stressTensors=dataIn.GetPointData().GetArray("stress")

#print("dir(stressTensor)="+str(dir(stressTensor)))
stressTensorsSize= stressTensors.GetSize()
print("stressTensorsSize="+str(stressTensorsSize))

#stressTensorSize= stressTensor[0].GetSize()
#print("stressTensor[0].GetSize()="+str(stressTensor[0].GetSize()))
#print("stressTensor.GetValue(0)="+str(stressTensor.GetValue(0)))

print("stressTensors.GetTuple(0)=["+str(stressTensors.GetTuple(0))+"]")

#mappedDataArray=stressTensors.MappedDataArray
#print("dir(mappedDataArray)="+str(dir(mappedDataArray)))
#dataArray= stressTensors.CreateDataArray(0)
#print("dir(dataArray)="+str(dir(dataArray)))
#print(reader.POINT_DATA)

points= dataIn.GetPoints()
#print(dir(points))
#print(points.GetPoint(0))
#print(points.GetPoint(1))
#print(points.GetPoint(2))
#print(points.GetPoint(3))
#print(points.GetPoint(4))
#print(points.GetPoint(5))
print("points.GetNumberOfPoints()="+str(points.GetNumberOfPoints()))

leftXDist=14018.0
rightXDist=2.98598e6
yFromBottom=594000.0

leftSigXXAcc=0.0
rightSigXXAcc=0.0

#pointIdx=0

#for point in points:
for pointIdx in range(0,points.GetNumberOfPoints()):

    point= points.GetPoint(pointIdx)

    #print(dir(point))
    
    if (math.fabs(point[0] - leftXDist) < 1.0) and  (point[1] >= yFromBottom):

        leftSigXXAcc += stressTensors.GetTuple(pointIdx)[0]

        print("leftSigXXAcc="+str(leftSigXXAcc))
        print("pointIdx="+str(pointIdx)+", point="+str(point))
        #sys.exit(0)

    if (math.fabs(point[0] - rightXDist) < 10.0) and  (point[1] >= yFromBottom):

        rightSigXXAcc += stressTensors.GetTuple(pointIdx)[0]
    
        print("rightSigXXAcc="+str(rightSigXXAcc))
        print("pointIdx="+str(pointIdx)+", point="+str(point))
        #sys.exit(0)
    # ---    
    #pointIdx += 1

# ---

print("final leftSigXXAcc="+str(leftSigXXAcc))
print("final rightSigXXAcc="+str(rightSigXXAcc))
