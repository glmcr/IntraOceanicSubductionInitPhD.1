#!/usr/bin/python3

def traditionalNorm(composTuple: tuple) -> tuple :

  composSum= 0.0

  composVolFracs= [0.0] * (len(composTuple) + 1)
    
  for compo in composTuple:
    composSum += compo

  print("composSum="+str(composSum))
    
  #for compo in composTuple:
  for c in range(0, len(composTuple)):
    composVolFracs[c+1]= composTuple[c]/composSum
    #composVolFracs.append(compo/composSum)

  return tuple(composVolFracs)
# ---
    
compos1= ( 0.2, 0.5, 0.25 ) # --- Sum to 0.95
compos1VolFracs= traditionalNorm(compos1)
print("compos1VolFracs="+str(compos1VolFracs))

#altCompos1VolFracs= altNorm(compos1)
#print("altCompos1VolFracs="+str(altCompos1VolFracs)+"\n")

compos2= ( 0.2, 0.5, 0.35 ) # --- Sum to 1.05
compos2VolFracs= traditionalNorm(compos2)
print("compos2VolFracs="+str(compos2VolFracs))

#altCompos2VolFracs= altNorm(compos2)
#print("altCompos2VolFracs="+str(altCompos2VolFracs))

compos3= (0.02, 0.15, 1.2)
compos3VolFracs= traditionalNorm(compos3)
print("compos3VolFracs="+str(compos3VolFracs))
