#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import json
import numpy as np
import pathlib
from vtk.util.numpy_support import vtk_to_numpy

vtuFileIn= sys.argv[1]

csvFileOut= sys.argv[2]

spreadVeloMPY= 0.025 # meters/years 

#middlePointX= 1.48949e6 #1.49036e6
#middlePointX= 1.49036e6
#middlePointX= 1.495e6
middlePointX= 1.5e6
#leftLimitX= 500e3
rightLimitX= 3.0e6 - 500e3
#elevLimitY= 700e3-140e3
elevLimitY= 700e3- 98.5e3 #100e3
#elevLimitY= 700e3-65e3

oneMyInSeconds= 86400*365*1e6

mantleDensSTP=3370.0

# --- Create the vtk reader object.
reader= vtk.vtkXMLUnstructuredGridReader()

reader.SetFileName(vtuFileIn)
print("aft reader.SetFileName(vtuFileIn)")

reader.Update()
print("aft reader.Update()")

dataIn= reader.GetOutput()
print("aft reader.GetOutput()")

#TField= dataIn.GetPointData().GetArray("T")

olmMrbField= dataIn.GetPointData().GetArray("oceanicLithMantleMRB")

ocCrustMrbField= dataIn.GetPointData().GetArray("oceanicCrustMRB")

pmeltedMrbAsthField= dataIn.GetPointData().GetArray("pmeltedMrbAsth")

densityField= dataIn.GetPointData().GetArray("density")

sclmField= dataIn.GetPointData().GetArray("SCLM")

ocSedsField= dataIn.GetPointData().GetArray("oceanicSeds")

points= dataIn.GetPoints()

#TInfos= { 100.0: {}, 200.0: {}, 300.0: {},
#          400.0: {}, 500.0: {}, 600.0: {},
#          700.0: {}, 800.0: {}, 900.0: {},
#          1000.0: {}, 1100.0: {}, 1200.0: {}, 1300.0: {} }
#TInfosKeys= tuple(TInfos.keys())

densityInfo= {}
distInfo= {}
depthInfo= {}

#OLMInfo= {} #{ "oceanicLithMantleMRB": {}, "oceanicCrustMRB": {} }

for pointIdx in range(0,points.GetNumberOfPoints()):

    point= points.GetPoint(pointIdx)

    #print("point="+str(point))
    #sys.exit(0)

    # --- Only integrate from the middle point at ridge
    if point[0] < middlePointX or point[0] > rightLimitX or point[1] < elevLimitY:
        continue
    # ---

    distFromRidge= point[0] - middlePointX
    depth= 700e3-point[1]

    print("distFromRidge="+str(distFromRidge))
    print("depth="+str(depth))

    ageInYears= (distFromRidge/spreadVeloMPY)

    print("ageInYears="+str(ageInYears))

    ageInMy= ageInYears/1e6

    print("ageInMy="+str(ageInMy))

    ageInMyRd= round(ageInMy)

    if ageInMyRd not in distInfo:
        distInfo[ageInMyRd]= distFromRidge
    # ---
    
    #distFromRidgeRound= ageInMyRd*spreadVeloMPY)

    #checkT= TField.GetTuple(pointIdx)[0] - 273.0

    checkCrustMrb= ocCrustMrbField.GetTuple(pointIdx)[0]
    checkOlmMrb= olmMrbField.GetTuple(pointIdx)[0]
    checkPmeltedMrbAsth= pmeltedMrbAsthField.GetTuple(pointIdx)[0]
    densityThere= densityField.GetTuple(pointIdx)[0]
    checkSCLM= sclmField.GetTuple(pointIdx)[0]
    checkOcSeds= ocSedsField.GetTuple(pointIdx)[0]

    if checkOlmMrb > 0.5 or checkCrustMrb > 0.5 or checkPmeltedMrbAsth > 0.5 or checkSCLM > 0.5 or checkOcSeds > 0.5 :

        if ageInMyRd not in densityInfo:#OLMInfo:
            densityInfo[ageInMyRd]= {}
            
            #OLMInfo[ageInMyRd]= {"depths": [], "distKmFromRidge": None}

        if ageInMyRd not in depthInfo:
            depthInfo[ageInMyRd]= {}

        densityInfo[ageInMyRd][point[1]]= densityThere
        depthInfo[ageInMyRd][point[1]]= depth
        #densityInfo[ageInMyRd]["distFromRidge"]= distFromRidge
        
        #OLMInfo[ageInMyRd].append( -(depth/1000.0) )
        #OLMInfo[ageInMyRd].append({ "depthKM": -(depth/1000.0), "distKmFromRidge": distFromRidge })
        #OLMInfo[ageInMyRd].append( (-(depth/1000.0), distFromRidgeRound) )
        
    #if checkCrustMrb > 0.5:
    #    if ageInMyRd not in OLMInfp["oceanicCrustMRB"]:
    #       OLMInfp["oceanicCrustMRB"][ageInMyRd]= []       
    #    OLMInfp["oceanicCrustMRB"][ageInMyRd].append({ "depthKM": -(depth/1000.0), "distKmFromRidge": distFromRidge })
    
    #print("checkT="+str(checkT))

    #if checkT > 1300:
    #    continue
    # ---

    print("\npoint="+str(point))
    #print("checkT="+str(checkT))

    #distFromRidge= point[0] - middlePointX
    #depth= 700e3-point[1]
    #print("distFromRidge="+str(distFromRidge))
    #print("depth="+str(depth))
    #ageInYears= (distFromRidge/spreadVeloMPY)
    #print("ageInYears="+str(ageInYears))
    #ageInMy= ageInYears/1e6
    #print("ageInMy="+str(ageInMy))

    #depthsForTAtAges[ageInMy]= checkT
    

    # ---
