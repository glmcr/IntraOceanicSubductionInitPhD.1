#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import json
import numpy as np
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

#print("metamGroupInfoDict="+str(metamGroupInfoDict))

#print("Debug exit 0")   
#sys.exit(0)

vtuPFiles= sorted(glob.glob(particlesDir + "/*.vtu"))
h5PFiles= sorted(glob.glob(particlesDir + "/*.h5")) #,  reverse= True)

# --- Remove the file that will be used for initialization from the other vtu files list
#if vtuParticlesInitFile in vtuPFiles:
#   vtuPFiles.remove(vtuParticlesInitFile)

h5MetamData= {}
markersTrackerDict= {}
lusiPid= 0

lastVTUFile= vtuPFiles[-1]

print("Reading last vtu file -> "+lastVTUFile+" to init the markers tracking with their final time")

reader= vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(lastVTUFile)
reader.Update()

#--- Extract all the particles data
dataTmpEnd= reader.GetOutput()
   
#--- Extract the timestamp (in years) as an int for this VTU file
dataTimeEnd= int( dataTmpEnd.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

print("dataTimeEnd="+str(dataTimeEnd))

# --- now h5 data
lastH5Data= h5py.File(h5PFiles[-1],"r")

#pidDataEnd= dataTmpEnd.GetPointData().GetArray("id")
#pidDataSizeEnd= pidDataEnd.GetSize()
pidDataEnd= lastH5Data["id"]
pidDataSizeEnd= pidDataEnd.shape[0]
print("pidDataEnd size="+str(pidDataSizeEnd)+"\n")
#sys.exit(0)

#--- particles initial position data for the timestamp
#initPosDataEnd= dataTmpEnd.GetPointData().GetArray("initial position")
initPosDataEnd= lastH5Data["initial position"]

#--- particles position data for the timestamp
#pPosDataEnd= dataTmpEnd.GetPointData().GetArray("position")
pPosDataEnd= lastH5Data["position"]

#--- Extract particle Pressure data:
#pPDataEnd= dataTmpEnd.GetPointData().GetArray("p")
pPDataEnd= lastH5Data["p"]
   
#--- Extract particles Temperature [K] data:
#pTDataEnd= dataTmpEnd.GetPointData().GetArray("T")
pTDataEnd= lastH5Data["T"]

#protoPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicCrustMRB")
protoPDataEnd= lastH5Data["lusi oceanicCrustMRB"]

#ocSedPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicSeds")
ocSedPDataEnd= lastH5Data["lusi oceanicSeds"]

#initCompo= dataTmp.GetPointData().GetArray("initial composition")
#validPids= []

#metamMatOthers= ("lusi greenschists", "lusi amphibolites", "lusi blueschists", "lusi eclogites")
#vtuMetamOthersData= {}
#for metamMatOther in metamMatOthers:
#    vtuMetamOthersData[metamMatOther]= dataTmpEnd.GetPointData().GetArray(metamMatOther)

h5MetamData= {}
h5MetamPidPT= {}

metamGroupInfoDict= { "lusi granulites", "lusi greenschists", "lusi amphibolites", "lusi blueschists", "lusi eclogites" }

for metamMatName in metamGroupInfoDict:

   print("metamMatName="+metamMatName)
   
   #vtuMetamData[metamMatName]= dataTmpEnd.GetPointData().GetArray(metamMatName)
   #vtuMetamPidPT[metamMatName]= {}

   h5MetamData[metamMatName]= lastH5Data[metamMatName]
   h5MetamPidPT[metamMatName]= {} 

   #for groupId in metamGroupInfoDict[metamMatName]:
   #   #vtuMetamPidPT[metamMatName][groupId]= {}
   #   h5MetamPidPT[metamMatName][groupId]= {}
   # ---
# ---

#greenschistsPData= dataTmpEnd.GetPointData().GetArray("lusi greenschists")
#amphibolitesPData= dataTmpEnd.GetPointData().GetArray("lusi amphibolites")

initPosTrackingList= []

for pidIter in range(0,pidDataSizeEnd):

    #pidPos= pPosDataEnd.GetTuple(pidIter)
    pidPos= pPosDataEnd[pidIter]
    
    for metamMatName in vtuMetamPidPT:

        # --- Compo for the metam. mat. at the pid position
        #metamMatCrt= h5MetamData[metamMatName].GetTuple(pidIter)[0]
        metamMatCrt= h5MetamData[metamMatName][pidIter,0] 
       
        #for groupId in h5MetamPidPT[metamMatName]:
        #    groupIdDict= metamGroupInfoDict[metamMatName][groupId]          
        #    if pidPos[0] > groupIdDict["x1"] and pidPos[1] < groupIdDict["y1"] \
        #       and pidPos[0] < groupIdDict["x2"] and pidPos[1] > groupIdDict["y2"]:
        #       if metamMatCrt > minCompoValue:
        #
        #          initialPos= initPosDataEnd.GetTuple(pidIter)
        #          #print("initialPos="+str(initialPos))
        #          #print("Debug exit 0")   
        #          #sys.exit(0)
        #
        #          aspectPid= int(pidDataEnd.GetTuple(pidIter)[0])
         initialPosIdStr= "{:12.7f}".format(initialPos[0])+"_"+"{:12.7f}".format(initialPos[1])+"_"+str(aspectPid)

                  #duplicateInitialPos= False
                  
                  if initialPosIdStr in vtuMetamPidPT[metamMatName][groupId]: # and \
                     #dataTimeEnd in vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]:

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
                     
                     vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]= {
                        dataTimeEnd: {
                        
                           "Pressure(Pa)": pPDataEnd.GetTuple(pidIter)[0],
                           "Temperature(K)": pTDataEnd.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "greenschists(%)": greenschistsPData.GetTuple(pidIter)[0],
                           "amphibolites(%)": amphibolitesPData.GetTuple(pidIter)[0],
                           "protoCompo(%)": protoPDataEnd.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedPDataEnd.GetTuple(pidIter)[0],
                           "PidPos": pidPos #,
                           #"pidIter": pidIter
                           #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                           #"duplicateInitialPos": None
                        }
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

       #for initialPosIdStr in vtuMetamPidPT[metamMatName][groupId]:
       #   print("initialPosIdStr="+initialPosIdStr+
       #         ", vtuMetamPidPT[metamMatName][groupId][initialPosIdStr].keys()="+
       #         str(tuple(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr].keys())))
       #   #print("Debug exit 0")   
       #   #sys.exit(0)
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

greenschistsPData= dataTmpStart.GetPointData().GetArray("lusi greenschists")
amphibolitesPData= dataTmpStart.GetPointData().GetArray("lusi amphibolites")

for metamMatName in metamGroupInfoDict:
   #print("metamMatName="+metamMatName)
   vtuMetamData[metamMatName]= dataTmpStart.GetPointData().GetArray(metamMatName)

for pidIter in range(0,pidDataSizeStart):

    initialPos= initPosDataStart.GetTuple(pidIter)
    aspectPid= int(pidDataStart.GetTuple(pidIter)[0])

    initialPosIdStr= "{:12.7f}".format(initialPos[0])+"_"+"{:12.7f}".format(initialPos[1])+"_"+str(aspectPid)

    #protolithCrt= protoPDataStart.GetTuple(pidIter)[0]
    #aspectPid= pidData.GetTuple(pidIter)[0]
    #ocSedCrt= ocSedPDataStart.GetTuple(pidIter)[0]

    if initialPosIdStr in initPosTrackingList:  #and protolithCrt > minCompoValue :

       #pidPos= pPosDataStart.GetTuple(pidIter)
       #aspectPid= int(pidData.GetTuple(pidIter)[0])
       #Pressure= pPDataStart.GetTuple(pidIter)[0]
       #Temp= pTDataStart.GetTuple(pidIter)[0]
       protolithCrt= protoPDataStart.GetTuple(pidIter)[0]
       #aspectPid= pidData.GetTuple(pidIter)[0]
       ocSedCrt= ocSedPDataStart.GetTuple(pidIter)[0]       

       for metamMatName in vtuMetamPidPT:

          #vtuMetamData[metamMatName]= dataTmpStart.GetPointData().GetArray(metamMatName)
          metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]
          
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

                   #if (metamMatCrt + protolithCrt + ocSedCrt) > minCompoValue:

                     vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTimeStart]= {
                           "Pressure(Pa)": pPDataStart.GetTuple(pidIter)[0],
                           "Temperature(K)": pTDataStart.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "greenschists(%)": greenschistsPData.GetTuple(pidIter)[0],
                           "amphibolites(%)": amphibolitesPData.GetTuple(pidIter)[0],                       
                           "protoCompo(%)": protolithCrt, #protoPDataStart.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedCrt,   #ocSedPDataStart.GetTuple(pidIter)[0],
                           "PidPos": pPosDataStart.GetTuple(pidIter)
                           #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                           #"duplicateInitialPos": None
                        }

                     print("\ntime start match for group:"+groupId+",item="+str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))
                     #print("Debug exit 0")
                     #sys.exit(0)   
                 # ---
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

       #for initialPosIdStr in vtuMetamPidPT[metamMatName][groupId]:
       #   print("initialPosIdStr="+initialPosIdStr+
       #         ", vtuMetamPidPT[metamMatName][groupId][initialPosIdStr].keys()="+
       #         str(tuple(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr].keys())))
       #   #print("Debug exit 0")   
       #   #sys.exit(0)       
   # ---
