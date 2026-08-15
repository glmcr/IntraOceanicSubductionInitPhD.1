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

middlePointX= 1.49036e6
#leftLimitX= 500e3
rightLimitX= 3.0e6 - 500e3
elevLimitY= 700e3-140e3

oneMyInSeconds= 86400*365*1e6

# --- Create the vtk reader object.
reader= vtk.vtkXMLUnstructuredGridReader()

reader.SetFileName(vtuFileIn)
print("aft reader.SetFileName(vtuFileIn)")

reader.Update()
print("aft reader.Update()")

dataIn= reader.GetOutput()
print("aft reader.GetOutput()")

TField= dataIn.GetPointData().GetArray("T")

olmMrbField= dataIn.GetPointData().GetArray("oceanicLithMantleMRB")

ocCrustMrbField= dataIn.GetPointData().GetArray("oceanicCrustMRB")

points= dataIn.GetPoints()

TInfos= { 100.0: {}, 200.0: {}, 300.0: {},
          400.0: {}, 500.0: {}, 600.0: {},
          700.0: {}, 800.0: {}, 900.0: {},
          1000.0: {}, 1100.0: {}, 1200.0: {}, 1300.0: {} }

TInfosKeys= tuple(TInfos.keys())

OLMInfo= {} #{ "oceanicLithMantleMRB": {}, "oceanicCrustMRB": {} }

for pointIdx in range(0,points.GetNumberOfPoints()):

    point= points.GetPoint(pointIdx)

    #print("point="+str(point))
    #sys.exit(0)

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

    #distFromRidgeRound= ageInMyRd*spreadVeloMPY)

    checkT= TField.GetTuple(pointIdx)[0] - 273.0

    checkCrustMrb= ocCrustMrbField.GetTuple(pointIdx)[0]
    checkOlmMrb= olmMrbField.GetTuple(pointIdx)[0]

    if checkOlmMrb > 0.5 or checkCrustMrb > 0.5 :

        if ageInMyRd not in OLMInfo:
            OLMInfo[ageInMyRd]= []
            #OLMInfo[ageInMyRd]= {"depths": [], "distKmFromRidge": None}

        OLMInfo[ageInMyRd].append( -(depth/1000.0) )
        #OLMInfo[ageInMyRd].append({ "depthKM": -(depth/1000.0), "distKmFromRidge": distFromRidge })
        #OLMInfo[ageInMyRd].append( (-(depth/1000.0), distFromRidgeRound) )
        
    #if checkCrustMrb > 0.5:
    #    if ageInMyRd not in OLMInfp["oceanicCrustMRB"]:
    #       OLMInfp["oceanicCrustMRB"][ageInMyRd]= []       
    #    OLMInfp["oceanicCrustMRB"][ageInMyRd].append({ "depthKM": -(depth/1000.0), "distKmFromRidge": distFromRidge })
    
    #print("checkT="+str(checkT))

    if checkT > 1300:
        continue
    # ---

    print("\npoint="+str(point))
    print("checkT="+str(checkT))

    #distFromRidge= point[0] - middlePointX
    #depth= 700e3-point[1]
    #print("distFromRidge="+str(distFromRidge))
    #print("depth="+str(depth))
    #ageInYears= (distFromRidge/spreadVeloMPY)
    #print("ageInYears="+str(ageInYears))
    #ageInMy= ageInYears/1e6
    #print("ageInMy="+str(ageInMy))

    #depthsForTAtAges[ageInMy]= checkT

    for Tc in TInfosKeys:

        TDiffCheck= math.fabs(Tc-checkT)

        if TDiffCheck < 5.0: #10.0: #20.0: #10.0: #5.0:

            #ageInMyFloor= math.floor(ageInMy)
            #ageInMyStr= str(round(ageInMy))
            #ageInMyRd= round(ageInMy)

            if ageInMyRd not in TInfos[Tc]:
                  TInfos[Tc][ageInMyRd]= []
            # ---
            
            TInfos[Tc][ageInMyRd].append({ "depthKM": -(depth/1000.0), "distKmFromRidge": (ageInMyRd*1e6*spreadVeloMPY)/1000.0 })

        # ---
        
            #TInfos[Tc].append({ "ageInMy": math.floor(ageInMy), "depthKM": -(depth/1000.0), "distKmFromRidge": distFromRidge })
            #print("TInfos="+str(TInfos))
            #sys.exit(0)
        # ---
    # ---
# ---

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
