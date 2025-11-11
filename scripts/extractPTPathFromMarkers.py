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
vtuParticlesInitFile= sys.argv[1]

# directory where the VTU particles files are located
vtuParticlesDir = sys.argv[2]
metamGroupInfoFile= sys.argv[3]
#csvFileOut= sys.argv[4]
minCompoValue= float(sys.argv[4])
csvFileOut= sys.argv[5]

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

print("Reading file -> "+lastFile+" to init the markers tracking")

reader= vtk.vtkXMLUnstructuredGridReader()
   
reader.SetFileName(lastFile)
reader.Update()

#--- Extract all the particles data
dataTmp= reader.GetOutput()
   
#--- Extract the timestamp (in years) as an int for this VTU file
dataTimeEnd= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

pidData= dataTmp.GetPointData().GetArray("id")

print("dataTimeEnd="+str(dataTimeEnd))

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

#validPids= []

vtuMetamData= {}
vtuMetamPidPT= {}

for metamMatName in metamGroupInfoDict:

   print("metamMatName="+metamMatName)
   
   vtuMetamData[metamMatName]= dataTmp.GetPointData().GetArray(metamMatName)
   vtuMetamPidPT[metamMatName]= {}

   for groupId in metamGroupInfoDict[metamMatName]:
      vtuMetamPidPT[metamMatName][groupId]= {}
   # ---
# ---

initPosTrackingList= []

for pidIter in range(0,pidDataSize):

    pidPos= pPosData.GetTuple(pidIter)
     
    for metamMatName in vtuMetamPidPT:

        # --- Compo for the metam. mat. at the pid position
        metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]
       
        for groupId in vtuMetamPidPT[metamMatName]:

            groupIdDict= metamGroupInfoDict[metamMatName][groupId]
           
            if pidPos[0] > groupIdDict["x1"] and pidPos[1] < groupIdDict["y1"] \
               and pidPos[0] < groupIdDict["x2"] and pidPos[1] > groupIdDict["y2"]:
       
               if metamMatCrt > minCompoValue:

                  initialPos= initPosData.GetTuple(pidIter)

                  #print("initialPos="+str(initialPos))
                  #print("Debug exit 0")   
                  #sys.exit(0)

                  initialPosStr= "{:12.7f}".format(initialPos[0])+","+"{:12.7f}".format(initialPos[1])
                  
                  vtuMetamPidPT[metamMatName][groupId][initialPosStr]= {
                     "Time": dataTimeEnd,
                     "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
                     "Temperature(K)": pTData.GetTuple(pidIter)[0],
                     "metamCompo(%)": metamMatCrt,
                     "protoCompo(%)": protoPData.GetTuple(pidIter)[0],
                     "ocSedsCompo(%)": ocSedPData.GetTuple(pidIter)[0],
                     "PidPos": pidPos,
                     "aspectPid": int(pidData.GetTuple(pidIter)[0])
                  }

                  initPosTrackingList.append(initialPosStr)

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

for metamMatName in vtuMetamPidPT:
   for groupId in vtuMetamPidPT[metamMatName]:
       print("Got "+str(len(vtuMetamPidPT[metamMatName][groupId]))+
             " markers extracted for group "+groupId+" of "+metamMatName)
   # ---
# ---

reader= vtk.vtkXMLUnstructuredGridReader()

firstFile= vtuPFiles[0]
   
reader.SetFileName(firstFile)
reader.Update()

#--- Extract all the particles data
dataTmp= reader.GetOutput()

#--- Extract the timestamp (in years) as an int for this VTU file
dataTimeStart= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

pidData= dataTmp.GetPointData().GetArray("id")

print("dataTimeStart="+str(dataTimeStart))

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

