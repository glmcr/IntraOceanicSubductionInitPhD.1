#!/usr/bin/python3

import os,sys
import numpy

import geomDefBtlAndBea2017EPSL as geom


aspectParamsFile= sys.argv[1]

aspectParamsFp= open(aspectParamsFile,"r")

aspectParamsFileLines= aspectParamsFp.readlines()

aspectParamsFp.close()

sep="::"

relevantSubsectionsDict={
    
    "subsection"+sep+"Geometry"+sep+"model" : {
        "set"+sep+"Y"+sep+"extent"+sep: None,
        "set"+sep+"X"+sep+"extent"+sep: None
     },
    "subsection"+sep+"Initial"+sep+"composition"+sep+"model" : {
        "set"+sep+ "Data" +sep+"file" +sep+"name"+sep: None,
        "set"+sep+"Data" +sep+"directory" +sep: None
    },
    "subsection"+sep+"Initial"+sep+"temperature"+sep+"model" : {
        "set"+sep+ "Data" +sep+"file" +sep+"name"+sep: None,
        "set"+sep+"Data" +sep+"directory"+sep: None     
    },
    "subsection"+sep+"Compositional"+sep+"fields": {
        "set"+sep+"Names"+sep+ "of"+sep+"fields"+sep: None
    }
}

endCounter= 0
relevantKey= None
relevantLine= False

for aspectParamsFileLine in aspectParamsFileLines:

    if aspectParamsFileLine[0] == "#": continue

    #print("start line processing: endCounter="+str(endCounter))
    
    relevantLineCheck= aspectParamsFileLine.rstrip("\n").lstrip().rstrip()

    #--- Replace blanks by the dot char.
    relevantLineCheck= sep.join(relevantLineCheck.split())
    
    print("relevantLineCheck="+relevantLineCheck)
    #sys.exit(0)

    if relevantLineCheck in relevantSubsectionsDict or relevantLine:
        
        relevantLine= True
        
        if relevantKey is None:
            relevantKey= relevantLineCheck

        relevantLineKey= relevantLineCheck.split("=")[0]
        
        print("OK: relevantLineCheck="+relevantLineCheck)
        #print("OK: item="+str(item))
        print("OK: relevantKey="+relevantKey)
        print("OK: relevantLineKey="+relevantLineKey)

        if relevantLineKey in relevantSubsectionsDict[relevantKey]:

            item= relevantLineCheck.split("=")[-1].split(",")
            
            print("item="+str(item))

            if len(item) > 1:
               relevantSubsectionsDict[relevantKey][relevantLineKey]= "".join(item).split(sep)[1:]
            else:
                relevantSubsectionsDict[relevantKey][relevantLineKey]= item[0].split(sep)[1]
            #relevantSubsectionsDict[relevantKey][relevantLineKey]= relevantLineCheck.split(sep)[-1].split(",")
            
            print("relevantSubsectionsDict="+str(relevantSubsectionsDict) )
            #sys.exit(0)

    if relevantLineCheck == "end":
        endCounter +=1

    if endCounter == 2: #and relevantLine:
        #print("endCounter == 2: reset control variables")
        relevantLine= False
        relevantKey= None
        endCounter= 0

    print("end line processing\n")    

#---
print("relevantSubsectionsDict="+str(relevantSubsectionsDict) )
#sys.exit(0)

geomDict= relevantSubsectionsDict["subsection"+sep+"Geometry"+sep+"model"]

print("geomDict="+str(geomDict))
#sys.exit(0)

xDim= geomDict["set"+sep+"X"+sep+"extent"+sep]
yDim= geomDict["set"+sep+"Y"+sep+"extent"+sep]

print("\nxDim="+xDim)
print("yDim="+yDim+"\n")
#sys.exit(0)

#--- nb. points : dim in meters, 1 point at every 1km
nbXPtsF= float(xDim)
nbYPtsF= float(yDim)

nbXPts= str(int(nbXPtsF/1e3))
nbYPts= str(int(nbYPtsF/1e3))

print("\nnbXPts="+nbXPts)
print("nbYPts="+nbYPts+"\n")

