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
pidDataEnd= numpy.copy(lastH5Data["id"])
pidDataSizeEnd= pidDataEnd.shape[0]
print("pidDataEnd size="+str(pidDataSizeEnd)+"\n")
#sys.exit(0)

#--- particles initial position data for the timestamp
#initPosDataEnd= dataTmpEnd.GetPointData().GetArray("initial position")
initPosDataEnd= numpy.copy(lastH5Data["initial position"])

#--- particles position data for the timestamp
#pPosDataEnd= dataTmpEnd.GetPointData().GetArray("position")
pPosDataEnd= numpy.copy(lastH5Data["position"])

#--- Extract particle Pressure data:
#pPDataEnd= dataTmpEnd.GetPointData().GetArray("p")
pPDataEnd= numpy.copy(lastH5Data["p"])
   
#--- Extract particles Temperature [K] data:
#pTDataEnd= dataTmpEnd.GetPointData().GetArray("T")
pTDataEnd= numpy.copy(lastH5Data["T"])

#protoPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicCrustMRB")
protoPDataEnd= numpy.copy(lastH5Data["lusi oceanicCrustMRB"])

#ocSedPDataEnd= dataTmpEnd.GetPointData().GetArray("lusi oceanicSeds")
ocSedPDataEnd= numpy.copy(lastH5Data["lusi oceanicSeds"])

initAsthEnd= numpy.copy(lastH5Data["initial asthenosphere"])
initProtoEnd= numpy.copy(lastH5Data["initial oceanicCrustMRB"])
initOcSedEnd= numpy.copy(lastH5Data["initial oceanicSeds"])

#nodesDataEnd= lastH5Data["nodes"]

#initCompo= dataTmp.GetPointData().GetArray("initial composition")
#validPids= []

#metamMatOthers= ("lusi greenschists", "lusi amphibolites", "lusi blueschists", "lusi eclogites")
#vtuMetamOthersData= {}
#for metamMatOther in metamMatOthers:
#    vtuMetamOthersData[metamMatOther]= dataTmpEnd.GetPointData().GetArray(metamMatOther)

h5MetamData= {}
h5MetamPidPT= {}
#h5MetamPidPT= {dataTimeEnd: {} }

metamGroupInfoDict= { "lusi granulites", "lusi greenschists", "lusi amphibolites", "lusi blueschists", "lusi eclogites" }

for metamMatName in metamGroupInfoDict:

   #print("metamMatName="+metamMatName)
   
   #vtuMetamData[metamMatName]= dataTmpEnd.GetPointData().GetArray(metamMatName)
   #vtuMetamPidPT[metamMatName]= {}

   h5MetamData[metamMatName]= numpy.copy(lastH5Data[metamMatName])
   #h5MetamPidPT[metamMatName]= {dataTimeEnd: {} } 

   #for groupId in metamGroupInfoDict[metamMatName]:
   #   #vtuMetamPidPT[metamMatName][groupId]= {}
   #   h5MetamPidPT[metamMatName][groupId]= {}
   # ---
# ---

#greenschistsPData= dataTmpEnd.GetPointData().GetArray("lusi greenschists")
#amphibolitesPData= dataTmpEnd.GetPointData().GetArray("lusi amphibolites")

#initPosTrackingList= []
#initPosTrackingDict= {}
h5MetamPidPTMats= {dataTimeEnd: {} }

yElevMin= 250e3
xMin= 0.5e6
xMax= 2.5e6

#finalPids= []

