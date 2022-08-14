#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
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
# that have a concentration > 0.75
ocCrtThr= 0.75

gridYMeters= 700e3

mrkXRange= [ 550e3, 760e3]
mrkYRange= [ gridYMeters - 3500, gridYMeters ]

#--- Only tracking the oceanic crust markers that have their initial position
#    inside the mrkXRange and the mrkYRange.

#--- 
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

   #--- particles position data for the timestamp
   pPos= dataTmp.GetPointData().GetArray("position")

   #--- Initial position of the particles
   #   (NOTE: could be read just once outside of the loop using the 1st file)
   ipPosData= dataTmp.GetPointData().GetArray("initial position")
   
   #--- Extract oceanic crust particles data:
   #ocCrustData= dataTmp.GetPointData().GetArray("oceanicCrust")
   ocCrustData= dataTmp.GetPointData().GetArray("initial oceanicCrust")
   
   #--- Extract particle Pressure data:
   pPData= dataTmp.GetPointData().GetArray("p")
   
   #--- Extract particles Temperature data:
   pTData= dataTmp.GetPointData().GetArray("T")
   
   relevantOCrustData= {}
   
   for pid in range(pidDataSize):

       #ipPos= ipPosData.GetTuple(pid)

       #print("ipPos="+str(ipPos))
       #print("mrkXRange="+str(mrkXRange))
       #print("mrkYRange="+str(mrkYRange))
       #sys.exit(0)

       #if not (mrkXRange[0] <= ipPos[0] and ipPos[0] <= mrkXRange[1] \
       #         and mrkYRange[1] <= ipPos[1] and ipPos[1] <= mrkYRange[1]):
       #   #print("initial position:"+str(ipPos)+" outside of X,Y ranges")
       #   #sys.exit(0)
       #   continue

       #print("valid initial position:"+str(ipPos)+" inside the X,Y ranges")
       #sys.exit(0)
       
       ocpCrt= ocCrustData.GetTuple(pid)[0]
       ocpP= pPData.GetTuple(pid)[0]
       ocpT= pTData.GetTuple(pid)[0]

       #depth= gridYMeters - ocpPos[1]
       
       if ocpCrt >= ocCrtThr and ocpP >= ocPLow and ocpT >= ocTLow: # and depth > 12000.0:
           
          ocpPos= pPos.GetTuple(pid)

          ipPos= ipPosData.GetTuple(pid)

          if not (mrkXRange[0] <= ipPos[0] and ipPos[0] <= mrkXRange[1] \
                and mrkYRange[0] <= ipPos[1] and ipPos[1] <= mrkYRange[1]):
             continue
          
          #print("ocpCrt="+str(ocpCrt))
          print("valid init pos fpr ocpPos="+str(ocpPos)+",pid="+str(pid))
          #print("ocpP="+str(ocpP))
          #print("ocpT="+str(ocpT))
          print("ipPos="+str(ipPos)+"\n")
          #print("mrkXRange="+str(mrkXRange))
          #print("mrkYRange="+str(mrkYRange))
          #sys.exit(0)

          relevantOCrustData[pid]= {
                                     "concentration": ocpCrt,
                                     "Pressure(GPa)": ocpP,
                                     "Temperature(C)": ocpT-273,
                                     "Temperature(K)": ocpT,
                                     "Depth(y[m])": gridYMeters - ocpPos[1],
                                     "Position(x[m])": ocpPos[0]
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
csvStatsFile= open("stats-"+csvFileOut,"w")

csvFile.write("time(years),particle id,concentration,Pressure(GPA),Temperature(C),Temperature(K),Depth(y[m]),Position(x[m])\n")
csvStatsFile.write("time(years),TemperatureAvg(C),PressureAvg(GPA),DepthsAvg(y[m])\n")

print("vtuPData keys="+str(tuple(vtuPData.keys())))

for dataTime in tuple(vtuPData.keys()):

   print("dataTime="+str(dataTime))
   
   vtuPDataT= vtuPData[dataTime]

   #print("vtuPDataT keys="+str(tuple(vtuPDataT.keys())))

   TCAvgList= []
   PGAvgList= []
   DepthsAvgList= []
   
   for pid in tuple(vtuPDataT.keys()):

      vtuPDataTPid= vtuPDataT[pid]
      
      csvFile.write(str(dataTime)+","+str(pid)+","+str(vtuPDataTPid["concentration"])+","+
                    str(vtuPDataTPid["Pressure(GPa)"])+","+str(vtuPDataTPid["Temperature(C)"])+","+
                    str(vtuPDataTPid["Temperature(K)"])+","+str(vtuPDataTPid["Depth(y[m])"])+","+str(vtuPDataTPid["Position(x[m])"])+"\n")

      TCAvgList.append(vtuPDataTPid["Temperature(C)"])
      PGAvgList.append(vtuPDataTPid["Pressure(GPa)"])
      DepthsAvgList.append(vtuPDataTPid["Depth(y[m])"])
   # ---

   #print("TCAvgList[0:2]="+str(TCAvgList[0:2]))

   if len( TCAvgList) != 0 :
   
      #TCAvgNp= np.array(TCAvgList, dtype=np.float64)
      #PGAvgNp= np.array(PGAvgList, dtype=np.float64)
      #print("shape TCAvgNp="+str(TCAvgNp))
   
      TCAvg= np.mean(np.array(TCAvgList, dtype=np.float64))
      PGAvg= np.mean(np.array(PGAvgList, dtype=np.float64))
      DepthsAvg= np.mean(np.array(DepthsAvgList, dtype=np.float64))
      
     #print("TCAvg="+str(TCAvg))
     #print("PGAvg="+str(PGAvg))

      csvStatsFile.write(str(dataTime)+","+str(TCAvg)+","+str(PGAvg)+","+str(DepthsAvg)+"\n")
      #sys.exit(0)
   #--- end if   
#--- end for dataTime in tuple(vtuPData.keys()): loop

#sys.exit(0)
csvFile.close()
csvStatsFile.close()
