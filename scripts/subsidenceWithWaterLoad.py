#!/usr/bin/python3

import os
import sys
#import vtk #.vtk
#import glob
import math

TLABatDistFromRidgeK= float(sys.argv[1])
TimeInMy= float(sys.argv[2])
N= int(sys.argv[3])

zrWithWater= 2500.0 #1550.0
zp= 98500.0
T0K= 273.25

rhoSeaWater= 1025.0
rhoMantle= 3300.0 #3370.0
thermalExpOLMMrb= 3e-5
thermalDiffOLMMrb= 1.07e-6

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

wt= zrWithWater + (0.5 * thermalExpOLMMrb * (TLABatDistFromRidgeK-T0K) * zp * checkConv)*(rhoMantle/(rhoMantle-rhoSeaWater))

print("wt(m)="+str(wt))
