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

# ---
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

    pid= pidDataEnd[pidIter][0]
    #pidFloat= pidDataEnd[pidIter][0]
    #pid= int(pidDataEnd[pidIter][0])
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

      pid= pidData[pidIter][0]
      #pid= int(pidData[pidIter][0])

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

   del initPosData
   del h5Data
   
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
         else:
           print("Cannot have different initial positions for the same pid:"+str(pidAtEnd))
           print("h5MetamPidPTMats[dataTimeChk][pidAtEnd][\"initial position\"]="+str(h5MetamPidPTMats[dataTimeChk][pidAtEnd]["initial position"]))
           print("h5MetamPidPTMats[dataTimeEnd][pidAtEnd][\"initial position\"]="+str(h5MetamPidPTMats[dataTimeEnd][pidAtEnd]["initial position"]))
           print("dataTimeChk="+str(dataTimeChk))
           print("metamPidTrack[pidAtEnd].keys()="+str(tuple(metamPidTrack[pidAtEnd].keys()))+"\n")
           print("h5MetamPidPTMats[dataTimeChk][pidAtEnd][materials]="+str(h5MetamPidPTMats[dataTimeChk][pidAtEnd]["materials"]))
           print("h5MetamPidPTMats[dataTimeEnd][pidAtEnd][materials]="+str(h5MetamPidPTMats[dataTimeEnd][pidAtEnd]["materials"]))
           #sys.exit(1)
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

depthThreshold= 10000.0 #20000.0

for markerPid in metamPidTrack:

    markerPidTimeKeys= sorted(tuple(metamPidTrack[markerPid].keys()))

    nbTimes= len(markerPidTimeKeys)

    mrkCsvFileOut= csvFilesOuputFolder + "/" + str(nbTimes)+"_"+ str(markerPid) +"_pTPathsMaterials.csv"

    mrkCsvFileOutP= open(mrkCsvFileOut,"w")

    mrkCsvFileOutP\
      .write("#time[My},p(GPA),T(C),T(K),Depth(y[m]),Position(x[m]),granulites,amphibolites,greenschists,blueschists,eclogites\
oceanicCrustMRB,oceanicSeds,initAsth,initOcCrustMrb,initOcSeds,metamCompVarBool,depthThresholdReached\n ")

    validPid= False
    countTimes= 0

    timeMyBeg= markerPidTimeKeys[0]
    #print("t0="+str(t0))
    #sys.exit(0)
    
    prevTimeGranu= metamPidTrack[markerPid][timeMyBeg]["materials"]["granulites"]
    prevTimeAmphi= metamPidTrack[markerPid][timeMyBeg]["materials"]["amphibolites"]
    prevTimeGrnSch= metamPidTrack[markerPid][timeMyBeg]["materials"]["greenschists"]
    prevTimeBluSch= metamPidTrack[markerPid][timeMyBeg]["materials"]["blueschists"]
    prevTimeEclo= metamPidTrack[markerPid][timeMyBeg]["materials"]["eclogites"]
    
    #for timeMy in sorted(tuple(metamPidTrack[markerPid].keys())):
    for timeMy in markerPidTimeKeys:

       #print("metamPidTrack[validMarkerPid][timeMy]="+str(metamPidTrack[validMarkerPid][timeMy]))
 
       materialDict= metamPidTrack[markerPid][timeMy]["materials"]

       if (materialDict["granulites"] + materialDict["amphibolites"] + materialDict["blueschists"] +
           materialDict["eclogites"] + materialDict["greenschists"] + materialDict["oceanicCrustMRB"] + materialDict["oceanicSeds"] ) > minCompoValue:

          validPid= True
          countTimes += 1

          depth= 700e3-metamPidTrack[markerPid][timeMy]["position"][1]

          depthThresholdReached= "TooShallow" #False
          
          if depth >= depthThreshold:
             depthThresholdReached= "DepthThrReached" #True

          metamCompoVar= False
             
          if materialDict["granulites"] > prevTimeGranu or \
             materialDict["amphibolites"] > prevTimeAmphi or \
             materialDict["greenschists"] > prevTimeGrnSch or \
             materialDict["blueschists"] > prevTimeBluSch or \
             materialDict["eclogites"] > prevTimeEclo:
               metamCompoVar= True
                 
          mrkCsvFileOutP\
             .write(str((timeMy-42e6)/1e6)+","+str(metamPidTrack[markerPid][timeMy]["p"])+","+
                    str(metamPidTrack[markerPid][timeMy]["T"]-273.0)+","+str(metamPidTrack[markerPid][timeMy]["T"])+","+
                    str(700e3-metamPidTrack[markerPid][timeMy]["position"][1])+","+str(metamPidTrack[markerPid][timeMy]["position"][0])+","+
                    str(materialDict["granulites"])+","+str(materialDict["amphibolites"])+","+str(materialDict["greenschists"])+","+
                    str(materialDict["blueschists"])+","+str(materialDict["eclogites"])+","+str(materialDict["oceanicCrustMRB"])+","+
                    str(materialDict["oceanicSeds"])+","+str(metamPidTrack[markerPid][timeMy]["initial asthenosphere"])+","+
                    str(metamPidTrack[markerPid][timeMy]["initial oceanicCrustMRB"])+","+str(metamPidTrack[markerPid][timeMy]["initial oceanicSeds"])+","+
                    str(metamCompoVar)+","+depthThresholdReached+"\n")

      # ---

    mrkCsvFileOutP.close

    if not validPid :
       print("No relevant metam. materials for marker -> "+str(markerPid)+" removing its file -> "+mrkCsvFileOut)
       os.remove(mrkCsvFileOut)

    elif countTimes != nbTimes:
       print("countTimes != nbTimes for marker -> "+str(markerPid)+" removing its file -> "+mrkCsvFileOut)
       os.remove(mrkCsvFileOut) 
    
    #sys.exit(0)
# ---

#print("Debug exit 0")
#sys.exit(0)
          

 