for pidIter in range(0,pidDataSizeEnd):
#for pidIter in range(pidDataSizeEnd-1,0,-1):
#for pidIter in range(int(pidDataSizeEnd/2),int(pidDataSizeEnd/1.75)):

    #print("pidIter="+str(pidIter))
    #print("pPosDataEnd[pidIter]="+str(pPosDataEnd[pidIter]))
    #pidPos= pPosDataEnd.GetTuple(pidIter)
    pidPosX= pPosDataEnd[pidIter][0]
    pidPosY= pPosDataEnd[pidIter][1]

    #pid= pidDataEnd[pidIter][0]
    #print("nodesDataEnd[pidIter]="+str(nodesDataEnd[pidIter]))
    #sys.exit(0)
    
    if pidPosY < yElevMin: #600e3:
       continue

    #if pidPosX < 1e6 or pidPosX > 2e6:
    if pidPosX < xMin or pidPosX > pidPosX:
       continue

    #pidFloat= pidDataEnd[pidIter][0]
    pid= int(pidDataEnd[pidIter][0])
    #print("pidIter="+str(pidIter))
    #print("pPosDataEnd[pidIter]="+str(pPosDataEnd[pidIter]))
    #print("pidFloat="+str(pidFloat))
    #print("pid="+str(pid))
    #print("nodesDataEnd[pidIter]="+str(nodesDataEnd[pidIter]))
    #initPosTrackingDict[pid]= pidIter
    #sys.exit(0)

    #print("pPosDataEnd[pidIter]="+str(pPosDataEnd[pidIter]))
    #print("checking at pPosDataEnd[pidIter]="+str(pPosDataEnd[pidIter]))
    #print("pid="+str(pid))

    ocCrustMRBCrt= protoPDataEnd[pidIter,0]
    ocSedsCrt= ocSedPDataEnd[pidIter,0]
    
    for metamMatName in metamGroupInfoDict: #h5MetamData: #h5MetamPidPT:
    #    #print("metamMatName="+metamMatName)
    #    # --- Compo for the metam. mat. at the pid position
    #    #metamMatCrt= h5MetamData[metamMatName].GetTuple(pidIter)[0]
        metamMatCrt= h5MetamData[metamMatName][pidIter,0]

        #print("metamMatName="+metamMatName+", metamMatCrt="+str(metamMatCrt))
        #sys.exit(0)

        checkInitMat= initAsthEnd[pidIter,0] + initProtoEnd[pidIter,0] + initOcSedEnd[pidIter,0]
        
        if ((ocCrustMRBCrt > minCompoValue) or (ocSedsCrt > minCompoValue ) or \
            (metamMatCrt > minCompoValue)) and (checkInitMat > 0.5) and (pid not in h5MetamPidPTMats[dataTimeEnd]) :      

           if pid in h5MetamPidPTMats[dataTimeEnd]:
              print("Cannot have duplicate pids !!"+str(pid)+" for last time : "+str(dataTimeEnd))
              sys.exit(1)
           #else :
           #  finalPids.append(pid)       
           
           #h5MetamPidPT[metamMatName][dataTimeEnd][pid]= {
           h5MetamPidPTMats[dataTimeEnd][pid]= {
              "initial asthenosphere": initAsthEnd[pidIter,0],
              "initial oceanicCrustMRB": initProtoEnd[pidIter,0],
              "initial oceanicSeds": initOcSedEnd[pidIter,0],
              "initial position":tuple(initPosDataEnd[pidIter][...]),
              "position": tuple(pPosDataEnd[pidIter][...]),
              "p": pPDataEnd[pidIter,0],
              "T": pTDataEnd[pidIter,0],
              "materials": {
                   "oceanicCrustMRB": protoPDataEnd[pidIter,0],
                   "oceanicSeds": ocSedPDataEnd[pidIter,0],
                   "granulites" : h5MetamData["lusi granulites"][pidIter,0],
                   "greenschists": h5MetamData["lusi greenschists"][pidIter,0],
                   "amphibolites": h5MetamData["lusi amphibolites"][pidIter,0],
                   "blueschists": h5MetamData["lusi blueschists"][pidIter,0],
                   "eclogites": h5MetamData["lusi eclogites"][pidIter,0],
              }
           }

           #print("h5MetamPidPTMats[dataTimeEnd][pid]="+str(h5MetamPidPTMats[dataTimeEnd][pid]))
           #sys.exit(0)

           #if h5MetamData["lusi granulites"][pidIter,0] > 0.5:
           #   print("h5MetamPidPTMats[dataTimeEnd][pid]="+str(h5MetamPidPTMats[dataTimeEnd][pid]))
           #   sys.exit(0)

           #if pid in :
           #   print("Cannot have duplicate pids !!"+str(pid))
           #   sys.exit(1)
           #else :
           #  finalPids.append(pid)       
           #print("metamMatName="+metamMatName)
           #print("h5MetamPidPTMats[dataTimeEnd][pid]="+str(h5MetamPidPTMats[dataTimeEnd][pid]))
           #print("h5MetamPidPT[metamMatName][dataTimeEnd][pid]="+str( h5MetamPidPT[metamMatName][dataTimeEnd][pid]))
           #sys.exit(0)
           #break
   # ---
