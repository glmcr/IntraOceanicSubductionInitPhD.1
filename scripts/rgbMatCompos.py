#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util.numpy_support import vtk_to_numpy

# --- TODO: Read this from a YAML or a Json input file.
RGBComposValues= {

    "lusi oceanicCrust"         : (        0.0,  102.0/255.0,         0.0), # Deep green
    "lusi oceanicLithMantle"    : (        0.0,  204.0/255.0,         0.0),
    "lusi asthenosphere"        : (  51.0/255.0, 255.0/255.0,  51.0/255.0),
    "lusi oceanicSeds"          : ( 255.0/255.0, 255.0/255.0,         0.0),
    "lusi oceanicCrustSSZ"      : ( 102.0/255.0,         0.0, 102.0/255.0),
    "lusi oceanicLithMantleSSZ" : ( 204.0/255.0,         0.0, 204.0/255.0),
    "lusi greenschists"         : ( 102.0/255.0, 102.0/255.0,         0.0),
    "lusi blueschists"          : (  51.0/255.0,  51.0/255.0, 255.0/255.0),
    "lusi amphibolites"         : ( 255.0/255.0, 128.0/255.0,         0.0),
    "lusi granulites"           : ( 255.0/255.0,         0.0,         0.0),
    "lusi eclogites"            : (         0.0,         0.0,         0.0),
    "lusi pmeltedSszAsth"       : ( 192.0/255.0, 192.0/255.0, 192.0/255.0)
}

dataDict= {}

vtuFilesIn= glob.glob(sys.argv[1] + os.sep + "*.vtu")

reader= vtk.vtkXMLUnstructuredGridReader()

for vtuFileIn in vtuFilesIn:

   print("Processing vtuFileIn="+vtuFileIn)
   
   reader.SetFileName(vtuFileIn)
   reader.Update()

   dataIn= reader.GetOutput()

   # --- Deep copy of all the vtu file content.
   dataOut= dsa.WrapDataObject(dataIn)

   # --- Trick: Use the velocity data 3D vector for the RGB compositions output
   #    (Assuming that velocity data 3D vector is in the vtu in file)
   rgbVectorData= dataOut.GetPointData().GetArray("velocity") 

   # --- Rename the velocity vector data field as RGBCompos for the output file
   rgbVectorData.SetName("RGBCompos")

   #--- particles position data for the timestamp
   pPos= dataOut.GetPointData().GetArray("position")   

   pidData= dataOut.GetPointData().GetArray("id")
   
   # --- Set the RGB values according to the dominant composition
   #     at the particle location.
   for matCompo in RGBComposValues:
       
       #print("Reading mat. compo data: "+matCompo)
       dataDict[matCompo]= dataOut.GetPointData().GetArray(matCompo)

       # --- TODO add check for compo existence here:
       #if dataDict[matCompo] is None: 
       
   # ---
       
   for pid in pidData:

      #print("pid="+str(int(pid))) 
      #rgbVector= rgbVectorData.GetTuple(int(pid))
      #print("rgbVector="+str(rgbVector))
      
      compoMax= 0.0
      domMatCompo= None

      # ---
      for matCompo in RGBComposValues:

          #print("matCompo="+matCompo)
          tmpMatCompo= dataDict[matCompo].GetTuple(int(pid))[0]

          if tmpMatCompo > compoMax:
             compoMax= tmpMatCompo
             domMatCompo= matCompo
          # ---   
      # ---

      #rgbVector= RGBComposValues[domMatCompo]
      rgbVectorData.SetTuple(int(pid),RGBComposValues[domMatCompo])
      
      #print("rgbVector="+str(rgbVectorData.GetTuple(int(pid))))
      
      #sys.exit(0)
   # ---
      
   #sys.exit(0)
   
   # --- Now write the output fields in the new vtu file
   writer= vtk.vtkXMLUnstructuredGridWriter()

   # --- Use a temp. output vtu file
   tmpVTUFile= vtuFileIn+".tmp"
   
   writer.SetFileName(vtuFileIn+".tmp")

   # --- We will copy all the input (except the velocity) and the
   #     newly defined RGBCompos vector data
   writer.SetInputData(dataOut.VTKObject)

   # ---
   writer.Write()

   # --- Rename the temp vtu file to the initial vtu file to
   #     fool the particles.pvd file
   #os.rename(tmpVTUFile, vtuFileIn)

   # --- Need to also replace the "velocity" vector field name
   #     by the "RGBCompos" name in the pvtu file to again fool
   #     the particles.pvd file
   pvtuFile= os.path.dirname(vtuFileIn) + os.sep + os.path.basename(vtuFileIn).split(".")[0] + ".pvtu"

   #print("pvtuFile="+pvtuFile)
   #sys.exit(0)

   pvtuFp= open(pvtuFile,"r")
   pvtuFileLines= pvtuFp.readlines()
   pvtuFp.close()
   
   newPvtuFile= pvtuFile+".new"
   newPvtuFp= open(newPvtuFile,"w")

   # --- 
   for pvtuFileLine in pvtuFileLines:

       #print("line written="+ pvtuFileLine.replace("velocity","RGBCompos"))
       newPvtuFp.write(pvtuFileLine.replace("velocity","RGBCompos"))

   newPvtuFp.close()

   # --- Rename new pvtu as the initial one.
   #os.rename(newPvtuFile, pvtuFile)

   print("done with vtuFileIn="+vtuFileIn)
   
   sys.exit(0)
   
# ---
