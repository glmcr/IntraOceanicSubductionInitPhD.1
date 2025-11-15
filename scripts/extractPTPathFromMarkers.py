#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import json
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy #thats what you need 

# -- VTU file with which the initial positions of the metam material(s)
#    are intialized to go backward in time. This vtu file is not necessarily
#    the final one.
#vtuParticlesInitFile= sys.argv[1]

# directory where the VTU particles files are located
vtuParticlesDir = sys.argv[1]
metamGroupInfoFile= sys.argv[2]
#csvFileOut= sys.argv[4]
minCompoValue= float(sys.argv[3])
csvFileOut= sys.argv[4]

#protolithCompoName="lusi oceanicCrustMRB"

# --- Get the metam. mats. info from the metamGroupInfoFile
metamGroupInfoFileP= open(metamGroupInfoFile,"r")
metamGroupInfoDict= json.load(metamGroupInfoFileP)
metamGroupInfoFileP.close()

print("metamGroupInfoDict="+str(metamGroupInfoDict))

#print("Debug exit 0")   
#sys.exit(0)

vtuPFiles= sorted(glob.glob(vtuParticlesDir + "/*.vtu")) #,  reverse= True)

# --- Remove the file that will be used for initialization from the other vtu files list
#if vtuParticlesInitFile in vtuPFiles:
#   vtuPFiles.remove(vtuParticlesInitFile)

vtuMetamData= {}
markersTrackerDict= {}
lusiPid= 0

lastFile= vtuPFiles[-1]

print("Reading last file -> "+lastFile+" to init the markers tracking with their final positions")

reader= vtk.vtkXMLUnstructuredGridReader()
   
reader.SetFileName(lastFile)
reader.Update()

#--- Extract all the particles data
dataTmpEnd= reader.GetOutput()
   
#--- Extract the timestamp (in years) as an int for this VTU file
dataTimeEnd= int( dataTmpEnd.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

print("dataTimeEnd="+str(dataTimeEnd))

pidDataEnd= dataTmpEnd.GetPointData().GetArray("id")
pidDataSizeEnd= pidDataEnd.GetSize()
print("pidDataEnd size="+str(pidDataSizeEnd)+"\n")

#--- particles initial position data for the timestamp
initPosDataEnd= dataTmpEnd.GetPointData().GetArray("initial position")

#--- particles position data for the timestamp
pPosDataEnd= dataTmpEnd.GetPointData().GetArray("position")

#--- Extract particle Pressure data:
pPDataEnd= dataTmpEnd.GetPointData().GetArray("p")
   
#--- Extract particles Temperature data:
pTDataEnd= dataTmpEnd.GetPointData().GetArray("T")

protoPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicCrustMRB")

ocSedPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicSeds")

#initCompo= dataTmp.GetPointData().GetArray("initial composition")

#validPids= []

vtuMetamData= {}
vtuMetamPidPT= {}

for metamMatName in metamGroupInfoDict:

   print("metamMatName="+metamMatName)
   
   vtuMetamData[metamMatName]= dataTmpEnd.GetPointData().GetArray(metamMatName)
   vtuMetamPidPT[metamMatName]= {}

   for groupId in metamGroupInfoDict[metamMatName]:
      vtuMetamPidPT[metamMatName][groupId]= {}
   # ---
# ---

initPosTrackingList= []

for pidIter in range(0,pidDataSizeEnd):

    pidPos= pPosDataEnd.GetTuple(pidIter)
     
    for metamMatName in vtuMetamPidPT:

        # --- Compo for the metam. mat. at the pid position
        metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]
       
        for groupId in vtuMetamPidPT[metamMatName]:

            groupIdDict= metamGroupInfoDict[metamMatName][groupId]
           
            if pidPos[0] > groupIdDict["x1"] and pidPos[1] < groupIdDict["y1"] \
               and pidPos[0] < groupIdDict["x2"] and pidPos[1] > groupIdDict["y2"]:
       
               if metamMatCrt > minCompoValue:

                  initialPos= initPosDataEnd.GetTuple(pidIter)

                  #print("initialPos="+str(initialPos))
                  #print("Debug exit 0")   
                  #sys.exit(0)

                  aspectPid= int(pidDataEnd.GetTuple(pidIter)[0])

                  initialPosIdStr= "{:12.7f}".format(initialPos[0])+","+"{:12.7f}".format(initialPos[1])+":"+str(aspectPid)

                  #duplicateInitialPos= False
                  
                  if initialPosIdStr in vtuMetamPidPT[metamMatName][groupId]: #initPosTrackingList:

                     #vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTimeEnd].append({
                     #      "Pressure(Gpa)": pPDataEnd.GetTuple(pidIter)[0],
                     #      "Temperature(K)": pTDataEnd.GetTuple(pidIter)[0],
                     #      "metamCompo(%)": metamMatCrt,
                     #      "protoCompo(%)": protoPDataEnd.GetTuple(pidIter)[0],
                     #      "ocSedsCompo(%)": ocSedPDataEnd.GetTuple(pidIter)[0],
                     #      "PidPos": pidPos #,
                     #      #"pidIter": pidIter
                     #      #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                     #      #"duplicateInitialPos": None
                     #})

                     print("\nFound a duplicate for "+groupId+" at pidIter="+str(pidIter)+
                           " at time end -> "+str(dataTimeEnd)+" with initial pos + id item -> \n"+initialPosIdStr+"->"+
                           str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTimeEnd]))

                     del vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]
                     initPosTrackingList.remove(initialPosIdStr)
                     #print("Debug exit 0")   
                     #sys.exit(0)
                     
                  else:

                  #aspectPid= int(pidData.GetTuple(pidIter)[0])

                     initPosTrackingList.append(initialPosIdStr)
                     
                     vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]= { # [dataTimeEnd]= 
                        #dataTimeEnd: [{
                        dataTimeEnd: {
                        
                           "Pressure(Gpa)": pPDataEnd.GetTuple(pidIter)[0],
                           "Temperature(K)": pTDataEnd.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "protoCompo(%)": protoPDataEnd.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedPDataEnd.GetTuple(pidIter)[0],
                           "PidPos": pidPos #,
                           #"pidIter": pidIter
                           #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                           #"duplicateInitialPos": None
                        }
                        #}]
                     }

                  # ---

                  #if initialPosStr not in initPosTrackingList:
                  #   initPosTrackingList.append(initialPosStr)

                  #print("initialPosStr="+initialPosStr)
                  #print("vtuMetamPidPT[metamMatName][groupId][initialPosStr]="+str(vtuMetamPidPT[metamMatName][groupId][initialPosStr]))
                  #print("Debug exit 0")   
                  #sys.exit(0)                 
                  
                # ---
            # ---
        # ---          
   # ---
