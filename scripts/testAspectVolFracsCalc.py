#!/usr/bin/python3

def aspectVolFracCalc(composTuple: tuple) -> tuple:

   # --- local mutable copy of the composTuple
   composList= list(composTuple)
   composition_fractions = [0.0] * (len(composTuple) + 1)

   # Clip the compositional fields so they are between zero and one,
   # and sum the compositional fields for normalization purposes.
   sum_composition = 0.0

   # GM note: composList do not include the background. 
   for c in range(0,len(composList)):

     # --- Here the compo at c becomes 1.0 if > 1.0 BUT
     #     it stays the same if < 1.0 (assuming it is >= 0.0)
     #     NOTE: the compo of background is used here (is it always at 0.0 ???)
     if composList[c] > 1.0:
        composList[c] = 1.0;
     # ---
     
     sum_composition += composList[c]
   # ---

   # --- Compute background field fraction
   if sum_composition >= 1.0:
     composition_fractions[0]= 0.0
   else :
     composition_fractions[0] = 1.0 - sum_composition
     
   # --- Compute and possibly normalize field fractions
   #     Note that this loop starts at 1
   for c in range(0,len(composList)):
       
      if sum_composition >= 1.0:
        composition_fractions[c+1]= composList[c]/sum_composition
      else:
        composition_fractions[c+1]= composList[c];
   # ---
   
   return tuple(composition_fractions)

# ---

compos1= (0.2, 0.5, 0.25)
volFracs1= aspectVolFracCalc(compos1)

print("compos1="+str(compos1))
print("volFracs1="+str(volFracs1)+"\n")

compos2= (0.2, 0.5, 0.35)
volFracs2= aspectVolFracCalc(compos2)

print("compos2="+str(compos2))
print("volFracs2="+str(volFracs2)+"\n")

compos3= (0.02, 0.15, 1.2)
volFracs3= aspectVolFracCalc(compos3)

print("compos3="+str(compos3))
print("volFracs3="+str(volFracs3)+"\n")