for pidIter in range(0,pidDataSize):

    initialPos= initPosData.GetTuple(pidIter)

    initialPosStr= "{:12.7f}".format(initialPos[0])+","+"{:12.7f}".format(initialPos[1])

    protolithCrt= protoPData.GetTuple(pidIter)[0]
    #aspectPid= pidData.GetTuple(pidIter)[0]
    ocSedCrt= ocSedPData.GetTuple(pidIter)[0]

    if initialPosStr in initPosTrackingList and protolithCrt > minCompoValue :

       pidPos= pPosData.GetTuple(pidIter)
       aspectPid= int(pidData.GetTuple(pidIter)[0])
       Pressure= pPData.GetTuple(pidIter)[0]
       Temp= pTData.GetTuple(pidIter)[0]

       for metamMatName in vtuMetamPidPT:
          for groupId in vtuMetamPidPT[metamMatName]:

              if initialPosStr in vtuMetamPidPT[metamMatName][groupId]:

                 checkPid= vtuMetamPidPT[metamMatName][groupId][initialPosStr]["aspectPid"]

                 if aspectPid == checkPid:
                    print("\nFound matching initialPosStr -> "+initialPosStr)
                    print("protolithCrt="+str(protolithCrt))
                    print("ocSedCrt="+str(ocSedCrt))        
                    print("Pressure="+str(Pressure))
                    print("Temp="+str(Temp))
                    print("pidPos="+str(pidPos))
                    print("aspectPid="+str(aspectPid))
                    print("metamMatName="+metamMatName+", groupId="+groupId)
                    print("vtuMetamPidPT[metamMatName][groupId][initialPosStr]="+
                          str(vtuMetamPidPT[metamMatName][groupId][initialPosStr]))
              #---
          # ---
       # ---
       #print("Debug exit 0")
       #sys.exit(0)
    # ---
# ---

del reader

print("Debug exit 0")
sys.exit(0)

#markersTrackerDictKeys= tuple(markersTrackerDict.keys())
#print("\ntentative nb. of tracked markers="+str(len(markersTrackerDictKeys)))
#for lusiPid in markersTrackerDictKeys:
#    checkPid= markersTrackerDict[lusiPid][dataTime0]["aspectPid"]
#    if checkPid not in validPids:
#       validPids.append(checkPid)
#       #print("len(validPids)="+str(len(validPids)))
#    else:
#       #print("WARNING: duplicate pid -> "+str(checkPid)+" cannot track the related marker")
#       del markersTrackerDict[lusiPid]
#    # ---
# ---

nbLusiPids= len(markersTrackerDict)

print("Tracking -> "+str(nbLusiPids)+" markers")

print("\nmarkersTrackerDict[0]="+str(markersTrackerDict[0]))
print("markersTrackerDict[nbLusiPids-1]="+str(markersTrackerDict[nbLusiPids-1]))

print("Debug exit 0")   
sys.exit(0)

del reader

