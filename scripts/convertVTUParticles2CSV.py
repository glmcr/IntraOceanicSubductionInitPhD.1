#!/usr/bin/python3

import os
import sys
import glob
import vtk #.vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy #thats what you need 

# directory where the VTU particles file are located
vtuParticlesDir = sys.argv[1]
csvFileOut= sys.argv[2]

vtuPFiles= sorted(glob.glob(vtuParticlesDir + "/*.vtu"))
reader= vtk.vtkXMLUnstructuredGridReader()

vtuPData= {}

# Only consider oceanic crust particles that have Pressure
# and Temperature values over those low limits thresholds
ocPLow= 4e8 # GPa, 4e8 == shorcut for 4*math.pow(10,8)
ocTLow= 673 # Kelvin -> 400C

# Only consider particle ids for oceanic crust particles
# that have a concentration > 0.5
ocCrtThr= 0.5

gridYMeters= 700e3

for vtuPFile in vtuPFiles:
                     
   print("Reading vtuPFile: "+vtuPFile)
   vtuPFileName= os.path.basename(vtuPFile)
                     
   reader.SetFileName(vtuPFile)
   reader.Update()
   
   #vtuPData[vtuPFileName]= reader.GetOutput()

   #--- Extract all the particles data
   dataTmp= reader.GetOutput()
   #--- Extract the timestamp (in years) as an int
   dataTime= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

   #--- Index the the particles data with the timestamp
   #vtuPData[dataTime]= dataTmp
   #pidData= vtuPData[dataTime].GetPointData().GetArray("id")
   pidData= dataTmp.GetPointData().GetArray("id")

   print("dataTime="+str(dataTime))

   pidDataSize= pidData.GetSize()
   print("pidData size="+str(pidDataSize)+"\n")

   #--- particles position data
   pPos= dataTmp.GetPointData().GetArray("position")
   
   #--- Extract oceanic crust particles data:
   ocCrustData= dataTmp.GetPointData().GetArray("oceanicCrust")
   
   #--- Extract particle Pressure data:
   pPData= dataTmp.GetPointData().GetArray("p")
   
   #--- Extract particles Temperature data:
   pTData= dataTmp.GetPointData().GetArray("T")
   
   relevantOCrustData= {}
   
   for pid in range(pidDataSize):

       ocpCrt= ocCrustData.GetTuple(pid)[0]
       ocpP= pPData.GetTuple(pid)[0]
       ocpT= pTData.GetTuple(pid)[0]       
       
       if ocpCrt >= ocCrtThr and ocpP >= ocPLow and ocpT >= ocTLow:
           
          ocpPos= pPos.GetTuple(pid)
          
          #print("ocpCrt="+str(ocpCrt))
          #print("ocpPos="+str(ocpPos))
          #print("ocpP="+str(ocpP))
          #print("ocpT="+str(ocpT))

          relevantOCrustData[pid]= {
                                     "concentration": ocpCrt,
                                     "Pressure(GPa)": ocpP,
                                     "Temperature(K)": ocpT,
                                     "Temperature(C)": ocpT-273,
                                     "Depth(m)": gridYMeters - ocpPos[1]
                                   }

          #print("relevantOCrustData[pid]="+str(relevantOCrustData[pid]))
          #relevantOCrustDataPids.append(pid)
          #sys.exit(0)
       
       #--- end if block
   #--- end for loop
   #sys.exit(0)
   
   #--- Index the the oceanic particles data with the timestamp
   vtuPData[dataTime]= relevantOCrustData

   print(" done with file: "+vtuPFile+"\n")
   
   #dataTime= vtuPData[vtuPFileName].GetPointData().GetArray("TIME")
   #dataTime= vtuPData[vtuPFileName].GetFieldData().GetArray("TIME").GetTuple(

#--- End for loop on VTU files

csvFile= open(csvFileOut,"w")

csvFile.write("time(years),particle id,concentration,Pressure(GPA),Temperature(K),Temperature(C),Depth(m)\n")

print("vtuPData keys="+str(tuple(vtuPData.keys())))

for dataTime in tuple(vtuPData.keys()):

   print("dataTime="+str(dataTime))
   
   vtuPDataT= vtuPData[dataTime]

   #print("vtuPDataT keys="+str(tuple(vtuPDataT.keys())))
   
   for pid in tuple(vtuPDataT.keys()):

      vtuPDataTPid= vtuPDataT[pid]
      
      csvFile.write(str(dataTime)+","+str(pid)+","+str(vtuPDataTPid["concentration"])+","+
                    str(vtuPDataTPid["Pressure(GPa)"])+","+str(vtuPDataTPid["Temperature(C)"])+","+
                    str(vtuPDataTPid["Temperature(K)"])+","+str(vtuPDataTPid["Depth(m)"])+"\n")
   #sys.exit(0)
   
#---
#sys.exit(0)



