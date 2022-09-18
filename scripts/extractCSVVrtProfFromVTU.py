#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy #thats what you need 

# 1469 km from the left side
iPosExtract= 765000

vtuFilePath= sys.argv[1]
csvVrtProfFilePath= sys.argv[2]

reader= vtk.vtkXMLUnstructuredGridReader()

reader.SetFileName(vtuFilePath)
reader.Update()

PointCoordinates = reader.GetOutput().GetPoints().GetData()
#print(str(PointCoordinates.GetTuple(500)))

dataTmp= reader.GetOutput()
strainRateData= dataTmp.GetPointData().GetArray("strain_rate")

#print(strainRateData)

viscData= dataTmp.GetPointData().GetArray("viscosity")

viscDict= {}
strtDict= {}

for pci in range(PointCoordinates.GetSize()):

    pct= PointCoordinates.GetTuple(pci)

    #print("pct="+str(pct))
    #sys.exit(500)

    if int(math.floor(pct[0])) == iPosExtract:
        #print("pct[0]="+str(pct[0]))
        #print("visc[pci]="+str(viscData.GetTuple(pci)[0]))      
        #sys.exit(0)

        # --- index the data with the elevation from the bottom
        #     (inverted depth
        viscDict[pct[1]]= viscData.GetTuple(pci)[0]
        strtDict[pct[1]]= strainRateData.GetTuple(pci)[0]
# ---
 
# --- CSV
csvFp= open(csvVrtProfFilePath,"w")

csvFp.write("#elevation from bottom, strtDict, viscDict\n")
#csvFp.write("#elevation from bottom, viscDict\n")

for elev in sorted( tuple(viscDict.keys())):

   #csvFp.write(str(elev)+","+str(strtDict[elev])+","+str(viscDict[elev])+"\n")
   csvFp.write(str(elev)+","+str(math.log10(strtDict[elev]))+","+str(math.log10(viscDict[elev]))+"\n")
   #csvFp.write(str(elev)+","+str(viscDict[elev])+"\n")

csvFp.close()