#--- 
for vtuPFile in vtuPFiles[1:]:
                     
   print("\nReading vtuPFile: "+vtuPFile)
   vtuPFileName= os.path.basename(vtuPFile)

   reader= vtk.vtkXMLUnstructuredGridReader()
   
   reader.SetFileName(vtuPFile)
   reader.Update()
   
   #vtuPData[vtuPFileName]= reader.GetOutput()

   #--- Extract all the particles data
   dataTmp= reader.GetOutput()
   
   #--- Extract the timestamp (in years) as an int for this VTU file
   dataTime= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

   markersTrackerDict[dataTime]= {}
   
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
   #ipPosData= dataTmp.GetPointData().GetArray("initial position")
   
   #--- Extract oceanic crust particles data:
   #ocCrustData= dataTmp.GetPointData().GetArray("oceanicCrust")
   #ocCrustData= dataTmp.GetPointData().GetArray("initial oceanicCrust")
   
   #--- Extract particle Pressure data:
   pPData= dataTmp.GetPointData().GetArray("p")
   
   #--- Extract particles Temperature data:
   pTData= dataTmp.GetPointData().GetArray("T")

   protholithCompoData= dataTmp.GetPointData().GetArray(protholithCompoName)

   for metamMatName in metamGroupInfoDict:

       print("metamMatName="+metamMatName)
   
       vtuMetamData[metamMatName]= dataTmp.GetPointData().GetArray(metamMatName)
       #vtuMetamPidPT[metamMatName]= {}
       #for groupId in metamGroupInfoDict[metamMatName]:
       #    vtuMetamPidPT[metamMatName][groupId]= {}
       # ---
   # ---

   markersTrackerDictKeys= tuple(markersTrackerDict.keys())

   #for pidIter in range(0,pidDataSize):
   for lusiPid in markersTrackerDictKeys:

       #pidIter= markersTrackerDict[lusiPid][dataTime0]["pidIter"]
       #pidPos= pPos.GetTuple(pidIter)
       #pid= int(pidData.GetTuple(pidIter)[0])

       print("lusiPid="+str(lusiPid))
      
       #if markersTrackerDict[lusiPid] is None:
       #   continue

       for pidIter in range(0,pidDataSize):
          pidCheck= int(pidData.GetTuple(pidIter)[0])

          #if markersTrackerDict[lusiPid] is None:
          #   continue          

          if pidCheck == markersTrackerDict[lusiPid][dataTime0]["aspectPid"]:

             #print("Found matching pid -> "+str(pidCheck))

             protholithCompoCrt= protholithCompoData.GetTuple(pidIter)[0]
             pidPos= pPos.GetTuple(pidIter)

             #print("pidIter="+str(pidIter))
             #print("markersTrackerDict[lusiPid][dataTime0][pidIter]="+str(markersTrackerDict[lusiPid][dataTime0]["pidIter"]))
             #print("protholithCompoCrt="+str(protholithCompoCrt))
             #print("markersTrackerDict[lusiPid][dataTime0][protholithCompo(%)]="+
             #      str(markersTrackerDict[lusiPid][dataTime0]["protholithCompo(%)"]))
             #print("pidPos="+str(pidPos))
             #print("markersTrackerDict[lusiPid][dataTime0][PidPos]="+str(markersTrackerDict[lusiPid][dataTime0]["PidPos"]))
             #print("Debug exit 0")   
             #sys.exit(0)             
             #break

             if dataTime not in markersTrackerDict[lusiPid]:

                markersTrackerDict[lusiPid][dataTime]= {
                     "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
                     "Temperature(K)": pTData.GetTuple(pidIter)[0],
                     "protholithCompo(%)": protholithCompoCrt,
                     "PidPos": pidPos
                } 
                
                #markersTrackerDict[lusiPid].append({
                #    dataTime:{
                #     "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
                #     "Temperature(K)": pTData.GetTuple(pidIter)[0],
                #     "protholithCompo(%)": protholithCompoCrt,
                #     "PidPos": pidPos
                #     } 
                # })
                
             else:
                print("WARNING: aspect pid duplicate -> "+str(pidCheck)+" for lusiPid -> "+str(lusiPid)+" Cannot track this marker anymore !!")
                #markersTrackerDict[lusiPid]= None
                del markersTrackerDict[lusiPid]
                break
             # ---
          # --- if pidCheck == markersTrackerDict[lusiPid][dataTime0]["aspectPid"] block
       # --- pidIter loop     

       #if pid != markersTrackerDict[lusiPid][dataTime0]["pid"]:
       #           

       #protholithCompoCrt= protholithCompoData.GetTuple(pidIter)[0]

       #if protholithCompoCrt > minCompoValue:
       #   
       #   markersTrackerDict[dataTime][lusiPid]= {
       #                        "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
       #                        "Temperature(K)": pTData.GetTuple(pidIter)[0],
       #                        "protholithCompo(%)": protholithCompoCrt,
       #                        "PidPos": pidPos, "aspectPid": pid, "pidIter": pidIter 
       #   }
       #   lusiPid += 1
       # ---
       
       #for metamMatName in vtuMetamData:          
       #    # --- Compo for the metam. mat. at the pid position
       #   metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]
       #   for groupId in metamGroupInfoDict[metamMatName]:
       #       if metamMatCrt > minCompoValue:               
       #           markersTrackerDict[dataTime][lusiPid]= {
       #                        "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
       #                        "Temperature(K)": pTData.GetTuple(pidIter)[0],
       #                        "protholithCompo(%)": protholithCompoCrt
       #                        "metamCompo(%)": metamMatCrt, "PidPos": pidPos, "aspectPid": pid, "pidIter": pidIter
       #           }
       #         
       #           lusiPid += 1
       #      # ---
       # ---      
   # --- lusiPid loop

   print("nb valid lusiPid="+str(len(markersTrackerDict))+" at dataTime -> "+str(dataTime))

   print("Done with file -> "+vtuPFile)
   
# ---    
print("total valid lusiPids for all times="+str(len(markersTrackerDict)))
print("Debug exit 0")   
sys.exit(0)

reader= vtk.vtkXMLUnstructuredGridReader()

print("Reading vtuParticlesInitFile: "+vtuParticlesInitFile)

#vtuPFileName= os.path.basename(vtuPFile)
                  
reader.SetFileName(vtuParticlesInitFile)
reader.Update()
   
#vtuPData[vtuPFileName]= reader.GetOutput()
#--- Extract all the particles data
dataTmp= reader.GetOutput()
#--- Extract the timestamp (in years) as an int
dataTime= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

pidData= dataTmp.GetPointData().GetArray("id")

print("dataTime="+str(dataTime))

