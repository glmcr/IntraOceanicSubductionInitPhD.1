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

    "lusi oceanicCrust"         : (        0.0,  102.0/255.0,         0.0), # Forest green, basalts & gabbros
    #"lusi oceanicLithMantle"    : (        0.0,  204.0/255.0,         0.0),
    "lusi oceanicLithMantle"    : ( 51.0/255.0, 255.0/255.0,  51.0/255.0),  # light green, harzburgite & dunite 
    #"lusi asthenosphere"        : (  51.0/255.0, 255.0/255.0,  51.0/255.0),
    "lusi asthenosphere"        : (        0.0,  204.0/255.0,         0.0), # intermediate green, lerzholite
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

## --- oceanic crust + oceanic seds Hybrid rock material (not present in the direct output files)
#oCrustPlusSedsHybMatRGB= ( 153.0/255.0, 153.0/255.0, 0.0)

white= ( 1.0, 1.0, 1.0)

dataDict= {}

vtuFilesIn= glob.glob(sys.argv[1] + os.sep + "*.vtu")

reader= vtk.vtkXMLUnstructuredGridReader()
writer= vtk.vtkXMLUnstructuredGridWriter()

for vtuFileIn in sorted(vtuFilesIn):

   print("Processing vtuFileIn="+vtuFileIn)

   reader= vtk.vtkXMLUnstructuredGridReader()

   #print("aft 
   
   reader.SetFileName(vtuFileIn)

   print("aft reader.SetFileName(vtuFileIn)")

   reader.Update()

   print("aft reader.Update()")

   dataIn= reader.GetOutput()

   print("aft reader.GetOutput()")

   # --- Deep copy of all the vtu file content.
   dataOut= dsa.WrapDataObject(dataIn)

   print("aft dsa.WrapDataObject(dataIn)")
   
   # --- Trick: Use the velocity data 3D vector for the RGB compositions output
   #    (Assuming that velocity data 3D vector is in the vtu in file)
   rgbVectorData= dataOut.GetPointData().GetArray("velocity") 

   # --- Rename the velocity vector data field as RGBCompos for the output file
   rgbVectorData.SetName("RGBCompos")

   #--- particles position data for the timestamp
   pPos= dataOut.GetPointData().GetArray("position")

   #print("pPos="+str(pPos))
   #sys.exit(0)

   pidData= dataOut.GetPointData().GetArray("id")
   
   # --- Set the RGB values according to the dominant composition
   #     at the particle location.
   for matCompo in RGBComposValues:
       
       #print("Reading mat. compo data: "+matCompo)
       dataDict[matCompo]= dataOut.GetPointData().GetArray(matCompo)

       # --- TODO add check for compo existence here:
       #if dataDict[matCompo] is None: 
       
   # ---

   pidDataSize= pidData.GetSize()
   print("pidData size="+str(pidDataSize))

   pressurePField= dataOut.GetPointData().GetArray("p")
   
   emptyParticles= 0
   
   #for pid in sorted(pidData):
   for pid in range(pidDataSize):

      #print("pid="+str(int(pid))) 
      #rgbVector= rgbVectorData.GetTuple(int(pid))
      #print("rgbVector="+str(rgbVector))
      
      compoMax= 0.0
      domMatCompo= None

      # ---
      for matCompo in RGBComposValues:

          #print("matCompo="+matCompo)
          tmpMatCompo= dataDict[matCompo].GetTuple(pid)[0]

          if tmpMatCompo > compoMax:
             compoMax= tmpMatCompo
             domMatCompo= matCompo
          # ---   
      # ---

      if domMatCompo is None:
         print("WARNING: No dominant compo for pid: "+str(pid)+" at p. pos: "+
               str(pPos.GetTuple(int(pid)))+", skipping this particle")
         emptyParticles += 1
         rgbVectorData.SetTuple(pid,white)
         continue
      
      # --- Set the RGB vector at the particle location according to
      #     the dominant compo RGB vector.
      rgbVectorData.SetTuple(int(pid),RGBComposValues[domMatCompo])
      
      #print("rgbVector="+str(rgbVectorData.GetTuple(int(pid))))

      ## --- Check if we have a mix between seds and oc. crust
      ##     at the surface (depth <= ~1km)
      #if domMatCompo == "lusi oceanicCrust":
      #   if dataDict["lusi oceanicSeds"].GetTuple(pid)[0] >= 0.5 :# and pressurePField[pid] < 1.5e7:  #pPos[pid][1] >= 699500.0:
      #      if pPos[pid][1] >= 699500.0:
      #         # --- Sediments only at depths < 500m
      #         #print("oc. crust + oc. seds mixture, p. position="+str(pPos.GetTuple(int(pid))))
      #         rgbVectorData.SetTuple(int(pid),RGBComposValues["lusi oceanicSeds"])
      #         #print("pPos[pid][1]="+str(pPos[pid][1])+", oc. seds compo here")
      #         #sys.exit(0)
      #      elif pressurePField[pid] < 2e7:
      #         # --- oc. crust + oc. seds mixture here
      #         rgbVectorData.SetTuple(int(pid),oCrustPlusSedsHybMatRGB)   
      #      # ---
      # ---      
   # ---

   print("Done with loop on particles")
   
   if emptyParticles > 0:
      print("WARNING: Found "+str(emptyParticles)+
            " particles with no composition at all for file: "+vtuFileIn)
      #sys.exit(0)
   
   # --- Now write the output fields in the new vtu file
   #writer= vtk.vtkXMLUnstructuredGridWriter()

   # --- Use a temp. output vtu file
   newVTUFile= vtuFileIn+".new"
   
   writer.SetFileName(newVTUFile)

   # --- We copy all the input (except the velocity) and the
   #     newly defined RGBCompos vector data in the new vtu file
   writer.SetInputData(dataOut.VTKObject)

   # ---
   writer.Write()

   print("aft writer.Write()")
   
   # --- Rename the temp vtu file to the initial vtu file to
   #     fool the particles.pvd file
   os.rename(newVTUFile, vtuFileIn)

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

   # --- Copy all ASCII lines in the new pvtu file
   #     but we replace the "velocity" string in the related
   #     line but the "RGBCompos" string
   for pvtuFileLine in pvtuFileLines:

       #print("line written="+ pvtuFileLine.replace("velocity","RGBCompos"))
       newPvtuFp.write(pvtuFileLine.replace("velocity","RGBCompos"))

   newPvtuFp.close()

   # --- Rename new pvtu as the initial one.
   os.rename(newPvtuFile, pvtuFile)

   print("done with vtuFileIn="+vtuFileIn)

   #del reader
   #del writer
   #del rgbVectorData
   #del dataIn
   #del dataOut
   
   #sys.exit(0)
   
# ---