# ---

del reader

print("at end: len(initPosTrackingList)="+str(len(initPosTrackingList)))

#for metamMatName in vtuMetamPidPT:
#  for groupId in vtuMetamPidPT[metamMatName]:
#      for initialPosStr in vtuMetamPidPT[metamMatName][groupId]:
#         if len(vtuMetamPidPT[metamMatName][groupId][initialPosStr][dataTimeEnd]) > 1: 
#           initPosTrackingList.remove(initialPosStr)
# ---
#print("without duplicates: len(initPosTrackingList)="+str(len(initPosTrackingList)))

for metamMatName in vtuMetamPidPT:
   for groupId in vtuMetamPidPT[metamMatName]:
       print("Got "+str(len(vtuMetamPidPT[metamMatName][groupId]))+
             " markers extracted at dataTimeEnd for group "+groupId+" of "+metamMatName)
   # ---
# ---

#print("Debug exit 0")   
#sys.exit(0)

reader= vtk.vtkXMLUnstructuredGridReader()

firstFile= vtuPFiles[0]

print("Reading first file -> "+firstFile+" to init the markers tracking in the past")

reader.SetFileName(firstFile)
reader.Update()

#--- Extract all the particles data
dataTmpStart= reader.GetOutput()

#--- Extract the timestamp (in years) as an int for this VTU file
dataTimeStart= int( dataTmpStart.GetFieldData().GetArray("TIME").GetTuple(0)[0] )
print("dataTimeStart="+str(dataTimeStart))

pidDataStart= dataTmpStart.GetPointData().GetArray("id")
pidDataSizeStart= pidDataStart.GetSize()
print("pidDataStart size="+str(pidDataSizeStart)+"\n")

#--- particles initial position data for the timestamp
initPosDataStart= dataTmpStart.GetPointData().GetArray("initial position")

#--- particles position data for the timestamp
pPosDataStart= dataTmpStart.GetPointData().GetArray("position")

#--- Extract particle Pressure data:
pPDataStart= dataTmpStart.GetPointData().GetArray("p")
   
#--- Extract particles Temperature data:
pTDataStart= dataTmpStart.GetPointData().GetArray("T")

protoPDataStart= dataTmpStart.GetPointData().GetArray("lusi oceanicCrustMRB")

ocSedPDataStart= dataTmpStart.GetPointData().GetArray("lusi oceanicSeds")