pidDataSize= pidData.GetSize()
print("pidData size="+str(pidDataSize)+"\n")

#--- particles position data for the timestamp
pPos= dataTmp.GetPointData().GetArray("position")

vtuMetamData= {}
vtuMetamPidPT= {}

for metamMatName in metamGroupInfoDict:

   print("metamMatName="+metamMatName)
   
   vtuMetamData[metamMatName]= dataTmp.GetPointData().GetArray(metamMatName)
   vtuMetamPidPT[metamMatName]= {}

   for groupId in metamGroupInfoDict[metamMatName]:
      vtuMetamPidPT[metamMatName][groupId]= {}
   # ---
# --- 
for pidIter in range(0,pidDataSize):

    pidPos= pPos.GetTuple(pidIter)
    pid= int(pidData.GetTuple(pidIter)[0])

    #print("pid int="+str(pid))
    #print("pid float="+str(pidData.GetTuple(pidIter)[0]))
    #print("Debug exit 0")   
    #sys.exit(0)
   
    for metamMatName in vtuMetamPidPT:

        # --- Compo for the metam. mat. at the pid position
        metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]
       
        for groupId in vtuMetamPidPT[metamMatName]:

            groupIdDict= metamGroupInfoDict[metamMatName][groupId]
           
            if pidPos[0] > groupIdDict["x1"] and pidPos[1] < groupIdDict["y1"] \
               and pidPos[0] < groupIdDict["x2"] and pidPos[1] > groupIdDict["y2"]:
       
               if metamMatCrt > minCompoValue:

                  #print("\npidIter="+str(pidIter)+",pid="+str(pid))
                  #print("pid int="+str(pid))
                  #print("pid float="+str(pidData.GetTuple(pidIter)[0]))
                  #print("pidPos="+str(pidPos))
                  #print("metamMatCrt="+str(metamMatCrt))
                  
                  if pid not in vtuMetamPidPT[metamMatName][groupId]:
                     vtuMetamPidPT[metamMatName][groupId][pid]= {} # { "pidIter": pidIter }
                  else:
                     print("Warning cannot have the same pid:"+str(pid)+" for two different pidIter !!")
                     #sys.exit(1)
                  # ---
                  
                  #if groupId=="group1":
                    #print("\nmetamMatName="+metamMatName)
                    #print("groupId="+groupId)
                    #print("metamMatCrt="+str(metamMatCrt))
                    #print("pidPos="+str(pidPos))
                    #print("pid="+str(pid))
                    #print("groupIdDict="+str(groupIdDict))
                    #sys.exit(0)
               # ---
            # ---
        # --- 
    # ---
# ---

print("vtuMetamPidPT[metamMatName][group1]="+str(sorted(vtuMetamPidPT[metamMatName]["group1"].keys())))
#print("Debug exit 0")   
#sys.exit(0)
del reader

timeInfoDict= {}

for metamMatName in vtuMetamPidPT:

   timeInfoDict[metamMatName]= {}
   
   for groupId in vtuMetamPidPT[metamMatName]:

       checkLen= len(vtuMetamPidPT[metamMatName][groupId])

       if checkLen==0:
          print("ERROR: no valid markers found for group -> "+
                groupId+", check its (x1,y1) vs (x2,y2) bounding box !!")
          sys.exit(1)
       # ---
          
       print("metamMatName="+metamMatName+", groupId="+groupId+", nb. markers found ="+str(checkLen))

       timeInfoDict[metamMatName][groupId]= {}
       # ---
       
   # ---
# ---
#print("Debug exit 0")   
#sys.exit(0)

timeInfoList= []

