import os,sys,math
import numpy

_epsilon= 1e-25
_minus_epsilon= -_epsilon

#---
def crossProd2D(v2D1: tuple,v2D2: tuple) -> float:

    #--- The cross product of two 2D vectors in the (i,j)
    #    plane produce a vector which is in the (k) dimension  
    #   (i1,j1,0) x (i2,j2,0) = (0,0,i1*j2 - i2*j1)

    return v2D1[0]*v2D2[1] - v2D1[1]*v2D2[0]

#---
def pointInsideTriangle(point2D: tuple, vertex1: tuple, vertex2: tuple, vertex3: tuple) -> bool:

    #print("pointInsideTriangle: point2D="+str(point2D))
    #print("pointInsideTriangle: vertex1="+str(vertex1))
    #print("pointInsideTriangle: vertex2="+str(vertex2))
    #print("pointInsideTriangle: vertex3="+str(vertex3))
    
    denom= crossProd2D(vertex1,vertex2) + crossProd2D(vertex2,vertex3) + crossProd2D(vertex3,vertex1)

    #print("denom="+str(denom))
    
    ret= False

    if math.fabs(denom) > _epsilon : #1e-15:

        v1MinusV2= ( vertex1[0]-vertex2[0], vertex1[1]-vertex2[1])
        v3MinusV1= ( vertex3[0]-vertex1[0], vertex3[1]-vertex1[1])
        v2MinusV3= ( vertex2[0]-vertex3[0], vertex2[1]-vertex3[1])
        
        weight12= ( crossProd2D(vertex1,vertex2) + crossProd2D(point2D,v1MinusV2) )/denom
        weight31= ( crossProd2D(vertex3,vertex1) + crossProd2D(point2D,v3MinusV1) )/denom
        weight23= ( crossProd2D(vertex2,vertex3) + crossProd2D(point2D,v2MinusV3) )/denom            

        #print("weight12="+str(weight12))
        #print("weight31="+str(weight31))
        #print("weight23="+str(weight23))

        #--- TODO: use a floor() and ceil() instead
        #    of this clumsy float comparison?: 
        #if ( 0.0 <= weight12 and weight12 <= 1.0) \
        #   and ( 0.0 <= weight31 and weight31 <= 1.0) \
        #       and ( 0.0 <= weight23 and weight23 <= 1.0) : ret = True
        
        if ( weight12 > _minus_epsilon or math.ceil(weight12) == 1) \
           and ( weight31 > _minus_epsilon or math.ceil(weight31) == 1 ) \
               and ( weight23 > _minus_epsilon or math.ceil(weight23) == 1 ) : ret = True
        
    #---    

    #print("pointInsideTriangle: ret="+str(ret))
    #sys.exit(0)
    
    return ret    


def insideRegBndBox(x:float,y:float, polygonPoints: tuple) -> bool:

    #print("insideRegBndBox:polygonPoints="+str(polygonPoints))
    lowLowCornerPoint= polygonPoints[0]
    uppUppCornerPoint= polygonPoints[2]

    #print("type(lowLowCornerPoint[0])="+str(type(lowLowCornerPoint[0])))
    #print("type(uppUppCornerPoint[0])="+str(type(uppUppCornerPoint[0])))

    ret= False
    
    if x >= lowLowCornerPoint[0] and x <= uppUppCornerPoint[0] \
       and y >= lowLowCornerPoint[1] and y <= uppUppCornerPoint[1]:

          ret= True
    #---
    #print("insideRegBndBox: ret="+str(ret))
    return ret

#---
def getLinearTin2D(ceilT: float, floorT: float, ceilElev: float, floorElev: float, yElev: float) -> float:

   if yElev > ceilElev or yElev < floorElev:
       print("\nERROR in getLinearTin2D: Invalid yElev: "+str(yElev)+" for ceilElev,floorElev: "+str(ceilElev)+","+str(floorElev) +" combo\n")
       sys.exit(1)
       
   #--- Assuming ceilT < floorT, floorElev < ceilElev and all are also not negative.
   TRange= floorT - ceilT
   compoRange= ceilElev - floorElev

   # --- Need to add 1000.0 to yElev to get
   #     weight 0.0 at the surface. Note that
   #     it can produce a smale negative yElevWeight
   #     but this is not causing any serious problem
   #     in terms of the geotherm (pun not intended)
   yElevWeight= (ceilElev-(yElev+1000.0))/compoRange
   #yElevWeight= (yElev - floorElev)/compoRange
 
   TAtYElev= ceilT + yElevWeight*TRange

   print("ceilT="+str(ceilT))
   print("floorT="+str(floorT))
   print("ceilElev="+str(ceilElev))
   print("floorElev="+str(floorElev))
   print("yElev="+str(yElev))
   print("TAtYElev="+str(TAtYElev))
   print("DEBUG yElevWeight="+str(yElevWeight))

   #assert yElevWeight >= 0.0, " yElevWeight < 0.0 !!" 
   
   #sys.exit(0)

   return TAtYElev