for metamMatName in metamGroupInfoDict:
   #print("metamMatName="+metamMatName)
   vtuMetamData[metamMatName]= dataTmpStart.GetPointData().GetArray(metamMatName)

for pidIter in range(0,pidDataSizeStart):

    initialPos= initPosDataStart.GetTuple(pidIter)
    aspectPid= int(pidDataStart.GetTuple(pidIter)[0])

    initialPosIdStr= "{:12.7f}".format(initialPos[0])+","+"{:12.7f}".format(initialPos[1])+":"+str(aspectPid)

    #protolithCrt= protoPDataStart.GetTuple(pidIter)[0]
    #aspectPid= pidData.GetTuple(pidIter)[0]
    #ocSedCrt= ocSedPDataStart.GetTuple(pidIter)[0]

    if initialPosIdStr in initPosTrackingList:  #and protolithCrt > minCompoValue :

       #pidPos= pPosDataStart.GetTuple(pidIter)
       #aspectPid= int(pidData.GetTuple(pidIter)[0])
       #Pressure= pPDataStart.GetTuple(pidIter)[0]
       #Temp= pTDataStart.GetTuple(pidIter)[0]
       #protolithCrt= protoPDataStart.GetTuple(pidIter)[0]
       #aspectPid= pidData.GetTuple(pidIter)[0]
       #ocSedCrt= ocSedPDataStart.GetTuple(pidIter)[0]       

       for metamMatName in vtuMetamPidPT:

          vtuMetamData[metamMatName]= dataTmpStart.GetPointData().GetArray(metamMatName)
          
          for groupId in vtuMetamPidPT[metamMatName]:

              if initialPosIdStr in vtuMetamPidPT[metamMatName][groupId] and \
                 dataTimeEnd in vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]:

                 if dataTimeStart in vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]:

                    #vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTimeStart].append({
                    #       "Pressure(Gpa)": pPDataStart.GetTuple(pidIter)[0],
                    #       "Temperature(K)": pTDataStart.GetTuple(pidIter)[0],
                    #       "metamCompo(%)": metamMatCrt,
                    #       "protoCompo(%)": protoPDataStart.GetTuple(pidIter)[0],
                    #       "ocSedsCompo(%)": ocSedPDataStart.GetTuple(pidIter)[0],
                    #       "PidPos": pPosDataStart.GetTuple(pidIter)
                    #})

                    print("\nFound a duplicate for "+groupId+" at pidIter="+str(pidIter)+
                          " at time start -> "+str(dataTimeStart)+" with initial pos + id item -> \n"+initialPosIdStr+"->"+
                           str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTimeStart]))

                    del vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]
                    initPosTrackingList.remove(initialPosIdStr)
                    #print("item at initialPosIdStr:"+str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))
                    #print("Debug exit 0")
                    #sys.exit(0)                   
                    
                 else:

                   vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTimeStart]= {
                         #dataTimeStart: [{
                         #dataTimeStart: {
                         #{
                           "Pressure(Gpa)": pPDataStart.GetTuple(pidIter)[0],
                           "Temperature(K)": pTDataStart.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "protoCompo(%)": protoPDataStart.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedPDataStart.GetTuple(pidIter)[0],
                           "PidPos": pPosDataStart.GetTuple(pidIter)
                           #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                           #"duplicateInitialPos": None
                        }
                        #}]
                   #})

                   print("\ntime start match for group:"+groupId+",item="+str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))
                   #print("Debug exit 0")
                   #sys.exit(0)   
 
                 #checkPid= vtuMetamPidPT[metamMatName][groupId].split(":")[1]
                 #if aspectPid == checkPid:
                 #   print("\nFound matching initialPosIdStr -> "+initialPosIdStr)
                 #   print("protolithCrt="+str(protolithCrt))
                 #   print("ocSedCrt="+str(ocSedCrt))        
                 #   print("Pressure="+str(Pressure))
                 #   print("Temp="+str(Temp))
                 #   print("pidPos="+str(pidPos))
                 #   print("aspectPid="+str(aspectPid))
                 #   print("metamMatName="+metamMatName+", groupId="+groupId)
                 #   print("vtuMetamPidPT[metamMatName][groupId][initialIdPosStr]="+
                 #         str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))
                    #print("Debug exit 0")
                    #sys.exit(0)
              #---
          # ---
       # ---
       #print("Debug exit 0")
       #sys.exit(0)
    # ---
# ---

print("at time start: len(initPosTrackingList)="+str(len(initPosTrackingList)))

for metamMatName in vtuMetamPidPT:
   for groupId in vtuMetamPidPT[metamMatName]:
       print("Got "+str(len(vtuMetamPidPT[metamMatName][groupId]))+
             " markers extracted at dataTimeStart for group "+groupId+" of "+metamMatName)
   # ---
