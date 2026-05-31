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

leftXDist= 14018.0
rightXDist= 2.98598e6
#yFromBottom=594000.0 # LAB
yFromBottom= 700000.0 - 150000 # strain rate

#vtuFileIn=sys.argv[1]
vtuFilesIn= sorted(glob.glob(sys.argv[1]+"/*.vtu"))

#print("vtuFilesIn="+str(vtuFilesIn))

begConvMy= float(sys.argv[2]) #int(42e6)

outCsv= open(sys.argv[3],"w")

outCsv.write("#year[My],left acc. sigXX[GN/m],right acc. sigXX[GN/m]\n")

for vtuFileIn in vtuFilesIn:

    print("processing vtuFileIn -> "+vtuFileIn)
    
    # --- Create the vtk reader and writer objects.
    reader= vtk.vtkXMLUnstructuredGridReader()

    reader.SetFileName(vtuFileIn)
    print("aft reader.SetFileName(vtuFileIn)")

    reader.Update()
    print("aft reader.Update()")

    dataIn= reader.GetOutput()
    print("aft reader.GetOutput()")

    #time=dataIn.GetPointData().GetField("TIME")
    #print("time="+str(time))

    dataMy= ( dataIn.GetFieldData().GetArray("TIME").GetTuple(0)[0] - begConvMy)/1e6
    print("dataMy="+str(dataMy))
    
    #print("dataIn.GetScalars()="+str(dataIn.GetScalars()))
    #print(dir(dataIn))
    #print(dir(dataIn.GetPointData()))
    #print("dataIn.GetAttributes()="+str(dataIn.GetAttributes(0)))

    pressureField= dataIn.GetPointData().GetArray("p")
    stressTensors= dataIn.GetPointData().GetArray("stress")

    #print("dataIn.__getattribute__(TIME)="+str(dataIn.__getattribute__("TIME")))

    #print("dir(stressTensors)="+str(dir(stressTensors)))
    stressTensorsSize= stressTensors.GetSize()
    print("stressTensorsSize="+str(stressTensorsSize))

    #print("stressTensors.GetInformation()="+str(stressTensors.GetInformation()))
    #sys.exit(0)
    
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

    leftSigXXAcc=0.0
    rightSigXXAcc=0.0

    nbDepthsRight= nbDepthsLeft= 0
    
    #pointIdx=0

    #for point in points:
    for pointIdx in range(0,points.GetNumberOfPoints()):

        point= points.GetPoint(pointIdx)

        pressure= pressureField.GetTuple(pointIdx)[0]
        #print("point="+str(point)+", pressure="+str(pressure))
        #sys.exit(0)

        depthOk= (point[1] >= yFromBottom)

        if depthOk:

           #nbDepths += 1
           #print("point="+str(point)+", pressure="+str(pressure))
           #sys.exit(0)            
    
           if (math.fabs(point[0] - leftXDist) < 1.0) :

              #leftSigXXAcc += math.fabs(stressTensors.GetTuple(pointIdx)[0])
              leftSigXXAcc += (stressTensors.GetTuple(pointIdx)[0] + pressure)

              nbDepthsLeft += 1
              
           #print("leftSigXXAcc="+str(leftSigXXAcc))
           #print("pointIdx="+str(pointIdx)+", point="+str(point))
           #sys.exit(0)

           if (math.fabs(point[0] - rightXDist) < 10.0): # and  (point[1] >= yFromBottom):

              #rightSigXXAcc += math.fabs(stressTensors.GetTuple(pointIdx)[0])
              rightSigXXAcc += (stressTensors.GetTuple(pointIdx)[0] + pressure)
              nbDepthsRight += 1
              
           #print("rightSigXXAcc="+str(rightSigXXAcc))
           #print("pointIdx="+str(pointIdx)+", point="+str(point))
           #sys.exit(0)
           # ---
    # ---    
    #pointIdx += 1
    print("final leftSigXXAcc="+str(leftSigXXAcc))
    print("final rightSigXXAcc="+str(rightSigXXAcc))
    print("nbDepthsLeft="+str(nbDepthsLeft))
    print("nbDepthsRight="+str(nbDepthsRight))

    outCsv.write(str(dataMy)+","+str(leftSigXXAcc/1e9)+","+str(rightSigXXAcc/1e9)+"\n")
    #outCsv.write(str(dataMy)+","+str(leftSigXXAcc/nbDepthsLeft)+","+str(rightSigXXAcc/nbDepthsRight)+"\n")
    
    print("Done with vtuFileIn -> "+vtuFileIn)

    del dataIn
    del reader
    #sys.exit(0)
# ---

#print("final leftSigXXAcc="+str(leftSigXXAcc))
#print("final rightSigXXAcc="+str(rightSigXXAcc))
