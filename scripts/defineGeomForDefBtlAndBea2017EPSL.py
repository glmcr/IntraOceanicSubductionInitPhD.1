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
    
    #print("relevantLineCheck="+relevantLineCheck)
    #sys.exit(0)

    if relevantLineCheck in relevantSubsectionsDict or relevantLine:
        
        relevantLine= True
        
        if relevantKey is None:
            relevantKey= relevantLineCheck

        relevantLineKey= relevantLineCheck.split("=")[0]
        
        #print("OK: relevantLineCheck="+relevantLineCheck)
        #print("OK: relevantKey="+relevantKey)
        #print("OK: relevantLineKey="+relevantLineKey)

        if relevantLineKey in relevantSubsectionsDict[relevantKey]:
            
            relevantSubsectionsDict[relevantKey][relevantLineKey]= relevantLineCheck.split(sep)[-1].split(",")
            
            #print("relevantSubsectionsDict="+str(relevantSubsectionsDict) )
            #sys.exit(0)

    if relevantLineCheck == "end":
        endCounter +=1

    if endCounter == 2: #and relevantLine:
        #print("endCounter == 2: reset control variables")
        relevantLine= False
        relevantKey= None
        endCounter= 0

    #print("end line processing\n")    

#---
print("relevantSubsectionsDict="+str(relevantSubsectionsDict) )

geomDict= relevantSubsectionsDict["subsection"+sep+"Geometry"+sep+"model"]

#print("geomDict="+str(geomDict))
#sys.exit(0)

xDim= geomDict["set"+sep+"X"+sep+"extent"+sep][0]
yDim= geomDict["set"+sep+"Y"+sep+"extent"+sep][0]

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
initCompoFile= initCompoDict["set"+sep+ "Data" +sep+"directory"+sep][0]+"/"+initCompoDict["set"+sep+ "Data" +sep+"file" +sep+"name"+sep][0]

initTDict= relevantSubsectionsDict["subsection"+sep+"Initial"+sep+"temperature"+sep+"model"]
initTFile= initTDict["set"+sep+ "Data" +sep+"directory"+sep][0]+"/"+initTDict["set"+sep+ "Data" +sep+"file" +sep+"name"+sep][0]

print("\ninitCompoFile="+initCompoFile)
print("initTFile="+initTFile+"\n")

initTFp= open(initTFile,"w")
initCompoFp= open(initCompoFile,"w")

#--- nb. points : dim in meters, 1 point at every 1km
initTFp.write("# POINTS: "+nbXPts+" "+nbYPts+"\n")
initTFp.write("# Columns: x y temperature [K]\n")

initCompoFieldsDict= relevantSubsectionsDict["subsection"+sep+"Compositional"+sep+"fields"]
initCompoFieldsList= initCompoFieldsDict["set"+sep+"Names"+sep+ "of"+sep+"fields"+sep]

initCompoFp.write("# POINTS: "+nbXPts+" "+nbYPts+"\n")
initCompoFp.write("# Columns: x y "+ " ".join(initCompoFieldsList)+"\n")

#--- lthos-asthenos bnd: 120km
#LABDepth= 90.0 # yDim - 610.0
#LABDOLith=90e3
#LABDClLith= 120e3 # yDim - 610.0

#--- contact position between continental and oceanic domains: 1200km
contVsOcean= 1200e3

OSDThkn= 3e3
OSDCeil= nbYPtsF 
OSDFloor= OSDCeil - OSDThkn

OUCThkn= 9e3
OUCCeil= OSDFloor
OUCFloor= OUCCeil - OUCThkn

CSPWidth= 15e3
CSPThkn= 12e3
CSPCeil= nbYPtsF
CSPFloor= CSPCeil-CSPThkn

#contUppCrustThkn= 30.0 # 700 - 670
CUCThkn= 30e3 # 700 - 670
CUCCeil= nbYPtsF
CUCFloor= CUCCeil - CUCThkn

#contLowCrustThkn= 10.0 # 670 - 660
CLCThkn= 10e3 # 670 - 660
CLCCeil= CUCFloor
CLCFloor= CLCCeil - CLCThkn

wZBlocWidth= CUCThkn - CLCThkn

SCLMThkn= 50e3 # 660 - 610
SCLMCeil= CLCFloor
SCLMFloor= SCLMCeil - SCLMThkn

#--- 2nd SCLM sector under the 1st
SCLM2Thkn= 30e3
SCLM2Ceil= SCLMFloor
SCLM2Floor= SCLM2Ceil - SCLM2Thkn

#--- T data [K]
AAUMCeilT= 1650.0
AAUMFloorT= 1750.0

SCLMFloorT= SOLMFloorT= AAUMCeilT

#--- Moho
SCLMCeilT= SOLMCeilT= OUCFloorT= CSPFloorT= 773.0

CLCFloorT= SCLMCeilT
CLCCeilT= CUCFloorT= 650.0

CUCFloorT= CLCCeilT

OSDFloorT= OUCCeilT= 400.0 

surfT= 273.0