# ---

print("Debug exit 0")
sys.exit(0)

del reader

# --- Iterate on all the other vtu files not yet processed. 
for vtuPFile in vtuPFiles[1:-1]:

   print("Reading VTU file -> "+vtuPFile) 
   
   reader= vtk.vtkXMLUnstructuredGridReader()
   
   reader.SetFileName(vtuPFile)
   reader.Update()

   #--- Extract all the particles data
   dataTmp= reader.GetOutput()

   #--- Extract the timestamp (in years) as an int for this VTU file
   dataTime= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )
   print("dataTime="+str(dataTime))

   pidData= dataTmp.GetPointData().GetArray("id")
   pidDataSize= pidData.GetSize()
   print("pidData size="+str(pidDataSize)+"\n")

   #--- particles initial position data for the timestamp
   initPosData= dataTmp.GetPointData().GetArray("initial position")

   #--- particles position data for the timestamp
   pPosData= dataTmp.GetPointData().GetArray("position")

   #--- Extract particle Pressure data:
   pPData= dataTmp.GetPointData().GetArray("p")
   
   #--- Extract particles Temperature data:
   pTData= dataTmp.GetPointData().GetArray("T")

   protoPData= dataTmp.GetPointData().GetArray("lusi oceanicCrustMRB")

   ocSedPData= dataTmp.GetPointData().GetArray("lusi oceanicSeds")

   for metamMatName in metamGroupInfoDict:
   #print("metamMatName="+metamMatName)
      vtuMetamData[metamMatName]= dataTmp.GetPointData().GetArray(metamMatName)   

   for pidIter in range(0,pidDataSize):

     initialPos= initPosData.GetTuple(pidIter)
     aspectPid= int(pidData.GetTuple(pidIter)[0])

     initialPosIdStr= "{:12.7f}".format(initialPos[0])+","+"{:12.7f}".format(initialPos[1])+":"+str(aspectPid)

     #protolithCrt= protoPData.GetTuple(pidIter)[0]
     #ocSedCrt= ocSedPData.GetTuple(pidIter)[0]

     if initialPosIdStr in initPosTrackingList:  #and protolithCrt > minCompoValue :

       #pidPos= pPosData.GetTuple(pidIter)
       #Pressure= pPDataStart.GetTuple(pidIter)[0]
       #Temp= pTDataStart.GetTuple(pidIter)[0]

       for metamMatName in vtuMetamPidPT:
          for groupId in vtuMetamPidPT[metamMatName]:

              if initialPosIdStr in vtuMetamPidPT[metamMatName][groupId]:

                 if dataTime in vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]:

                    vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTime].append({
                           "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
                           "Temperature(K)": pTData.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "protoCompo(%)": protoPData.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedPData.GetTuple(pidIter)[0],
                           "PidPos": pPosData.GetTuple(pidIter)
                    })

                 else:

                   vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]= {
                         dataTime: [{
                           "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
                           "Temperature(K)": pTData.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "protoCompo(%)": protoPData.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedPData.GetTuple(pidIter)[0],
                           "PidPos": pPosData.GetTuple(pidIter)
                           #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                           #"duplicateInitialPos": None
                         }]
                  }
       # ---            
     # ---
   # ---

   print("Done with reading VTU file -> "+vtuPFile) 
   
   del reader
# ---

print("Debug exit 0")
sys.exit(0)

csvFile= open(csvFileOut,"w")
csvStatsFile= open("stats-"+csvFileOut,"w")

csvFile.write("time(years),particle id,concentration,Pressure(GPA),Temperature(C),Temperature(K),Depth(y[m]),Position(x[m])\n")
csvStatsFile.write("time(years),TemperatureAvg(C),PressureAvg(GPA),DepthsAvg(y[m]),DepthsMin(y[m]),DepthsMax(y[m])\n")

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

      DepthsNp= np.array(DepthsAvgList, dtype=np.float64)
      
      DepthsAvg= np.mean(DepthsNp)

      DepthsMin= np.min(DepthsNp)
      DepthsMax= np.max(DepthsNp)
      
     #print("TCAvg="+str(TCAvg))
     #print("PGAvg="+str(PGAvg))

      csvStatsFile.write(str(dataTime)+","+str(TCAvg)+","+str(PGAvg)+","+str(DepthsAvg)+","+str(DepthsMin)+","+str(DepthsMax)+"\n")
      #sys.exit(0)
   #--- end if   
#--- end for dataTime in tuple(vtuPData.keys()): loop

#sys.exit(0)
csvFile.close()
csvStatsFile.close()
 
