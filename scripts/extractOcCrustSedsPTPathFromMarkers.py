#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import json
import numpy #as np
import pathlib

import h5py
#from vtk.util.numpy_support import vtk_to_numpy #thats what you need 

# -- VTU file with which the initial positions of the metam material(s)
#    are intialized to go backward in time. This vtu file is not necessarily
#    the final one.
#vtuParticlesInitFile= sys.argv[1]

# directory where the particles hdf5 files are located
particlesDir = sys.argv[1]
#metamGroupInfoFile= sys.argv[2]
#csvFileOut= sys.argv[4]
minCompoValue= float(sys.argv[2])
csvFilesOuputFolder= sys.argv[3]
#metamGroupInfoFile= sys.argv[4]

#protolithCompoName="lusi oceanicCrustMRB"

# --- Get the metam. mats. info from the metamGroupInfoFile
#metamGroupInfoFileP= open(metamGroupInfoFile,"r")
#metamGroupInfoDict= json.load(metamGroupInfoFileP)
#metamGroupInfoFileP.close()

vtuPFiles= sorted(glob.glob(particlesDir + "/*.vtu"))
h5PFiles= sorted(glob.glob(particlesDir + "/*.h5")) #,  reverse= True)

firstVTUFile= vtuPFiles[0]

print("Reading first vtu file -> "+firstVTUFile+" to init the markers tracking with their initial time")

reader= vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(firstVTUFile)
reader.Update()

#--- 
dataTmpStart= reader.GetOutput()
   
#--- Extract the timestamp (in years) as an int for this VTU file
dataTimeStart= int( dataTmpStart.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

print("dataTimeStart="+str(dataTimeStart))

# --- now h5 data
h5Data= h5py.File(h5PFiles[0],"r")

#pidDataEnd= dataTmpEnd.GetPointData().GetArray("id")
#pidDataSizeEnd= pidDataEnd.GetSize()
pidData= numpy.copy(h5Data["id"])
pidDataSize= pidData.shape[0]
print("pidData size="+str(pidDataSize)+"\n")
#sys.exit(0)

ocCrustPDataStart= numpy.copy(h5Data["lusi oceanicCrustMRB"])

#ocSedPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicSeds")
ocSedsPDataStart= numpy.copy(h5Data["lusi oceanicSeds"])

#--- particles position data for the 1st timestamp
pPosDataStart= numpy.copy(h5Data["position"])

pInitPosDataStart= numpy.copy(h5Data["initial position"])

pPDataStart= numpy.copy(h5Data["p"])
pTDataStart= numpy.copy(h5Data["T"])

ocCrustTrack= {}
ocSedsTrack= {}

yElevMin= 250e3
xMin= 0.5e6
xMax= 2.5e6

for pidIter in range(0,pidDataSize):

     pidPosX= pPosDataStart[pidIter][0]
     pidPosY= pPosDataStart[pidIter][1]

    #pid= pidDataEnd[pidIter][0]
    #print("nodesDataEnd[pidIter]="+str(nodesDataEnd[pidIter]))
    #sys.exit(0)
    
     if pidPosY < yElevMin: #600e3:
       continue

    #if pidPosX < 1e6 or pidPosX > 2e6:
     if pidPosX < xMin or pidPosX > pidPosX:
       continue

     pPosStr= str(pPosDataStart[pidIter][0])+","+str(pPosDataStart[pidIter][1])

     initPosStr= str(pInitPosDataStart[pidIter][0])+","+str(pInitPosDataStart[pidIter][1])

     if ocCrustPDataStart[pidIter,0] > minCompoValue:

         ocCrustTrack[pPosStr]= { "initPos": initPosStr, "times": { dataTimeStart: { "pressure": pPDataStart[pidIter,0], "T": pTDataStart[pidIter,0] }}}

         #print("ocCrust: pPosStr="+pPosStr+", ocCrustTrack[pPosStr]="+str(ocCrustTrack[pPosStr]))
         #sys.exit(0)
         
     if ocSedsPDataStart[pidIter,0] > minCompoValue:

         ocSedsTrack[pPosStr]= {  "initPos": initPosStr, "times": { dataTimeStart: { "pressure": pPDataStart[pidIter,0], "T": pTDataStart[pidIter,0] }} }
# ---

print("Nb. init oc. crust="+str(len(ocCrustTrack.keys())))
print("Nb. init oc. seds="+str(len(ocSedsTrack.keys())))

h5Data.close()

for vtuFile in sorted(vtuPFiles[1:]): #,reverse=True):

   reader= vtk.vtkXMLUnstructuredGridReader()

   print("\nReading vtu file -> "+vtuFile)

   reader.SetFileName(vtuFile)
   reader.Update()

   vtuData= reader.GetOutput()
   
   dataTime= int(vtuData.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

   print("dataTime="+str(dataTime))
   
   del vtuData
   del reader

   h5FilePath= particlesDir+"/particles-"+ os.path.basename(vtuFile).split("-")[1].split(".")[0]+".h5"

   print("h5FilePath="+str(h5FilePath))

   h5Data= h5py.File(h5FilePath,"r")
   
   pidData= numpy.copy(h5Data["id"])

   pidDataSize= pidData.shape[0]

   print("pidDataSize="+str(pidDataSize))

   initPosData= numpy.copy(h5Data["initial position"])

   pPosData= numpy.copy(h5Data["position"])

   pPData= numpy.copy(h5Data["p"])

   pTData= numpy.copy(h5Data["T"])

   for ocCrustT0PosItem in ocCrustTrack:

       ocCrustItemInitPos= ocCrustTrack[ocCrustT0PosItem]["initPos"]
   
       for pidIter in range(0,pidDataSize):

          pidPosX= pPosData[pidIter][0]
          pidPosY= pPosData[pidIter][1]
          
          if pidPosY < yElevMin: #600e3:
             continue
          if pidPosX < xMin or pidPosX > pidPosX:
             continue

          initPosStr= str(pPosData[pidIter][0])+","+str(pPosData[pidIter][1])

          if initPosStr == ocCrustItemInitPos:

               ocCrustTrack[ocCrustT0PosItem]["times"][dataTime]= {"pressure": pPData[pidIter,0], "T": pTData[pidIter,0] }

               print("ocCrustT0PosItem="+ocCrustT0PosItem+", ocCrustTrack[ocCrustT0PosItem]="+str(ocCrustTrack[ocCrustT0PosItem]))
               sys.exit(0)
          # ---
   # ---

   h5Data.close()
   
