#!/usr/bin/python3

import os
import sys
import glob
import vtk #.vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy #thats what you need 

# directory where the VTU particles file are located
vtuParticlesDir = sys.argv[1]
csvFileOut= sys.argv[2]

vtuPFiles= sorted(glob.glob(vtuParticlesDir + "/*.vtu"))
reader= vtk.vtkXMLUnstructuredGridReader()

vtuPData= {}

# Only consider oceanic crust particles that have Pressure
# and Temperature values over those low limits thresholds
ocPLow= 4e8 # GPa, 4e8 == shorcut for 4*math.pow(10,8)
ocTLow= 673 # Kelvin -> 400C

# Only consider particle ids for oceanic crust particles
# that have a concentration > 0.5
ocCrtThr= 0.5

gridYMeters= 700e3

for vtuPFile in vtuPFiles:
                     
   print("Reading vtuPFile: "+vtuPFile)
   vtuPFileName= os.path.basename(vtuPFile)
                     
   reader.SetFileName(vtuPFile)
   reader.Update()
   
   #vtuPData[vtuPFileName]= reader.GetOutput()

   #--- Extract all the particles data
   dataTmp= reader.GetOutput()
   #--- Extract the timestamp (in years) as an int
   dataTime= int( dataTmp.GetFieldData().GetArray("TIME").GetTuple(0)[0] )

   #--- Index the the particles data with the timestamp
   #vtuPData[dataTime]= dataTmp
   #pidData= vtuPData[dataTime].GetPointData().GetArray("id")
   pidData= dataTmp.GetPointData().GetArray("id")

   print("dataTime="+str(dataTime))

   pidDataSize= pidData.GetSize()
   print("pidData size="+str(pidDataSize)+"\n")

   #--- particles position data
   pPos= dataTmp.GetPointData().GetArray("position")
   
   #--- Extract oceanic crust particles data:
   ocCrustData= dataTmp.GetPointData().GetArray("oceanicCrust")
   
   #--- Extract particle Pressure data:
   pPData= dataTmp.GetPointData().GetArray("p")
   
   #--- Extract particles Temperature data:
   pTData= dataTmp.GetPointData().GetArray("T")
   
   relevantOCrustData= {}
   
   for pid in range(pidDataSize):

       ocpCrt= ocCrustData.GetTuple(pid)[0]
       ocpP= pPData.GetTuple(pid)[0]
       ocpT= pTData.GetTuple(pid)[0]       
       
       if ocpCrt >= ocCrtThr and ocpP >= ocPLow and ocpT >= ocTLow:
           
          ocpPos= pPos.GetTuple(pid)
          
          print("ocpCrt="+str(ocpCrt))
          print("ocpPos="+str(ocpPos))
          print("ocpP="+str(ocpP))
          print("ocpT="+str(ocpT))

          relevantOCrustData[pid]= { "concentration": ocpCrt,
                                     "Pressure(Gpa)": ocpP,
                                     "Temperature(K)": ocpT,
                                     "Temperature(C)": ocpT-273,
                                     "Depth": gridYMeters - ocpPos[1]
                                   }

          print("relevantOCrustData[pid]="+str(relevantOCrustData[pid]))
          #relevantOCrustDataPids.append(pid)
          #sys.exit(0)
       
       #if ocCrustData
   #--- end for loop
   #sys.exit(0)
   
   #--- Index the the oceanic particles data with the timestamp
   vtuPData[dataTime]= relevantOCrustData

   print(" done with file: "+vtuPFile+"\n")
   
   #dataTime= vtuPData[vtuPFileName].GetPointData().GetArray("TIME")
   #dataTime= vtuPData[vtuPFileName].GetFieldData().GetArray("TIME").GetTuple(
                     
sys.exit(0)

# Read the source file.
#reader = vtk.vtkXMLUnstructuredGridReader()
#reader = vtk.vtkUnstructuredGridReader()
#reader = vtk.vtkDataSetReader()
#reader.SetFileName(file_name)

#reader.ReadAllScalarsOn()
#reader.ReadAllVectorsOn()
#reader.ReadAllTensorsOn()
#reader.ReadAllFieldsOn()
#reader.Update()  # Needed because of GetScalarRange

#print(reader)
#sys.exit(0)
#output = reader.GetOutput()
#print(output)
#sys.exit(0)

opdnp= vtk_to_numpy(output.GetPoints().GetData())
print("opdnp.shape="+str(opdnp.shape))
print("opdnp[0]="+str(opdnp[0]))
print("opdnp[1]="+str(opdnp[1]))
#print("opdnp[2186560-1]="+str(opdnp[2186560-1]))
print("opdnp[end]="+str(opdnp[-1]))
ymax= np.max(opdnp[:,1])
print("ymax="+str(ymax))
sy= sorted(opdnp[:,1])
print("sy[end]="+str(sy[-1]))
#sys.exit(0)

#opdext= opd.GetDataArray().GetExtents()
#print("opdext="+str(opdext))

#opd0= opd.GetTuple(0)
#print("opd0="+str(opd0))
#opdend= opd.GetTuple(opd.GetSize()-1)
#print("opdend="+str(opdend))
#sys.exit(0)

#ncells= output.GetNumberOfCells()
#print("ncells="+str(ncells))

ppos= output.GetPointData().GetArray("position")
print("ppos size="+str(ppos.GetSize()))
ppos0= ppos.GetTuple(0)
print("ppos0="+str(ppos0))
ppos1= ppos.GetTuple(1)
print("ppos1="+str(ppos1))
pposT=ppos.GetTuple(2186560-1)
print("pposT="+str(pposT))

#pposLast= ppos.GetTuple(ppos.GetSize()-1)
#print("pposLast="+str(pposLast))
#sys.exit(0)

pid= output.GetPointData().GetArray("id")
print("pid size="+str(pid.GetSize()))
pid0= pid.GetTuple(0)
print("pid0="+str(pid0))
pidLast= pid.GetTuple(pid.GetSize()-1)
print("pidLast="+str(pidLast))
#maxPid= sorted(pid.GetTuples())[0]
#print("maxPid="+str(maxPid))

pidSize= pid.GetSize()

#potential = output.GetPointData().GetArray("potential")
oc= output.GetPointData().GetArray("oceanicCrust")

#pd= oc.GetPoint

print("oc size="+str(oc.GetSize()))
oct0= oc.GetTuple(0)
print(oct0)
octend= oc.GetTuple(oc.GetSize()-1)
print(octend)

TPD= output.GetPointData().GetArray("T")
print("TPD size="+str(TPD.GetSize()))
T0= TPD.GetTuple(0)
print("T0="+str(T0))
TLast= TPD.GetTuple(TPD.GetSize()-1)
print("TLast="+str(TLast))

PPD= output.GetPointData().GetArray("p")
print("PPD size="+str(PPD.GetSize()))
P0= PPD.GetTuple(0)
print("P0="+str(P0))
PLast= PPD.GetTuple(PPD.GetSize()-1)
print("PLast="+str(PLast))

#DPD= output.GetPointData().GetArray("depth")
##print(DPD)
#D0= DPD.GetTuple(0)
#print("D0="+str(D0))
#Dend= DPD.GetTuple(PPD.GetSize()-1)
#print("Dend"+str(Dend))


#sys.exit(0)

#--- numpy
#oc_np= vtk_to_numpy(oc)
#print("oc_np.shape="+str(oc_np.shape))
#print(oc_np)