# ---

#print("Debug exit 0")
#sys.exit(0)

del reader

# --- Iterate on all the other vtu files not yet processed. 
for vtuPFile in vtuPFiles[1:-1]: #vtuPFiles[1:2]: #vtuPFiles[1:-1]:

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

   greenschistsPData= dataTmp.GetPointData().GetArray("lusi greenschists")
   amphibolitesPData= dataTmp.GetPointData().GetArray("lusi amphibolites")   

   for metamMatName in metamGroupInfoDict:
   #print("metamMatName="+metamMatName)
      vtuMetamData[metamMatName]= dataTmp.GetPointData().GetArray(metamMatName)
   # --

   for pidIter in range(0,pidDataSize):

     initialPos= initPosData.GetTuple(pidIter)
     aspectPid= int(pidData.GetTuple(pidIter)[0])

     initialPosIdStr= "{:12.7f}".format(initialPos[0])+"_"+"{:12.7f}".format(initialPos[1])+"_"+str(aspectPid)

     protolithCrt= protoPData.GetTuple(pidIter)[0]
     ocSedCrt= ocSedPData.GetTuple(pidIter)[0]

     if initialPosIdStr in initPosTrackingList:  #and protolithCrt > minCompoValue :

       #pidPos= pPosData.GetTuple(pidIter)
       #Pressure= pPDataStart.GetTuple(pidIter)[0]
       #Temp= pTDataStart.GetTuple(pidIter)[0]

       for metamMatName in vtuMetamPidPT:

          metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]
          
          for groupId in vtuMetamPidPT[metamMatName]:

              if initialPosIdStr in vtuMetamPidPT[metamMatName][groupId] and \
                 dataTimeEnd in vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]:

                 if dataTime in vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]:
                    
                    print("\nFound a duplicate for "+groupId+" at pidIter="+str(pidIter)+
                          " at time -> "+str(dataTime)+" with initial pos + id item -> \n"+initialPosIdStr+"->"+
                           str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTime]))
                    
                    del vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]
                    initPosTrackingList.remove(initialPosIdStr)

                 else:

                   #if (metamMatCrt + protolithCrt + ocSedCrt) > minCompoValue:
                      
                     vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][dataTime]= {
                         #dataTime: [{
                           "Pressure(Pa)": pPData.GetTuple(pidIter)[0],
                           "Temperature(K)": pTData.GetTuple(pidIter)[0],
                           "metamCompo(%)": metamMatCrt,
                           "greenschists(%)": greenschistsPData.GetTuple(pidIter)[0],
                           "amphibolites(%)": amphibolitesPData.GetTuple(pidIter)[0],    
                           "protoCompo(%)": protolithCrt, #protoPData.GetTuple(pidIter)[0],
                           "ocSedsCompo(%)": ocSedCrt , #ocSedPData.GetTuple(pidIter)[0],
                           "PidPos": pPosData.GetTuple(pidIter)
                           #"aspectPid": int(pidData.GetTuple(pidIter)[0]),
                           #"duplicateInitialPos": None
                         #}]
                     }

                     print("\n intermediate time match for group:"+groupId+",item="+str(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))
                 # ---
       # ---            
     # ---
   # ---

   print("Done with reading VTU file -> "+vtuPFile)

   print("at intermediate time : len(initPosTrackingList)="+str(len(initPosTrackingList)))

   for metamMatName in vtuMetamPidPT:
      for groupId in vtuMetamPidPT[metamMatName]:
         print("Got "+str(len(vtuMetamPidPT[metamMatName][groupId]))+
             " markers extracted at intermediate time -> "+str(dataTime)+" for group "+groupId+" of "+metamMatName)
   # ---