#--- 
for vtuPFile in vtuPFiles:
                     
   print("Reading vtuPFile: "+vtuPFile)
   vtuPFileName= os.path.basename(vtuPFile)

   reader= vtk.vtkXMLUnstructuredGridReader()
   
   reader.SetFileName(vtuPFile)
   reader.Update()
   
   #vtuPData[vtuPFileName]= reader.GetOutput()

   #--- Extract all the particles data
   dataTmp= reader.GetOutput()
   
   #--- Extract the timestamp (in years) as an int for this VTU file
   dataTime= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

   timeInfoList.append(dataTime)

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
   #ipPosData= dataTmp.GetPointData().GetArray("initial position")
   
   #--- Extract oceanic crust particles data:
   #ocCrustData= dataTmp.GetPointData().GetArray("oceanicCrust")
   #ocCrustData= dataTmp.GetPointData().GetArray("initial oceanicCrust")
   
   #--- Extract particle Pressure data:
   pPData= dataTmp.GetPointData().GetArray("p")
   
   #--- Extract particles Temperature data:
   pTData= dataTmp.GetPointData().GetArray("T")

   # --- Get the markers data for the metam. mats. for this time
   for metamMatName in vtuMetamPidPT:
       vtuMetamData[metamMatName]= dataTmp.GetPointData().GetArray(metamMatName)
       
       #timeInfoDict[metamMatName]= {}
       for groupId in vtuMetamPidPT[metamMatName]:
           timeInfoDict[metamMatName][groupId][dataTime]= []
           #vtuMetamPidPT[metamMatName][groupId][dataTime]= []
       # ---
   # ---
       
   #continue

   # --- Loop on all the markers ids.
   for pidIter in range(0,pidDataSize):

       pidPos= pPos.GetTuple(pidIter)
       pid= int(pidData.GetTuple(pidIter)[0])
       #print("pidPos check="+str(pidPos)+",pid="+str(pid))

       for metamMatName in vtuMetamPidPT:

          # --- Compo for the metam. mat. at the pid position for the time being processed
          metamMatCrt= vtuMetamData[metamMatName].GetTuple(pidIter)[0]

          #print("metamMatCrt="+str(metamMatCrt))

          #vtuMetamPidPT[metamMatName][groupId][dataTime]= []
          
          for groupId in vtuMetamPidPT[metamMatName]:
             if pid in vtuMetamPidPT[metamMatName][groupId] and metamMatCrt > minCompoValue:

                if dataTime in vtuMetamPidPT[metamMatName][groupId][pid]:
                   print("\nalready existing P,T info for pid:"+str(pid)+"="+str(vtuMetamPidPT[metamMatName][groupId][pid][dataTime]))
                   tmpDict= { "Pressure(Gpa)": pPData.GetTuple(pidIter)[0], "Temperature(K)": pTData.GetTuple(pidIter)[0],
                              "Compo(%)": metamMatCrt, "PidPos": pidPos }
                   print("Other P,T info="+str(tmpDict))
                   #print("pidPos="+str(pidPos))
                   #print("Debug exit 0")
                   #sys.exit(0)
                # ---
                
                vtuMetamPidPT[metamMatName][groupId][pid].update({
                   dataTime: { "Pressure(Gpa)": pPData.GetTuple(pidIter)[0],
                               "Temperature(K)": pTData.GetTuple(pidIter)[0],
                               "Compo(%)": metamMatCrt,
                               "PidPos": pidPos
                              }
                })

                timeInfoDict[metamMatName][groupId][dataTime].append(pid)

                #print("vtuMetamPidPT[metamMatName][groupId][dataTime]="+str(vtuMetamPidPT[metamMatName][groupId][dataTime]))

                #if dataTime not in timeInfoDict[metamMatName][groupId]:
                #   timeInfoDict[metamMatName][groupId].append(dataTime)
                # ---
             #else:
                
                #if groupId == "group1":
                #   print("pid="+str(pid)+", metamMatCrt="+str(metamMatCrt))
                # ---

                #print("Found valid marker with pid="+str(pid)+" for metamMatName="+metamMatName
                #      +" for groupId="+groupId+" at dataTime="+str(dataTime)+" at pos"+str(pidPos))
                #print("vtuMetamPidPT[metamMatName][groupId][pid][dataTime]="+str(vtuMetamPidPT[metamMatName][groupId][pid][dataTime]))
                #print("Debug exit 0")   
                #sys.exit(0)               
                
             # ---
          # ---
       # ---
       #print("pidPos check="+str(pidPos))
       
   # --- pids loop

   #print(

   #validPids= {}

   for metamMatName in vtuMetamPidPT:

      #pavg= 0.0
      #tavg= 0.0
      #nbData= 0
      #validPids[metamMatName]= []
      
      for groupId in vtuMetamPidPT[metamMatName]:
         
         pavg= 0.0
         tavg= 0.0
         cavg= 0.0
         nbData= 0
         
         for pid in vtuMetamPidPT[metamMatName][groupId]:
            if dataTime in vtuMetamPidPT[metamMatName][groupId][pid]:
               pavg += vtuMetamPidPT[metamMatName][groupId][pid][dataTime]["Pressure(Gpa)"]
               tavg += vtuMetamPidPT[metamMatName][groupId][pid][dataTime]["Temperature(K)"]
               cavg += vtuMetamPidPT[metamMatName][groupId][pid][dataTime]["Compo(%)"]
               nbData += 1
            # ---
         # ---

         if nbData >= 1:
            print("\nmetamMatName: "+metamMatName+" nbData for group: "+groupId+" at time: "+str(dataTime)+" is: "+str(nbData))
            print("metamMatName: "+metamMatName+" pavg for group: "+groupId+" at time: "+str(dataTime)+" is: "+str(pavg/nbData))
            print("metamMatName: "+metamMatName+" tavg for group: "+groupId+" at time: "+str(dataTime)+" is: "+str(tavg/nbData))
            print("metamMatName: "+metamMatName+" cavg for group: "+groupId+" at time: "+str(dataTime)+" is: "+str(cavg/nbData))
         else:
            print("WARNING: no valid markers found for metamMatName:"+metamMatName+" for group: "+groupId+" at time: "+str(dataTime))
         # ---

         print("timeInfoDict[metamMatName][groupId][dataTime]="+str(sorted(timeInfoDict[metamMatName][groupId][dataTime])))
         
      # --- 
   # ---
   print("done with VTU file: "+vtuPFile+"\n")

   del reader

   print("Debug exit 0")   
   sys.exit(0)
   #dataTime= vtuPData[vtuPFileName].GetPointData().GetArray("TIME")
   #dataTime= vtuPData[vtuPFileName].GetFieldData().GetArray("TIME").GetTuple(

