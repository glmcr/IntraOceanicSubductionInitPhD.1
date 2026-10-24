#!/usr/bin/python3

import os
import sys
import vtk #.vtk
import glob
import math
import json
import numpy as np
import pathlib

aspectTopoFile= sys.argv[1]
xRidge= float(sys.argv[2])
horizVelo= float(sys.argv[3])
maxAge= float(sys.argv[4])
topoConvFileOut= sys.argv[5]

infile= open(aspectTopoFile,"r")
inlines= infile.readlines()
infile.close()

#csvFp= open(topoConvFileOut,"w")
#csvFp.write("#age[My],topo[m]")

topoAtAge= {}

for line in inlines[1:]:

    lineSplit= line.split(" ")

    #print("lineSplit="+str(lineSplit))
    #sys.exit(0)

    distFromLeftSide= float(lineSplit[0])

    if distFromLeftSide > xRidge:

        distFromRidge= distFromLeftSide - xRidge

        ageInYears= (distFromRidge/horizVelo)

        #print("ageInYears="+str(ageInYears))

        ageInMy= ageInYears/1e6

        #print("ageInMy="+str(ageInMy))

        ageInMyRd= round(math.floor(ageInMy+0.5))

        if ageInMyRd <= maxAge:

          if ageInMyRd not in topoAtAge:
              topoAtAge[ageInMyRd]= []
          # ---

          topoValue= float(lineSplit[2])

          topoAtAge[ageInMyRd].append(topoValue)
          
          #print("ageInMyRd="+str(ageInMyRd))
          #print("topoValue="+str(topoValue))
          #sys.exit(0)
          #csvFp.write(str(ageInMyRd)+","+str(float(lineSplit[2]))+"\n")
        # ---
# ---

csvFp= open(topoConvFileOut,"w")

csvFp.write("#age[My],topoAvg[m]\n")

for age in sorted(topoAtAge):

    print("age="+str(age))
    #sys.exit(0)      
    topoAvgAtAge= np.mean(topoAtAge[age])

    csvFp.write(str(age)+","+str(topoAvgAtAge)+"\n")
# ---
csvFp.close()

