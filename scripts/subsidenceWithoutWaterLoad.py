#!/usr/bin/python3

import os
import sys
#import vtk #.vtk
#import glob
import math

TLABatDistFromRidgeK= float(sys.argv[1])
TimeInMy= float(sys.argv[2])
N= int(sys.argv[3])

#zrNoWater= 1550.0
zrNoWater=1074.49
zp= 98500.0
#zp= 90000.0
T0K= 273.25

#rhoMantle= 3370.0
thermalExpOLMMrb= 3e-5
#thermalExpOLMMrb= 2.5e-5
thermalDiffOLMMrb= 1.07e-6
#thermalDiffOLMMrb= 2.14e-6

piSquared= math.pi**2
piSquaredInv= 1.0/piSquared

timeInSeconds= TimeInMy*86400*365

zpSquaredInv= 1.0/(zp**2)

checkConvInit= checkConv= 1.0 - 8.0*piSquaredInv*math.e**(-thermalDiffOLMMrb*piSquared*timeInSeconds*zpSquaredInv)

#print("checkConvInit="+str(checkConvInit))

epsilon= 1e-10

nbIter= 1

for i in range(1,N):

    itermSqu= (1.0+2.0*i)**2

    itermSquInv= 1.0/itermSqu

    checkConvIter= 1.0 - 8.0*piSquaredInv*itermSquInv*math.e**(-thermalDiffOLMMrb*piSquared*timeInSeconds*zpSquaredInv*itermSqu)

    #print("checkConvIter="+str(checkConvIter))

    nbIter += 1

    checkEpsilon= math.fabs(checkConvIter-checkConv)

    print("checkEpsilon="+str(checkEpsilon))
    
    if checkEpsilon < epsilon:
        break
    else :
        checkConv= checkConvIter
# ---

print("checkConvInit="+str(checkConv))
print("checkConv="+str(checkConv))
print("nbIter="+str(nbIter))

#print(" thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K)="+str( thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K)))

wtHalfPlateModel= zrNoWater + 0.5 * thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K) * zp * checkConv
#wtHalfPlateModel= zrNoWater + 1.0 * thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K) * zp * checkConv
                     
#wt= zrNoWater + 0.5 * math.fabs(thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K) -1.0) * zp * checkConv
#wt= zrNoWater + 0.5 *  zp * checkConv *(1.0/(1.0 - thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K)))

print("wtHalfPlateModel(m)="+str(wtHalfPlateModel))

wtHalfSpaceModel= zrNoWater + 2.0 * thermalExpOLMMrb * zp * math.sqrt( (thermalDiffOLMMrb*timeInSeconds)/math.pi )

print("2.0 * thermalExpOLMMrb * zp * math.sqrt( (thermalDiffOLMMrb*timeInSeconds)/math.pi )="+
      str(2.0 * thermalExpOLMMrb * zp * math.sqrt( (thermalDiffOLMMrb*timeInSeconds)/math.pi )))

print("wtHalfSpaceModel(m)="+str(wtHalfSpaceModel))
