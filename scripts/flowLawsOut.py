#!/usr/bin/python3

import sys
import math

def calcVisc(T, P, APrefact, ActEng, ActVol, StrExp, StrRate):

    perfectGasConst= 8.31
    
    return (StrRate**((1-StrExp)/StrExp))*(math.e**((ActEng + P*ActVol)/(StrExp*perfectGasConst*T)))*(((1/APrefact)**(1/StrExp)))
# ---

#perfectGasConst= 8.31

dryOlA= 1.1e-15
wetOlA= 1.76e-14
mixOlA= 6.037e-15
#mixOlA= 2e-15

dryOlActEng= 540e3
wetOlActEng= 430e3
mixOlActEng= wetOlActEng

dryOlActVol= 20.e-6
wetOlActVol= 15.e-6
mixOlActVol= wetOlActVol

dryOlStrExp= 3.5
wetOlStrExp= 3.0
mixOlStrExp= wetOlStrExp

P= 1.e9

StrRate= 5e-13

folderOut= sys.argv[1]

ofp= open(folderOut+"/viscWRTTempWithPConstAt1e9.csv","w")

ofp.write("#T[K],wetv,dryv,mixv\n")

for T in range(573,1600):

    # ---  calcVisc(T, P, APrefact, ActEng, ActVol, StrExp, StrRate)
    wetv= calcVisc(T, P, wetOlA, wetOlActEng, wetOlActVol, wetOlStrExp, StrRate)
    
    #wetv_= (strainRate**((1-wetOlStrExp)/wetOlStrExp))*(math.e**((wetOlActEng + Pressure*wetOlActVol)/(wetOlStrExp*perfectGasConst*T)))*(((1/wetOlA)**(1/wetOlStrExp)))

    dryv= calcVisc(T, P, dryOlA, dryOlActEng, dryOlActVol, dryOlStrExp, StrRate)
    #dryv= (strainRate**((1-dryOlStrExp)/dryOlStrExp))*(math.e**((dryOlActEng + Pressure*dryOlActVol)/(dryOlStrExp*perfectGasConst*T)))*(((1/dryOlA)**(1/dryOlStrExp)))

    mixv= calcVisc(T, P, mixOlA, mixOlActEng, mixOlActVol, mixOlStrExp, StrRate)
    #mixv= (strainRate**((1-mixOlStrExp)/mixOlStrExp))*(math.e**((mixOlActEng + Pressure*mixOlActVol)/(mixOlStrExp*perfectGasConst*T)))*(((1/mixOlA)**(1/mixOlStrExp)))

    ofp.write(str(T)+","+str(wetv)+","+str(dryv)+","+str(mixv)+"\n")
# ---
    
ofp.close()

P= 2.e9

ofp= open(folderOut+"/viscWRTTempWithPConstAt2e9.csv","w")

ofp.write("#T[K],wetv,dryv,mixv\n")

for T in range(573,1600):

    wetv= calcVisc(T, P, wetOlA, wetOlActEng, wetOlActVol, wetOlStrExp, StrRate)
    #wetv= (strainRate**((1-wetOlStrExp)/wetOlStrExp))*(math.e**((wetOlActEng + Pressure*wetOlActVol)/(wetOlStrExp*perfectGasConst*T)))*(((1/wetOlA)**(1/wetOlStrExp)))

    dryv= calcVisc(T, P, dryOlA, dryOlActEng, dryOlActVol, dryOlStrExp, StrRate)
    #dryv= (strainRate**((1-dryOlStrExp)/dryOlStrExp))*(math.e**((dryOlActEng + Pressure*dryOlActVol)/(dryOlStrExp*perfectGasConst*T)))*(((1/dryOlA)**(1/dryOlStrExp)))

    mixv= calcVisc(T, P, mixOlA, mixOlActEng, mixOlActVol, mixOlStrExp, StrRate)
    #mixv= (strainRate**((1-mixOlStrExp)/mixOlStrExp))*(math.e**((mixOlActEng + Pressure*mixOlActVol)/(mixOlStrExp*perfectGasConst*T)))*(((1/mixOlA)**(1/mixOlStrExp)))

    ofp.write(str(T)+","+str(wetv)+","+str(dryv)+","+str(mixv)+"\n")
# ---
    
ofp.close()

T= 873

ofp= open(folderOut+"/viscWRTPWithTConstAt873.csv","w")

ofp.write("#P[Pa],wetv,dryv,mixv\n")

P0= 0.2e8
Pincr= 0.01e8

for pit in range(0,2000):

    P= P0 + pit*Pincr

    wetv= calcVisc(T, P, wetOlA, wetOlActEng, wetOlActVol, wetOlStrExp, StrRate)
    #wetv= (strainRate**((1-wetOlStrExp)/wetOlStrExp))*(math.e**((wetOlActEng + P*wetOlActVol)/(wetOlStrExp*perfectGasConst*T)))*(((1/wetOlA)**(1/wetOlStrExp)))

    dryv= calcVisc(T, P, dryOlA, dryOlActEng, dryOlActVol, dryOlStrExp, StrRate)
    #dryv= (strainRate**((1-dryOlStrExp)/dryOlStrExp))*(math.e**((dryOlActEng + P*dryOlActVol)/(dryOlStrExp*perfectGasConst*T)))*(((1/dryOlA)**(1/dryOlStrExp)))

    mixv= calcVisc(T, P, mixOlA, mixOlActEng, mixOlActVol, mixOlStrExp, StrRate)
    #mixv= (strainRate**((1-mixOlStrExp)/mixOlStrExp))*(math.e**((mixOlActEng + P*mixOlActVol)/(mixOlStrExp*perfectGasConst*T)))*(((1/mixOlA)**(1/mixOlStrExp)))

    ofp.write(str(P)+","+str(wetv)+","+str(dryv)+","+str(mixv)+"\n")
# ---

ofp.close()

T= 1573

ofp= open(folderOut+"/viscWRTPWithTConstAt1573.csv","w")

ofp.write("#P[Pa],wetv,dryv,mixv\n")

#P0= 0.2e8
#Pincr= 0.01e8

for pit in range(0,2000):

    P= P0 + pit*Pincr

    wetv= calcVisc(T, P, wetOlA, wetOlActEng, wetOlActVol, wetOlStrExp, StrRate)
    #wetv= (strainRate**((1-wetOlStrExp)/wetOlStrExp))*(math.e**((wetOlActEng + P*wetOlActVol)/(wetOlStrExp*perfectGasConst*T)))*(((1/wetOlA)**(1/wetOlStrExp)))

    dryv= calcVisc(T, P, dryOlA, dryOlActEng, dryOlActVol, dryOlStrExp, StrRate)
    #dryv= (strainRate**((1-dryOlStrExp)/dryOlStrExp))*(math.e**((dryOlActEng + P*dryOlActVol)/(dryOlStrExp*perfectGasConst*T)))*(((1/dryOlA)**(1/dryOlStrExp)))

    mixv= calcVisc(T, P, mixOlA, mixOlActEng, mixOlActVol, mixOlStrExp, StrRate)
    #mixv= (strainRate**((1-mixOlStrExp)/mixOlStrExp))*(math.e**((mixOlActEng + P*mixOlActVol)/(mixOlStrExp*perfectGasConst*T)))*(((1/mixOlA)**(1/mixOlStrExp)))

    ofp.write(str(P)+","+str(wetv)+","+str(dryv)+","+str(mixv)+"\n")
# ---

ofp.close()