# ---   
   
   del reader

   #break
   #print("Debug exit 0")
   #sys.exit(0)
   
# ---

Pa2GPa= 1.0/1e9

for metamMatName in vtuMetamPidPT:

   print("metamMatName:"+metamMatName)
   
   for groupId in sorted(vtuMetamPidPT[metamMatName], reverse=True):

      print("Processing group:"+groupId)
      
      for initialPosIdStr in vtuMetamPidPT[metamMatName][groupId]:

         #sortedTimes= tuple(sorted(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))

         #csvFileOut= csvFilesOuputFolder + os.sep + groupId + "-" +initialPosIdStr.split(":")[0]+".csv"
         csvFileOut= csvFilesOuputFolder + os.sep + groupId + "-" + initialPosIdStr + ".csv"

         print("csvFileOut="+csvFileOut)

         if pathlib.Path(csvFileOut).exists():
            print("Warning: csvFileOut: "+csvFileOut+" already created !!")
            csvFileOut= csvFileOut+"_dup"
         # ---

         sortedTimes= tuple(sorted(vtuMetamPidPT[metamMatName][groupId][initialPosIdStr]))

         print("sortedTimes="+str(sortedTimes))
         
         #print("Debug exit 0")
         #sys.exit(0)
         
         csvFileP= open(csvFileOut,"w")
         
         #csvFileP.write("#time(years),"+metamMatName.split(" ")[1]+"Compo(%),Pressure(GPa),Temperature(C)\n") #,Depth(y[m]),Position(x[m])\n")
         csvFileP.write("#time(years),Temperature(C),Pressure(GPa),"+
                        metamMatName.split(" ")[1]+"Compo(%),greenschists(%),amphibolites(%),ocCrustCompo(%),ocSedsCompo(%)\n") #,Depth(y[m]),Position(x[m])\n")

         #validTimes= 0
         
         for time in sortedTimes:

            print("Processing time:"+str(time))

            metamCompo= vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["metamCompo(%)"]
            ocCrustCompo= vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["protoCompo(%)"]
            ocSedsCompo=  vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["ocSedsCompo(%)"]

            greenschistsCompo= vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["greenschists(%)"]
            amphibolitesCompo=  vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["amphibolites(%)"]
            
            pressurePa= vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["Pressure(Pa)"]
            tempK= vtuMetamPidPT[metamMatName][groupId][initialPosIdStr][time]["Temperature(K)"]

            if (metamCompo + greenschistsCompo + amphibolitesCompo + ocCrustCompo + ocSedsCompo) > minCompoValue:
              #csvFileP.write(str(time)+","+str(metamCompo)+","+str(pressurePa*Pa2GPa)+","+str(tempK-273.0)+"\n")
              csvFileP.write(str(time)+","+str(tempK-273.0)+","+str(pressurePa*Pa2GPa)+","+str(metamCompo)+","
                             +str(greenschistsCompo)+","+str(amphibolitesCompo)+","+str(ocCrustCompo)+","+str(ocSedsCompo)+"\n")

              #validTimes += 1
              
         # ---
         csvFileP.close()

         print("Done with csv file:"+csvFileOut+"\n")

         #print("Debug exit 0")
         #sys.exit(0)
      # ---
      print("Done with processing group:"+groupId)
   # ---
   print("Done with processing metamMatName:"+metamMatName)
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
 