# ---

sortedAges= sorted(tuple(densityInfo.keys()))
sortedElevsAge0= sorted(tuple(densityInfo[sortedAges[0]]))

print("sortedElevsAge0)="+str(sortedElevsAge0))
#sys.exit(0)

for age in sortedAges[1:]:

    checkElevs= sorted(tuple(densityInfo[age].keys()))

    print("len(checkElevs)="+str(len(checkElevs)))

    if len(checkElevs) < len(sortedElevsAge0):
        print("WARNING: len(checkElevs) < len(sortedElevsAge0) for age -> "+str(age)+", will ignore this age!!")

        sys.exit(0)
        del densityInfo[age]
        continue
    # ---

    #for checkElev in checkElevs:
    for elevAge0 in sortedElevsAge0:

        #if checkElev not in sortedElevsAge0:
        if elevAge0 not in checkElevs:

            #densityAtAge= densityInfo[age][checkElev]
            #del densityInfo[age][checkElev]
            
            #nearestAge0Elev= None
            nearestAgeElev= None
            minElevDist= 1e20

            #for elev in sortedElevsAge0:
            for checkElev in checkElevs:

                checkDist= math.fabs(elevAge0-checkElev)

                if checkDist < minElevDist:
                    nearestAge0Elev= checkElev
                    minElevDist= checkDist
            #---

            densityInfo[age][elevAge0]= densityInfo[age][nearestAge0Elev]

            #del densityInfo[age][nearestAge0Elev]
            
            #print("elevAge0="+str(elevAge0))
            #print("nearestAge0Elev="+str(nearestAge0Elev))
            #sys.exit(0)
            
            #del densityInfo[age][checkElev]
        # ---
    # ---

    checkElevsNb= len(tuple(densityInfo[age].keys()))

    print("checkElevsNb="+str(checkElevsNb))

    if checkElevsNb < len(sortedElevsAge0):
       print("ERROR!! cannot have checkElevsNb != len(sortedElevsAge0) here !! age -> "+str(age))
       #print("tuple(densityInfo[age].keys())="+str(tuple(densityInfo[age].keys())))
       sys.exit(1)

       del densityInfo[age]
    # ---
    else:
       print("Okay for age -> "+str(age))
       #sys.exit(0)
    # ---
# ---

#sys.exit(0)
             
densityDiffAccDict= {}