# ---

finalPids= tuple(h5MetamPidPTMats[dataTimeEnd].keys())
print("nb. of finalPids="+str(len(finalPids)))
#for  metamMatName in metamGroupInfoDict:
#print("found "+str(len(h5MetamPidPT[metamMatName][dataTimeEnd]))+" markers for "+metamMatName+" at "+str(dataTimeEnd)+" My")


del pidDataEnd
del initPosDataEnd
del pPosDataEnd
del pPDataEnd
del pTDataEnd
del protoPDataEnd
del ocSedPDataEnd

for metamMatName in metamGroupInfoDict:

   del h5MetamData[metamMatName]
# ---

lastH5Data.close()
print("done with final file")
#print("Debug exit 0")   
#sys.exit(0)

#pidsAtTimes= {}

for vtuFileInPast in sorted(vtuPFiles[0:-1],reverse=True):

   reader= vtk.vtkXMLUnstructuredGridReader()

   print("\nReading vtu file -> "+vtuFileInPast)

   reader.SetFileName(vtuFileInPast)
   reader.Update()

   vtuData= reader.GetOutput()
   
   dataTime= int(vtuData.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

   print("dataTime="+str(dataTime))
   
   del vtuData
   del reader

   h5FilePath= particlesDir+"/particles-"+ os.path.basename(vtuFileInPast).split("-")[1].split(".")[0]+".h5"

   print("h5FilePath="+str(h5FilePath))

   h5Data= h5py.File(h5FilePath,"r")

   pidData= numpy.copy(h5Data["id"])

   pidDataSize= pidData.shape[0]

   print("pidDataSize="+str(pidDataSize))

   initPosData= numpy.copy(h5Data["initial position"])

   pPosData= numpy.copy(h5Data["position"])

   pPData= numpy.copy(h5Data["p"])

   pTData= numpy.copy(h5Data["T"])

   protoPData= numpy.copy(h5Data["lusi oceanicCrustMRB"])

   ocSedPData= numpy.copy(h5Data["lusi oceanicSeds"])

   initAsthData= numpy.copy(h5Data["initial asthenosphere"])

   initProtoData= numpy.copy(h5Data["initial oceanicCrustMRB"])
   initOcSedsData= numpy.copy(h5Data["initial oceanicSeds"])

   for metamMatName in metamGroupInfoDict:

      #print("metamMatName="+metamMatName)

      h5MetamData[metamMatName]= numpy.copy(h5Data[metamMatName])
   # ---
   
   h5MetamPidPTMats[dataTime]= {}

   for pidIter in range(0,pidDataSize):

      pidPosX= pPosData[pidIter][0]
      pidPosY= pPosData[pidIter][1]

      if pidPosY < yElevMin: #600e3:
         continue

      if pidPosX < xMin or pidPosX > pidPosX:
         continue  
    
      pid= int(pidData[pidIter][0])

      ocCrustMRBCrt= protoPData[pidIter,0]
      ocSedsCrt= ocSedPData[pidIter,0]

      for metamMatName in metamGroupInfoDict:

        metamMatCrt= h5MetamData[metamMatName][pidIter,0]

        #print("metamMatName="+metamMatName+", metamMatCrt="+str(metamMatCrt))
        #sys.exit(0)

        checkInitMat= initAsthData[pidIter,0] + initProtoData[pidIter,0] + initOcSedsData[pidIter,0]
        
        if ((ocCrustMRBCrt > minCompoValue) or (ocSedsCrt > minCompoValue ) or \
            (metamMatCrt > minCompoValue)) and (checkInitMat > 0.5 ) and (pid not in h5MetamPidPTMats[dataTime]) :

           if pid in h5MetamPidPTMats[dataTime]:
              print("Cannot have duplicate pids !!"+str(pid)+" for time:"+str(dataTime))
              sys.exit(1)           
           # ---
           
           h5MetamPidPTMats[dataTime][pid]= {
              
              "initial asthenosphere": initAsthData[pidIter,0],
              "initial oceanicCrustMRB": initProtoData[pidIter,0],
              "initial oceanicSeds": initOcSedsData[pidIter,0],
              "initial position":tuple(initPosData[pidIter][...]),
              "position": tuple(pPosData[pidIter][...]),
              "p": pPData[pidIter,0],
              "T": pTData[pidIter,0],
              "materials": {
                   "oceanicCrustMRB": protoPData[pidIter,0],
                   "oceanicSeds": ocSedPData[pidIter,0],
                   "granulites" : h5MetamData["lusi granulites"][pidIter,0],
                   "greenschists": h5MetamData["lusi greenschists"][pidIter,0],
                   "amphibolites": h5MetamData["lusi amphibolites"][pidIter,0],
                   "blueschists": h5MetamData["lusi blueschists"][pidIter,0],
                   "eclogites": h5MetamData["lusi eclogites"][pidIter,0]
              }
           }

           #if h5MetamData["lusi granulites"][pidIter,0] > 0.5:
           #   print("h5MetamPidPTMats[dataTime][pid]="+str(h5MetamPidPTMats[dataTime][pid]))
           #   sys.exit(0)           

        # ---
      # ---
   print("nb. markers="+str(len(h5MetamPidPTMats[dataTime]))+" for time: "+str(dataTime))

   for metamMatName in metamGroupInfoDict:

      #print("metamMatName="+metamMatName)

      del h5MetamData[metamMatName]
   # ---
   
# ---

metamPidTrack= {}

for pidAtEnd in h5MetamPidPTMats[dataTimeEnd]:
   
   metamPidTrack[pidAtEnd]= { dataTimeEnd : h5MetamPidPTMats[dataTimeEnd][pidAtEnd] }
   
   for dataTimeChk in sorted((tuple(h5MetamPidPTMats.keys())[1:]),reverse=True):

      #print("pidAtEnd="+str(pidAtEnd)+", checking dataTimeChk="+str(dataTimeChk))

      if pidAtEnd in h5MetamPidPTMats[dataTimeChk]:

         if h5MetamPidPTMats[dataTimeChk][pidAtEnd]["initial position"] == \
              h5MetamPidPTMats[dataTimeEnd][pidAtEnd]["initial position"] :

              metamPidTrack[pidAtEnd].update({ dataTimeChk: h5MetamPidPTMats[dataTimeChk][pidAtEnd] })
         # ---
      # ---
   # ---

   if len(metamPidTrack[pidAtEnd]) >= 2:
      #print("\nmetamPidTrack[pidAtEnd]="+str(metamPidTrack[pidAtEnd]))
      #print("metamPidTrack[pidAtEnd][materials]="+str(metamPidTrack[pidAtEnd][materials]))
      for time in tuple(metamPidTrack[pidAtEnd].keys()):
          print("metamPidTrack[pidAtEnd][time][position]="+str(metamPidTrack[pidAtEnd][time]["position"]))
          print("metamPidTrack[pidAtEnd][time][p]="+str(metamPidTrack[pidAtEnd][time]["p"]))
          print("metamPidTrack[pidAtEnd][time][T]="+str(metamPidTrack[pidAtEnd][time]["T"]))
          print("metamPidTrack[pidAtEnd][time][materials]="+str(metamPidTrack[pidAtEnd][time]["materials"]))
      # ---
      print("metamPidTrack[pidAtEnd].keys()="+str(tuple(metamPidTrack[pidAtEnd].keys()))+"\n")
      #sys.exit(0)
   else:
      del metamPidTrack[pidAtEnd]
   # ---

# ---

print("nb. valid markers: "+str(len(metamPidTrack)))
print("Debug exit 0")
sys.exit(0)
          
#--- Extract all the particles data
#dataTmpStart= reader.GetOutput()

#--- Extract the timestamp (in years) as an int for this VTU file
#dataTimeStart= int( dataTmpStart.GetFieldData().GetArray("TIME").GetTuple(0)[0] )
#print("dataTimeStart="+str(dataTimeStart))
#print("Debug exit 0")
#sys.exit(0)

startH5Data= h5py.File(h5PFiles[0],"r")

pidDataStart= numpy.copy(startH5Data["id"])
#pidDataStart= dataTmpStart.GetPointData().GetArray("id")
#pidDataSizeStart= pidDataStart.GetSize()
pidDataSizeStart= pidDataStart.shape[0]

print("pidDataStart size="+str(pidDataSizeStart)+"\n")

#--- particles initial position data for the timestamp
#initPosDataStart= dataTmpStart.GetPointData().GetArray("initial position")
initPosDataStart= numpy.copy(startH5Data["initial position"])

#--- particles position data for the timestamp
#pPosDataStart= dataTmpStart.GetPointData().GetArray("position")
pPosDataStart= numpy.copy(startH5Data["position"])

#--- Extract particle Pressure data:
#pPDataStart= dataTmpStart.GetPointData().GetArray("p")
pPDataStart= numpy.copy(startH5Data["p"])                        
   
#--- Extract particles Temperature data:
#pTDataStart= dataTmpStart.GetPointData().GetArray("T")
pTDataStart= numpy.copy(startH5Data["T"])

#protoPDataStart= dataTmpStart.GetPointData().GetArray("lusi oceanicCrustMRB")
protoPDataStart= numpy.copy(startH5Data["lusi oceanicCrustMRB"])

#ocSedPDataStart= dataTmpStart.GetPointData().GetArray("lusi oceanicSeds")
ocSedPDataStart= numpy.copy(startH5Data["lusi oceanicSeds"])

#greenschistsPData= dataTmpStart.GetPointData().GetArray("lusi greenschists")
greenschistsPData= numpy.copy(startH5Data["lusi greenschists"])

#amphibolitesPData= dataTmpStart.GetPointData().GetArray("lusi amphibolites")
amphibolitesPData=  numpy.copy(startH5Data["lusi amphibolites"])

for metamMatName in metamGroupInfoDict:

   print("metamMatName="+metamMatName)

   h5MetamData[metamMatName]= numpy.copy(startH5Data[metamMatName])
# ---

h5MetamPidPTMats[dataTimeStart]= {}

for pidIter in range(0,pidDataSizeStart):

    #initialPos= initPosDataStart.GetTuple(pidIter)
    #aspectPid= int(pidDataStart.GetTuple(pidIter)[0])
    #initialPosIdStr= "{:12.7f}".format(initialPos[0])+"_"+"{:12.7f}".format(initialPos[1])+"_"+str(aspectPid)

    #protolithCrt= protoPDataStart.GetTuple(pidIter)[0]
    #aspectPid= pidData.GetTuple(pidIter)[0]
    #ocSedCrt= ocSedPDataStart.GetTuple(pidIter)[0]

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
    
    pid= int(pidDataStart[pidIter][0])

    ocCrustMRBCrt= protoPDataStart[pidIter,0]
    ocSedsCrt= ocSedPDataStart[pidIter,0]

    for metamMatName in metamGroupInfoDict:

        metamMatCrt= h5MetamData[metamMatName][pidIter,0]

        #print("metamMatName="+metamMatName+", metamMatCrt="+str(metamMatCrt))
        #sys.exit(0)
        
        if ((ocCrustMRBCrt > minCompoValue) or (ocSedsCrt > minCompoValue ) or \
            (metamMatCrt > minCompoValue)) and (pid not in h5MetamPidPTMats[dataTimeStart]) :

           if pid in h5MetamPidPTMats[dataTimeStart]:
              print("Cannot have duplicate pids !!"+str(pid))
              sys.exit(1)           

           h5MetamPidPTMats[dataTimeStart][pid]= {
              "initial position":initPosDataStart[pidIter],
              "position": pPosDataStart[pidIter],
              "p": pPDataStart[pidIter,0],
              "T": pTDataStart[pidIter,0],
              "materials": {
                   "oceanicCrustMRB": protoPDataStart[pidIter,0],
                   "oceanicSeds": ocSedPDataStart[pidIter,0],
                   "granulites" : h5MetamData["lusi granulites"][pidIter,0],
                   "greenschists": h5MetamData["lusi greenschists"][pidIter,0],
                   "amphibolites": h5MetamData["lusi amphibolites"][pidIter,0],
                   "blueschists": h5MetamData["lusi blueschists"][pidIter,0],
                   "eclogites": h5MetamData["lusi eclogites"][pidIter,0]
              }
           }
           
           #print("metamMatName="+metamMatName)
           #print("h5MetamPidPTMats[dataTimeStart][pid]="+str(h5MetamPidPTMats[dataTimeStart][pid]))
           #sys.exit(0)    
 
# ---
initialPids= tuple(h5MetamPidPTMats[dataTimeStart].keys())

print("nb. of initialPids="+str(len(initialPids)))
print("Done with 1st markers file")

#addedPids= []
persistentPids= []

#for finalPid in sorted(finalPids):
for initialPid in initialPids:
   
   #print("checking finalPid="+str(finalPid))
   if initialPid in finalPids:

      persistentPids.append(initialPid)   
# ---

print("tenttaive nb. of persistentPids="+str(len(persistentPids)))

validPids= []

for persistentPid in persistentPids:

   #print("h5MetamPidPTMats[dataTimeStart][persistentPid]="+str(h5MetamPidPTMats[dataTimeStart][persistentPid]))
   #print("h5MetamPidPTMats[dataTimeEnd][persistentPid]="+str(h5MetamPidPTMats[dataTimeEnd][persistentPid]))
   
   if h5MetamPidPTMats[dataTimeEnd][persistentPid]["initial position"][0] != h5MetamPidPTMats[dataTimeStart][persistentPid]["initial position"][0]:
      print("\ninitial position mismatch for persistentPid -> "+str(persistentPid)+", rejected !!\n")
      #sys.exit(0)

   else:

      if (h5MetamPidPTMats[dataTimeEnd][persistentPid]["materials"]["granulites"] > 0.1):
          print("h5MetamPidPTMats[dataTimeStart][persistentPid][materials][granulites]="+str(h5MetamPidPTMats[dataTimeStart][persistentPid]["materials"]["granulites"]))
          print("h5MetamPidPTMats[dataTimeEnd][persistentPid][materials][granulites]="+str(h5MetamPidPTMats[dataTimeEnd][persistentPid]["materials"]["granulites"]))         
      validPids.append(persistentPid)
      
# ---

print("nb. of validPids="+str(len(validPids)))
print("Debug exit 0")
sys.exit(0)

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
 