initCompoDict= relevantSubsectionsDict["subsection"+sep+"Initial"+sep+"composition"+sep+"model"]

print("initCompoDict="+str(initCompoDict))
#print("dir="+"set"+sep+ "Data" +sep+"directory"+sep)
#sys.exit(0)

initCompoFile= initCompoDict["set"+sep+ "Data" +sep+"directory"+sep]+"/"+initCompoDict["set"+sep+ "Data" +sep+"file" +sep+"name"+sep]

initTDict= relevantSubsectionsDict["subsection"+sep+"Initial"+sep+"temperature"+sep+"model"]
initTFile= initTDict["set"+sep+ "Data" +sep+"directory"+sep]+"/"+initTDict["set"+sep+ "Data" +sep+"file" +sep+"name"+sep]

print("\ninitCompoFile="+initCompoFile)
print("initTFile="+initTFile+"\n")
#sys.exit(0)

initTFp= open(initTFile,"w")
initCompoFp= open(initCompoFile,"w")

#--- nb. points : dim in meters, 1 point at every 1km
initTFp.write("# POINTS: "+nbXPts+" "+nbYPts+"\n")
initTFp.write("# Columns: x y temperature [K]\n")

initCompoFieldsDict= relevantSubsectionsDict["subsection"+sep+"Compositional"+sep+"fields"]
initCompoFieldsList= initCompoFieldsDict["set"+sep+"Names"+sep+ "of"+sep+"fields"+sep]

initCompoFp.write("# POINTS: "+nbXPts+" "+nbYPts+"\n")
initCompoFp.write("# Columns: x y "+ " ".join(initCompoFieldsList)+"\n")

#---
midXPoint= 750e3

MTZFloor= topLowMantleCeil= 30e3
MTZCeil= AAUMFloor= 290e3

oLithMtlFloor=670e3
oCrustFloor=692e3
oCrustThickness= nbYPtsF - oCrustFloor
oLithMtlThickness= oCrustFloor-oLithMtlFloor
oLithThickness= oLithMtlThickness+oLithMtlThickness

#wzXLen= 10e3
#wzYDepth= nbXPtsF-oLithFloor

#--- T data [K]
topLowMantleCeilT= MTZFloorT= 1725.0
topLowMantleFloorT= 1750.0

MTZCeilT= AAUMFloorT= 1700.0
AAUMCeilT= oLithMtlFloorT= 1650.0

oCrustFloorT= oLithMtlCeilT= 850 #moho

#SCLMFloorT= SOLMFloorT= AAUMCeilT

#--- Moho
#SCLMCeilT
#SOLMCeilT= OUCFloorT= 773.0

#CLCFloorT= SCLMCeilT
#CLCCeilT= CUCFloorT= 650.0

#CUCFloorT= CLCCeilT
#OSDFloorT= OUCCeilT= 400.0 

surfT= 273.0

composGeomDict= {
    "totalStrain": {
    "col": 2,
    "TCeil2Floor": [ [nbYPtsF, surfT], [oLithMtlFloor, oLithMtlFloorT]],
    "polygons": 
       [
         [  
          [midXPoint-oLithThickness,oLithMtlFloor],
          [midXPoint,oLithMtlFloor],
          [midXPoint,nbYPtsF]
         ],
         [  
          [midXPoint,oLithMtlFloor],
          [midXPoint,nbYPtsF],
          [midXPoint+oLithThickness,nbYPtsF]
         ]        
       ]
    },
    "oceanicCrust": {
        "col": 3,
        "TCeil2Floor": [ [nbYPtsF, surfT], [oCrustFloor, oCrustFloorT]],
        "polygons":
            [
              [
                [0.0,oCrustFloor],
                [0.0,nbYPtsF],
                [nbXPtsF,nbYPtsF],
                [nbXPtsF,oCrustFloor]
              ]
            ]
    },
   "oceanicLithMantle":  {
        "col": 4,
        "TCeil2Floor": [[oCrustFloor,oCrustFloorT], [oLithMtlFloor, oLithMtlFloorT ]],
        "polygons":
            [
                [
                  [0.0,oLithMtlFloor],
                  [0.0,oCrustFloor],
                  [nbXPtsF,oCrustFloor],
                  [nbXPtsF,oLithMtlFloor]
                ]
            ]
    },
    "asthenosphere": {
        "col": 5,
        "TCeil2Floor": [[oLithMtlFloor, AAUMCeilT], [AAUMFloor, AAUMFloorT]],
        "polygons":
            [
                [
                  [0.0,AAUMFloor],
                  [0.0,oLithMtlFloor],
                  [nbXPtsF,oLithMtlFloor],
                  [nbXPtsF,AAUMFloor]
                ]
            ] 
    }
}