for age in sorted(tuple(densityInfo.keys())):

    #print("age="+str(age))
    
    #sortedElevs= sorted(tuple(densityInfo[age].keys()))

    #print("sortedElevs="+str(sortedElevs))

    #dz= sortedElevs[1]-sortedElevs[0]
    #densityDiffAcc= 0.5*(densityInfo[age][sortedElevs[0]]+densityInfo[age][sortedElevs[1]])*dz

    densityDiffAcc= 0.0

    #for elevIter in range(1,len(sortedElevs)):
    for elevIter in range(1,len(sortedElevsAge0)):

       dz= sortedElevsAge0[elevIter]-sortedElevsAge0[elevIter-1]

       if dz < 0.0:
           print("ERROR: dz cannot be < 0.0 here !!, elevIter="+str(elevIter))
           sys.exit(1)

       densityDiffAcc += 0.5*(densityInfo[age][sortedElevsAge0[elevIter]]+densityInfo[age][sortedElevsAge0[elevIter-1]])*dz

       #print("dz="+str(dz))
       #print("densityInfo[age][sortedElevs[elevIter]]="+str(densityInfo[age][sortedElevs[elevIter]]))
       #print("densityInfo[age][sortedElevs[elevIter-1]]="+str(densityInfo[age][sortedElevs[elevIter-1]]))      
       #print("densityDiffAcc="+str(densityDiffAcc))
       #sys.exit(0)
    # ---
    
    print("\nage="+str(age))
    print("densityDiffAcc="+str(densityDiffAcc))
    print("distInfo[age]="+str(distInfo[age]))
    #print("len(sortedElevs)="+str(len(sortedElevs)))
    #sys.exit(0)

    densityDiffAccDict[age]= densityDiffAcc
    
# ---
#sys.exit(0)

bathyAtRidge= 1e20

for elev in depthInfo[sortedAges[0]] :

    checkDepth= depthInfo[sortedAges[0]][elev]

    if checkDepth < bathyAtRidge:
        bathyAtRidge= checkDepth
    # ---
# ---

print("bathyAtRidge="+str(bathyAtRidge))

bathyAtAge= {0: bathyAtRidge}

for age in sortedAges[1:]:

    bathyAtAge[age]= bathyAtRidge + (1.0/mantleDensSTP)*(densityDiffAccDict[age]-densityDiffAccDict[0])

    print("age="+str(age)+", bathyAtAge[age]="+str(bathyAtAge[age]))
# ---
#print("depthInfo[sortedAges[0]]="+str(depthInfo[sortedAges[0]]))
sys.exit(0)

for Tc in TInfosKeys:

    csvFp= open(str(Tc)+"-"+csvFileOut,"w")

    #print("Tc="+str(Tc)+", nb. ages="+str(len( TInfos[Tc])))

    csvFp.write("#age[My],depth(Km), distFromRidge(Km)\n")

    for age in sorted(TInfos[Tc]):
        #print("age="+str(age)+",nb. depths="+str(len( TInfos[Tc][age])))

        avgDepthAtAgeAcc= 0.0

        for dictItem in TInfos[Tc][age]:
            avgDepthAtAgeAcc += dictItem["depthKM"]

        avgDepthAtAge= avgDepthAtAgeAcc/float(len(TInfos[Tc][age]))

        distKmFromRidge= (age*1e6*spreadVeloMPY)/1000.0

        csvFp.write(str(age)+","+str(avgDepthAtAge)+","+str(distKmFromRidge)+"\n")
    # ---
    #for TcInfo in TInfos[Tc] :
    #    csvFp.write(str(TcInfo["ageInMy"])+","+str(TcInfo["depthKM"])+","+str(TcInfo["distKmFromRidge"])+"\n")
    csvFp.close()
    #sys.exit(0)
# ---

csvFp2= open("LABDepths-"+csvFileOut,"w")

csvFp2.write("#age[My],depth(Km), distFromRidge(Km)\n")

for age in sorted(OLMInfo.keys()):

    #print("age="+str(age)+", sorted(OLMInfo[age])[-1]="+str(sorted(OLMInfo[age])[-1]))
    
    maxDepthKm= sorted(OLMInfo[age])[0]

    distKmFromRidge=(age*1e6*spreadVeloMPY)/1000.0

    csvFp2.write(str(age)+","+str(maxDepthKm)+","+str(distKmFromRidge)+"\n")

csvFp2.close()
                           
del reader
#csvFp.close()
