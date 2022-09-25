#!/usr/bin/python3

import sys
import math

# convergence
velcmyLHS= 3.5
velcmyRHS= -3.5

# extension
#velcmyLHS= -2.0
#velcmyRHS= 2.0

cm2m=0.01
year=1
bottomDepth=700e3
xdim= 1500e3

#switchDepthRHS=40e3
#switchDepthLHS=40e3

switchDepthRHS=45e3
switchDepthLHS=45e3

#switchDepthRHS=50e3
#switchDepthLHS=50e3

#switchDepthRHS=80e3
#switchDepthLHS=80e3

#maxDepth= 700e3
nbCellsY= 700

csvFileName= sys.argv[1]

csvFile= open(csvFileName,"w")

rhsVeloAccIn= 0.0
lhsVeloAccIn= 0.0

rhsVeloAccOut= 0.0
lhsVeloAccOut= 0.0

cellSide= 1 #1000.0

#bFact= -0.0785
#bFact= -0.078525
#bFact= -0.0785245
#bFact= -0.0785235
#bFact= -0.0785225
#bFact= -0.078522
#bFact= -0.078521
#bFact= -0.07852
#bFact= -0.078519
#bFact= -0.078518
#bFact= -0.078517
bFact= -0.078516
bFact= -0.078515
bFact= -0.078512
bFact= -0.078509
bFact= -0.0785091
bFact= -0.07850912
bFact= -0.07850911
bFact= -0.07850905
bFact= -0.07850907
bFact= -0.07850909
bFact= -0.07850912 # < 4.800014413719467e-09
bFact= -0.0785091195 # < 4.657486812886802e-09
bFact= -0.0785091197 # < 8.74514433091278e-10
bFact= -0.07850911971 # < 6.853730638578526e-10
bFact= -0.07850911972 # < 4.962081578963051e-10
bFact= -0.07850911973 # < 3.0706234777078123e-10
bFact= -0.07850911975 # < 7.126413348323979e-11
bFact= -0.078509119745 # < 2.3329310705477724e-11
bFact= -0.078509119746 # < 4.420436239271908e-12
bFact= -0.0785091197462 # < 6.396827512133996e-13
bFact= -0.07850911974621 # < 4.1763814628836826e-13
bFact= -0.07850911974625 # < 3.2776559244496184e-13
bFact= -0.07850911974623 # < 7.813194535799539e-14
bFact= -0.07850911974623428 # 40km

#40km bFact=  -0.07850911974623428
#45km bFact= -0.08713029576339054
#80km bFact= -0.1515664690939903  

dFact= 35.0
#dFact= 70.0

csvFile.write("#lhsXVelo,rhsXVelo,yElev\n")

for cellY in range(700):

    y= cellY*1000.0

    lhsXVelo=rhsXVelo= 0.0
    
    if (y > (bottomDepth-switchDepthRHS)):
        rhsXVelo= velcmyRHS*(cm2m/year)
        rhsVeloAccIn += rhsXVelo*cellSide
        
    elif ( y >= (bottomDepth-switchDepthRHS-20e3)):
        rhsXVelo= velcmyRHS*(cm2m/year)*((y - (bottomDepth-switchDepthRHS-20e3))*dFact)/bottomDepth
        rhsVeloAccIn += rhsXVelo*cellSide

    elif ( y >= (bottomDepth-switchDepthRHS-40e3)):
        #rhsXVelo= bFact*velcmyRHS*(cm2m/year)*(((bottomDepth-switchDepthRHS-20e3)-y)*dFact)/bottomDepth
        rhsXVelo= velcmyRHS*(cm2m/year)*(((bottomDepth-switchDepthRHS-20e3)-y)*dFact)/bottomDepth
        rhsVeloAccOut += rhsXVelo*cellSide
        rhsXVelo *= -1
        
    else:
        #rhsXVelo= -5e-3*velcmyRHS*(cm2m/year)
        #rhsXVelo= bFact*velcmyRHS*(cm2m/year)
        rhsXVelo= velcmyRHS*(cm2m/year)
        rhsVeloAccOut += rhsXVelo*cellSide
        rhsXVelo *= -1
        
    if (y > (bottomDepth-switchDepthLHS)):
        lhsXVelo= velcmyLHS*(cm2m/year)
        lhsVeloAccIn += lhsXVelo*cellSide
        
    elif ( y >= (bottomDepth-switchDepthLHS-20e3)):
        lhsXVelo= velcmyLHS*(cm2m/year)*((y - (bottomDepth-switchDepthLHS-20e3))*dFact)/bottomDepth
        lhsVeloAccIn += lhsXVelo*cellSide
        
    elif ( y >= (bottomDepth-switchDepthLHS-40e3)):
        #lhsXVelo= bFact*velcmyLHS*(cm2m/year)*(((bottomDepth-switchDepthLHS-20e3)-y)*dFact)/bottomDepth
        lhsXVelo= velcmyLHS*(cm2m/year)*(((bottomDepth-switchDepthLHS-20e3)-y)*dFact)/bottomDepth
        lhsVeloAccOut += lhsXVelo*cellSide
        lhsXVelo *= -1
        
    else:     
        #lhsXVelo= -5e-3*velcmyLHS*(cm2m/year)
        #lhsXVelo= bFact*velcmyLHS*(cm2m/year)
        lhsXVelo= velcmyLHS*(cm2m/year)
        lhsVeloAccOut += lhsXVelo*cellSide
        lhsXVelo *= -1
        
    csvFile.write(str(lhsXVelo)+","+str(rhsXVelo)+","+str(y)+"\n")
# ---

print("lhsVeloAccIn="+str(lhsVeloAccIn))
print("lhsVeloAccOut="+str(lhsVeloAccOut))
print("rhsVeloAccIn="+str(rhsVeloAccIn))
print("rhsVeloAccOut="+str(rhsVeloAccOut))

#   lhsVeloAccIn + lhsBFact*lhsVeloAccOut = 0.0
#   lhsBFact = -lhsVeloAccIn/lhsVeloAccOut

lhsBFact = -lhsVeloAccIn/lhsVeloAccOut
rhsBFact = -rhsVeloAccIn/rhsVeloAccOut

print("lhsBFact="+str(lhsBFact))
print("rhsBFact="+str(rhsBFact))

csvFile.close()
    
    