#print(str(composGeomDict["SOLM"]))
#sys.exit(0)

#--- Need to have the same order for compo fields names in
#    both composGeomDict and initCompoFieldsList
assert tuple(composGeomDict.keys()) == tuple(initCompoFieldsList), \
    "Inconsistency between initCompoFieldsList and composGeomDict.keys():" + \
    " initCompoFieldsList="+str(initCompoFieldsList)+", composGeomDict.keys()="+str(tuple(composGeomDict.keys()))

composTemplate= ["0.0"]*(len(initCompoFieldsList)+1)

for y in range(0,int(nbYPts)):
   for x in range(0,int(nbXPts)):

      xmeters= float(x*1e3)
      ymeters= float(y*1e3)
       
      print("\nx,y="+str(x)+","+str(y))
       
      found= False 
      compoCounter= 2
      composLineList= [str(xmeters), str(ymeters)] +  composTemplate
      
      for compoField in composGeomDict:

         if found: break
          
         polygonPointsList= composGeomDict[compoField]["polygons"]

         print("\ncompoField="+compoField)
         #print("polygonPointsList="+str(polygonPointsList))
         
         for polygonPoints in polygonPointsList:
             
            #print("polygonPoints="+str(polygonPoints))
            
            nbVertices= len(polygonPoints)

            #print("nbVertices="+str(nbVertices))
            #sys.exit(0)

            pointInside= False
         
            if nbVertices == 3:
               pointInside= geom.pointInsideTriangle( (xmeters,ymeters), polygonPoints[0],polygonPoints[1],polygonPoints[2])
             
            else:
               pointInside= geom.insideRegBndBox(xmeters,ymeters,polygonPoints)

            #---   
            if pointInside:

               if compoField == "totalStrain"
                  composLineList[compoCounter] = math.uniform(0.5, 1.5)
               
               else :
                  composLineList[compoCounter] = "1.0"
               
               #print("\ncompoField="+compoField)
               print("pointInside: x,y in [km]="+str(x)+","+str(y))
               print("polygonPoints"+str(polygonPoints))
               print("composLineList="+str(composLineList))
               initCompoFp.write(" ".join(composLineList)+"\n")

               ceilElev,ceilT,= composGeomDict[compoField]["TCeil2Floor"][0]
               floorElev,floorT= composGeomDict[compoField]["TCeil2Floor"][1]
               
               TAtYElev= geom.getLinearTin2D(ceilT,
                                             floorT,
                                             ceilElev,
                                             floorElev,
                                             ymeters)

               print("composGeomDict[compoField][\"TCeil2Floor\"]="+str(composGeomDict[compoField]["TCeil2Floor"]))
               print("TAtYElev="+str(TAtYElev)+"\n")

               initTFp.write(str(xmeters)+" "+str(ymeters)+" "+str(TAtYElev)+"\n")
               
               #if compoField == "contLowCrust":
               #   sys.exit(0)

               #if compoCounter == 4:
               #   print("compoCounter==4") 
               #   sys.exit(0)
               
               #if nbVertices == 3:
               #   print("nbVertices==3") 
               #   sys.exit(0)

               #if compoField == "weakZone": sys.exit(0)
               #if compoField == "contSedsPrism": sys.exit(0)
               
               #--- found, break loop
               found= True
               break
               
         #--- if block
         
         compoCounter += 1    
         #--- 
      #---
      if not found:
          print("no compo found for (x,y)=("+str(x)+","+str(y)+")")
          sys.exit(0)
          
      #if (x==1225 and y==625): sys.exit(0)
   #---
#---

initTFp.close()
initCompoFp.close()

print("End script")