composGeomDict= {

    "AAUM": {
        "col": 2,
        "TCeil2Floor": [[SCLMFloor, AAUMCeilT], [0.0, AAUMFloorT]],
        "polygons":
            [ [ [contVsOcean+(SCLMThkn-SCLM2Thkn),SCLM2Floor],[contVsOcean+SCLMThkn,SCLM2Ceil],[contVsOcean+SCLMThkn,SCLM2Floor] ],
              [ [contVsOcean+SCLMThkn,SCLM2Floor],[contVsOcean+SCLMThkn,SCLM2Ceil],[nbXPtsF,SCLM2Ceil],[nbXPtsF,SCLM2Floor] ],
              #[ [0.0,SCLM2Floor],[0.0,SCLM2Ceil],[contVsOcean-SCLM2Thkn,SCLM2Ceil],[contVsOcean-SCLM2Thkn,SCLM2Floor] ],
              [ [0.0,0.0],[0.0,SCLM2Floor],[nbXPtsF,SCLM2Floor],[nbXPtsF,0.0] ] ] 
    },
    "SCLM": {
        "col": 3,
        "TCeil2Floor": [[ SCLMCeil, SCLMCeilT], [SCLM2Floor,SCLMFloorT]],
        "polygons": 
            [ #SCLM2
              [ [contVsOcean-SCLM2Thkn,SCLM2Floor],[contVsOcean-SCLM2Thkn,SCLM2Ceil],[contVsOcean,SCLM2Ceil] ],
              [ [0.0,SCLM2Floor],[0.0,SCLM2Ceil],[contVsOcean-SCLM2Thkn,SCLM2Ceil],[contVsOcean-SCLM2Thkn,SCLM2Floor] ],

              #SCLM
              [ [contVsOcean,SCLMFloor],[contVsOcean,SCLMCeil],[contVsOcean+SCLMThkn,SCLMCeil] ], 
              [ [0.0,SCLMFloor],[0.0,SCLMCeil],[contVsOcean,SCLMCeil],[contVsOcean,SCLMFloor] ] ] 
    },
    "contLowCrust": {
        "col": 4,
        "TCeil2Floor": [ [CLCCeil, CLCCeilT], [CLCFloor, CLCFloorT]],
        "polygons": 
            [ [ [contVsOcean+SCLMThkn,CLCFloor],[contVsOcean+SCLMThkn,CLCCeil],[contVsOcean+SCLMThkn+CLCThkn,CLCCeil] ],
              [ [0.0,CLCFloor],[0.0,CLCCeil],[contVsOcean+SCLMThkn,CLCCeil],[contVsOcean+SCLMThkn,CLCFloor] ] ]  
    },
    "contUppCrust":{
        "col": 5,
        "TCeil2Floor": [[nbYPtsF,surfT], [CUCFloor,CUCFloorT]],
        "polygons":
            [ [ [contVsOcean+SCLMThkn+CLCThkn,CUCFloor],[contVsOcean+SCLMThkn+CLCThkn,CUCCeil],[contVsOcean+SCLMThkn+CLCThkn+CUCThkn,CUCCeil] ],
              [ [0.0,CUCFloor],[0.0,CUCCeil],[contVsOcean+SCLMThkn+CLCThkn,CUCCeil],[contVsOcean+SCLMThkn+CLCThkn,CUCFloor] ] ]
    },
    "contSedsPrism": {
        "col": 6,
        "TCeil2Floor": [[ nbYPtsF, surfT], [CSPFloor,CSPFloorT]],
        "polygons":
             [ [ [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth-CSPThkn,CSPFloor],[contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,CSPCeil],
                 [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,CSPFloor] ],
               
               [ [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,CSPFloor],[contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,CSPCeil],
                 [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth+CSPWidth,CSPCeil], [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth+CSPWidth,CSPFloor] ] ]
    },
    "SOLM":  {
        "col": 7,
        "TCeil2Floor": [[OUCFloor, SOLMCeilT], [SCLMFloor,SOLMFloorT ]],
        "polygons":
            [ [ [contVsOcean+SCLMThkn,SCLMFloor],[contVsOcean+2*SCLMThkn,SCLMCeil],[contVsOcean+2*SCLMThkn,SCLMFloor] ],
              [ [contVsOcean+2*SCLMThkn,SCLMFloor],[contVsOcean+2*SCLMThkn,SCLMCeil],[nbXPtsF,SCLMCeil],[nbXPtsF,SCLMFloor] ],
        
              [ [contVsOcean+2*SCLMThkn,CLCFloor],[contVsOcean+2*SCLMThkn+CLCThkn,CLCCeil],[contVsOcean+2*SCLMThkn+CLCThkn,CLCFloor] ],
              [ [contVsOcean+2*SCLMThkn+CLCThkn,CLCFloor],[contVsOcean+2*SCLMThkn+CLCThkn,CLCCeil],[nbXPtsF,CLCCeil],[nbXPtsF,CLCFloor] ],

              [ [contVsOcean+2*SCLMThkn+CLCThkn,CUCFloor],[contVsOcean+2*SCLMThkn+CLCThkn+(CSPFloor-CUCFloor),CSPFloor],
                [contVsOcean+2*SCLMThkn+CLCThkn+(CSPFloor-CUCFloor),CUCFloor] ],
              
              [ [contVsOcean+2*SCLMThkn+CLCThkn+(CSPFloor-CUCFloor),CUCFloor],[contVsOcean+2*SCLMThkn+CLCThkn+(CSPFloor-CUCFloor),CSPFloor],
                [nbXPtsF,CSPFloor],[nbXPtsF,CUCFloor] ] ]
    },
    "oceanicUppCrust": {
        "col": 8,
        "TCeil2Floor": [ [ OUCCeil, OUCCeilT], [OUCFloor, OUCFloorT]],
        "polygons":
            [ [ [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,OUCFloor],[contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,OUCCeil],
                [nbXPtsF,OUCCeil],[nbXPtsF,OUCFloor] ] ]
    },
    "oceanicSeds": {
        "col": 9,
        "TCeil2Floor": [ [nbYPtsF, surfT], [OSDFloor, OSDFloorT]],
        "polygons":
           [ [ [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,OSDFloor],[contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,OSDCeil],
               [nbXPtsF,OSDCeil],[nbXPtsF,OSDFloor] ] ]
    },
    "weakZone": {
        "col": 10,
        "TCeil2Floor": [ [nbYPtsF, surfT], [SCLM2Floor,SCLMFloorT] ],
        "polygons":
            [ #SCLM2 depths
                [ [contVsOcean-SCLM2Thkn,SCLM2Floor], [contVsOcean,SCLM2Ceil], [contVsOcean,SCLM2Floor] ],
                [ [contVsOcean,SCLM2Floor], [contVsOcean,SCLM2Ceil], [contVsOcean+(SCLMThkn-SCLM2Thkn),SCLM2Ceil], [contVsOcean+(SCLMThkn-SCLM2Thkn),SCLM2Floor] ],
                [ [contVsOcean+(SCLMThkn-SCLM2Thkn),SCLM2Floor], [contVsOcean+(SCLMThkn-SCLM2Thkn),SCLM2Ceil], [contVsOcean+SCLMThkn,SCLM2Ceil] ] ,

              #SCLM depts (only triangles)
              [ [contVsOcean,SCLMFloor],[contVsOcean+SCLMThkn,SCLMCeil],[contVsOcean+SCLMThkn,SCLMFloor] ],
              [ [contVsOcean+SCLMThkn,SCLMFloor],[contVsOcean+SCLMThkn,SCLMCeil],[contVsOcean+2*SCLMThkn,SCLMCeil] ],
        
              [ [contVsOcean+SCLMThkn,CLCFloor],[contVsOcean+SCLMThkn+CLCThkn,CLCCeil],[contVsOcean+SCLMThkn+CLCThkn,CLCFloor] ],

              # Rect block between triangles, CLC depths
              [ [contVsOcean+SCLMThkn,CLCFloor], [contVsOcean+SCLMThkn,CLCCeil], [contVsOcean+2*SCLMThkn,CLCCeil],[contVsOcean+2*SCLMThkn,CLCFloor] ],
              
              [ [contVsOcean+2*SCLMThkn,CLCFloor],[contVsOcean+2*SCLMThkn,CLCCeil],[contVsOcean+2*SCLMThkn+CLCThkn,CLCCeil]],

              [ [contVsOcean+SCLMThkn+CLCThkn,CUCFloor],[contVsOcean+SCLMThkn+CLCThkn+CUCThkn,CUCCeil],[contVsOcean+SCLMThkn+CLCThkn+CUCThkn,CUCFloor] ],

              # Rect block between triangles, CUC depths
              [ [contVsOcean+SCLMThkn+CLCThkn+CUCThkn,CUCFloor],[contVsOcean+SCLMThkn+CLCThkn+CUCThkn,CUCCeil],[contVsOcean+SCLMThkn+CLCThkn+CUCThkn+wZBlocWidth,CUCCeil],
                [contVsOcean+SCLMThkn+CLCThkn+CUCThkn+wZBlocWidth,CUCFloor] ],
              
              [ [contVsOcean+SCLMThkn+CLCThkn+CUCThkn+wZBlocWidth,CUCFloor],[contVsOcean+SCLMThkn+CLCThkn+CUCThkn+wZBlocWidth,CUCCeil],
                [contVsOcean+SCLMThkn+CLCThkn+2*CUCThkn+wZBlocWidth,CUCCeil] ] ]
    }    
}

#print(str(composGeomDict["SOLM"]))
#sys.exit(0)

#--- Need to have the same order for compo fields names in
#    both composGeomDict and initCompoFieldsList
assert tuple(composGeomDict.keys()) == tuple(initCompoFieldsList), \
    "Inconsistency between initCompoFieldsList and composGeomDict.keys():" + \
    " initCompoFieldsList="+str(initCompoFieldsList)+", composGeomDict.keys()="+str(tuple(composGeomDict.keys()))

composTemplate= ["0.0"]*len(initCompoFieldsList)

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
