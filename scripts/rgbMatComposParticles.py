#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import yaml
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util.numpy_support import vtk_to_numpy

# ---
if len(sys.argv) != 3:
   print("Usage: "+sys.argv[0]+" <directory where to find the particles vtu files> <RGB values for compositions YAML file>")
   sys.exit(1)
# ---

# --- White only used when no dominant compo has been found
#     for a given marker (did not happen up-to-now).
white= ( 1.0, 1.0, 1.0)

# --- Dict to store the values for each material composition
#     for a given marker.
matComposValuesDict= {}

vtuFilesIn= glob.glob(sys.argv[1] + os.sep + "*.vtu")

# --- Get the RGB values associated to each material
#     compositions from a YAML config file.
RGBComposValuesFp= open(sys.argv[2],"r")
RGBComposValues= yaml.load(RGBComposValuesFp,Loader= yaml.SafeLoader)
RGBComposValuesFp.close()

# --- Create the vtk reader and writer objects.
reader= vtk.vtkXMLUnstructuredGridReader()
writer= vtk.vtkXMLUnstructuredGridWriter()

# --- Loop on all the vtu particles (a.k.a. markers) file(s).
for vtuFileIn in sorted(vtuFilesIn):

   print("Processing vtuFileIn="+vtuFileIn)

   reader= vtk.vtkXMLUnstructuredGridReader()   
   reader.SetFileName(vtuFileIn)
   print("aft reader.SetFileName(vtuFileIn)")

   reader.Update()
   print("aft reader.Update()")

   dataIn= reader.GetOutput()
   print("aft reader.GetOutput()")

   # --- Deep copy of all the vtu file content in order
   #     to update it.
   dataOut= dsa.WrapDataObject(dataIn)
   print("aft dsa.WrapDataObject(dataIn)")
   
   # --- Trick: Use the velocity data 3D vector for the RGB compositions output
   #    (Assuming that velocity data 3D vector is in the vtu in file)
   rgbVectorData= dataOut.GetPointData().GetArray("velocity") 

   assert rgbVectorData is not None, "ERROR: Must have the \"velocity\" vector field in the particles vtu file!"
   
   # --- Rename the velocity vector data field as RGBCompos for the output file
   rgbVectorData.SetName("RGBCompos")

   # --- particles position data for this timestamp
   pPos= dataOut.GetPointData().GetArray("position")

   #print("pPos="+str(pPos))
   #sys.exit(0)

   # --- particles numeric ids data
   pidData= dataOut.GetPointData().GetArray("id")
   
   # --- Get the material compositions values
   #     from the markers vtu file (point) data
   #     NOTE that the string names of the
   #     RGBComposValues MUST match the names
   #     of the material compositions names of
   #     the vtu file(s)
   for matCompo in RGBComposValues:
       
       #print("Reading mat. compo data: "+matCompo)
       # --- Store the array (field) of the material compo matCompo
       matComposValuesDict[matCompo]= dataOut.GetPointData().GetArray(matCompo)

       # --- TODO add check for compo existence here:
       assert matComposValuesDict[matCompo] is not None, \
          "ERROR: matComposValuesDict[matCompo] is None !!" 
   # ---

   # --- Print the number of markers found in the vtu file.
   pidDataSize= pidData.GetSize()
   print("pidData size="+str(pidDataSize))

   #pressurePField= dataOut.GetPointData().GetArray("p")
   
   emptyParticles= 0

   
   
   # --- Loop on all the markers found
   #     in the vtu file being processed.
   #     (Note the usage of the range(pidDataSize) 
   for pid in range(pidDataSize):

      #print("pid="+str(int(pid))) 
      #rgbVector= rgbVectorData.GetTuple(int(pid))
      #print("rgbVector="+str(rgbVector))

      nonZeroThreshold= 1e-42
      
      # --- Temp. local compo max and dominant compo id.
      compoMax= nonZeroThreshold #0.0
      domMatCompo= None

      # --- Loop on the material compos names.
      #     Again we MUST have that the string
      #     names keys of the RGBComposValues dict
      #     MUST match the names of the material
      #     compositions names of the vtu file(s)
      for matCompo in RGBComposValues:

          #print("matCompo="+matCompo)
          # --- Extract the compo value for this matCompo on
          #     the markera having the id "pid"
          if matCompo not in matComposValuesDict: continue
         
          tmpMatCompo= matComposValuesDict[matCompo].GetTuple(pid)[0]

          # --- Check if tmpMatCompo is the new compo maximum. 
          if tmpMatCompo > compoMax:

             # --- Update the compoMax and domMatCompo key accordingly
             compoMax= tmpMatCompo
             domMatCompo= matCompo

             #if not compoMax > nonZeroThreshold :
             #print("WARNING: tmpMatCompo <= 1e-32 at p. pos: "+str(pPos.GetTuple(int(pid))));
             #  sys.exit(0)
          #else:
          #   print("WARNING: tmpMatCompo <= nonZeroThreshold at p. pos: "+str(pPos.GetTuple(int(pid))));
          #   sys.exit(0)
          # ---   
      # ---

      # --- Did not happen up-to-now
      if domMatCompo is None:
         print("WARNING: No dominant compo for pid: "+str(pid)+" at p. pos: "+
               str(pPos.GetTuple(int(pid)))+", skipping this particle")
         emptyParticles += 1
         rgbVectorData.SetTuple(pid,white)
         continue
      
      # --- Set the RGB vector according to the dominant
      #     material composition found for the marker being
      #     processed (the float() operator usage here is
      #     probably not really necessary)
      rgbVector= ( float(RGBComposValues[domMatCompo]["Red"]),
                   float(RGBComposValues[domMatCompo]["Green"]),
                   float(RGBComposValues[domMatCompo]["Blue"]) )

      # --- Set the RGB vector at the marker position according to
      #     the dominant compo found for the marker being processed
      rgbVectorData.SetTuple(int(pid),rgbVector)
      
      #print("rgbVector="+str(rgbVectorData.GetTuple(int(pid))))
      
   # ---

   print("Done with loop on particles")

   # --- Did not happen up-to-now
   if emptyParticles > 0:
      print("WARNING: Found "+str(emptyParticles)+
            " particles with no composition at all for file: "+vtuFileIn)
      #sys.exit(0)
   
   # --- Now write the output (including the new RGBCompos vector field)
   #     in the new vtu file.

   # --- Use a temporary output vtu file
   newVTUFile= vtuFileIn+".new"
   
   writer.SetFileName(newVTUFile)

   # --- We copy all the input (except the velocity) and the
   #     newly defined RGBCompos vector field in the new vtu file
   writer.SetInputData(dataOut.VTKObject)

   # ---
   writer.Write()

   print("aft writer.Write()")
   
   # --- Rename the temp vtu file to the initial vtu file to
   #     fool the particles.pvd file
   os.rename(newVTUFile, vtuFileIn)

   # --- Need to also replace the "velocity" vector field name
   #     by the "RGBCompos" name in the companion pvtu file to
   #     again fool the particles.pvd file
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
