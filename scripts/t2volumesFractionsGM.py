#!/usr/bin/python3

def traditionalNorm(composTuple: tuple) -> tuple :

  composSum= 0.0

  composVolFracs= []
    
  for compo in composTuple:
    composSum += compo

  print("composSum="+str(composSum))
    
  for compo in composTuple:
    composVolFracs.append(compo/composSum)

  return tuple(composVolFracs)
# ---

def altNorm(composTuple: tuple) -> tuple :

  #compoMax= -1.0
  ## --- find max compo first.
  #for compo in composTuple:
  #  if compo > compoMax:
  #    compoMax= compo
  # ---
  #print("compoMax="+str(compoMax))

  composSum= 0.0

  for compo in composTuple:
    composSum += compo  
  
  composSumsAdjTo1= 1.0/composSum

  print("composSumsAdjTo1="+str(composSumsAdjTo1))
  
  altComposSum= 0.0

  altComposFracs= [0.0]

  for c in range(1,len(composTuple)):

    altCompo= composSumsAdjTo1*composTuple[c]
    altComposFracs.append(altCompo)
    altComposSum += altCompo
    
  # ---

  #print("altCompos="+str(altCompos))
  print("altComposSum="+str(altComposSum))
  #composVolFracs= [0.0]

  #for c in range(1,len(composTuple)):
  #   composVolFracs.append(altCompos[c]/altComposSum)
  # --- 

  return tuple(altComposFracs)
        
# ---
    
compos1= ( 0.0, 0.2, 0.5, 0.25 ) # --- Sum to 0.95

compos1VolFracs= traditionalNorm(compos1)

print("compos1VolFracs="+str(compos1VolFracs))

altCompos1VolFracs= altNorm(compos1)

print("altCompos1VolFracs="+str(altCompos1VolFracs)+"\n")

compos2= ( 0.0 , 0.2, 0.5, 0.35 ) # --- Sum to 1.05

compos2VolFracs= traditionalNorm(compos2)

print("compos2VolFracs="+str(compos2VolFracs))

altCompos2VolFracs= altNorm(compos2)

print("altCompos2VolFracs="+str(altCompos2VolFracs))