#--- End for loop on VTU files

print("Debug exit 0")   
sys.exit(0)

# --- 
timeIncrTuple= tuple(sorted(timeInfoList))

print("len(timeIncrTuple)="+str(len(timeIncrTuple)))

validPidsPerGroup= {}

for metamMatName in vtuMetamPidPT:

   validPidsPerGroup[metamMatName]= {}
   
   for groupId in vtuMetamPidPT[metamMatName]:
      
       print("len(timeInfoDict[metamMatName]["+groupId+"])="+str(len(timeInfoDict[metamMatName][groupId])))

       validPidsPerGroup[metamMatName][groupId]= []

       for pid in vtuMetamPidPT[metamMatName][groupId]:
          
          timesForPid= tuple(vtuMetamPidPT[metamMatName][groupId][pid].keys())

          #print("len(timesForPid)="+str(len(timesForPid)))

          # --- Only keep the pid if it has all the wanted times keys in its vtuMetamPidPT[metamMatName][groupId][pid] dict  
          if len(timesForPid) == timeInfoDict[metamMatName][groupId]:
              validPidsPerGroup[metamMatName][groupId].append(pid) 
          # --
       # ---
       
       #for time in timeInfoDict[metamMatName][groupId]:
       #for pid in vtuMetamPidPT[metamMatName][groupId]:
       #      if time in vtuMetamPidPT[metamMatName][groupId][pid]:
       #         if pid not in validPidsPerGroup[metamMatName][groupId]:
       #            validPidsPerGroup[metamMatName][groupId].append(pid)
             # ---
          # ---
       # ---
       print("Nb. valid pids="+str(len(validPidsPerGroup[metamMatName][groupId]))+" for group "+groupId+" of "+metamMatName)
       
   # ---metamMatName
# ---
print("Debug exit 0")   
sys.exit(0)


#validMetamPidPT= {}
#for time in timeInfoList:
#   for metamMatName in vtuMetamPidPT:
#       validMetamPidPT[metamMatName]= {}
#       
#       for groupId in vtuMetamPidPT[metamMatName]:
#           validMetamPidPT[metamMatName][groupId]= {}          
#           for pid in vtuMetamPidPT[metamMatName][groupId]:             
#              if time in vtuMetamPidPT[metamMatName][groupId][pid]:
#                  validMetamPidPT[metamMatName][groupId][pid]= { time: vtuMetamPidPT[metamMatName][groupId][pid][time]}
#              else:
#                  validMetamPidPT[metamMatName][groupId][pid]= { time: None }
#              # ---
#           # ---
#        # ---
#   # ---
# ---
#print("Debug exit 0")   
#sys.exit(0)

#for metamMatName in vtuMetamPidPT:
#    metamMatNameReal= metamMatName.split(" ")[1]
#    print("metamMatNameReal="+metamMatNameReal)
#     for groupId in vtuMetamPidPT[metamMatName]:
#        if len(timeInfoDict[metamMatName][groupId]) == len(timeIncrTuple):          
              
    
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
 
