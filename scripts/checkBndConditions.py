#!/usr/bin/python3

import sys

velcmyLHS= -1.0
velcmyRHS= 1.0
cm2m=0.01
year=1
bottomDepth=700e3
xdim= 1500e3

switchDepthRHS=40e3
switchDepthLHS=40e3

#switchDepthRHS=140e3
#switchDepthLHS=140e3

#maxDepth= 700e3
nbCellsY= 700

csvFileName= sys.argv[1]

csvFile= open(csvFileName,"w")

csvFile.write("#lhsXVelo,rhsXVelo,yElev\n")

for cellY in range(700):

    y= cellY*1000.0

    lhsXVelo=rhsXVelo= 0.0
    
    if (y > (bottomDepth-switchDepthRHS)):
        rhsXVelo= velcmyRHS*(cm2m/year)
        
    elif ( y >= (bottomDepth-switchDepthRHS-20e3)):
        rhsXVelo= velcmyRHS*(cm2m/year)*((y - (bottomDepth-switchDepthRHS-20e3))*35.0)/bottomDepth

    elif ( y >= (bottomDepth-switchDepthRHS-40e3)):
        #lhsXVelo= 0.01*velcmyLHS*(cm2m/year)*((y - (bottomDepth-switchDepthLHS-20e3))*35.0)/bottomDepth
        rhsXVelo= 0.1*velcmyLHS*(cm2m/year)*(((bottomDepth-switchDepthRHS-20e3)-y)*35.0)/bottomDepth
        
    else:
        #rhsXVelo= -5e-3*velcmyRHS*(cm2m/year)
        rhsXVelo= -0.1*velcmyRHS*(cm2m/year)

    if (y > (bottomDepth-switchDepthLHS)):
        lhsXVelo= velcmyLHS*(cm2m/year)
        
    elif ( y >= (bottomDepth-switchDepthLHS-20e3)):
        lhsXVelo= velcmyLHS*(cm2m/year)*((y - (bottomDepth-switchDepthLHS-20e3))*35.0)/bottomDepth

    elif ( y >= (bottomDepth-switchDepthLHS-40e3)):
        #lhsXVelo= 0.01*velcmyLHS*(cm2m/year)*((y - (bottomDepth-switchDepthLHS-20e3))*35.0)/bottomDepth
        lhsXVelo= 0.1*velcmyLHS*(cm2m/year)*(((bottomDepth-switchDepthLHS-20e3)-y)*35.0)/bottomDepth

    else:     
        #lhsXVelo= -5e-3*velcmyLHS*(cm2m/year)
        lhsXVelo= -0.1*velcmyLHS*(cm2m/year)

    csvFile.write(str(lhsXVelo)+","+str(rhsXVelo)+","+str(y)+"\n")
# ---
           
csvFile.close()
    
    
