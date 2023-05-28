#!/usr/bin/python3

import numpy as np
import os
import sys
import vtk
from vtk.util import numpy_support
import glob
import re
import matplotlib.pyplot as plt
import scipy.interpolate

#------------------------------------------------------------------------------
#  read values from VTU
#------------------------------------------------------------------------------

def readvtu(file):

    #Load vtu data (pvtu directs to vtu files)
    reader = vtk.vtkXMLPUnstructuredGridReader()
    reader.SetFileName(file)
    reader.Update()
    
    #Get the coordinates of nodes in the mesh
    nodes_vtk_array= reader.GetOutput().GetPoints().GetData()
    
    #Convert nodal vtk data to a numpy array
    nodes_numpy_array = vtk.util.numpy_support.vtk_to_numpy(nodes_vtk_array)
    
    #Extract x, y and z coordinates from numpy array
    x,y,z= nodes_numpy_array[:,0] , nodes_numpy_array[:,1] , nodes_numpy_array[:,2]    

    #Determine the number of scalar fields contained in the .pvtu file
    number_of_fields = reader.GetOutput().GetPointData().GetNumberOfArrays()
    
    #Determine the name of each field and place it in an array.
    field_names = []
          
    for i in range(number_of_fields):
        field_names.append(reader.GetOutput().GetPointData().GetArrayName(i))
    
    #Extract values

    npDataDict= {}

    #idx = field_names.index("eclogites")
    field_vtk_array = reader.GetOutput().GetPointData().GetArray(field_names.index("eclogites"))
    npDataDict["eclogites"] = numpy_support.vtk_to_numpy(field_vtk_array)

    field_vtk_array = reader.GetOutput().GetPointData().GetArray(field_names.index("greenschists"))
    npDataDict["greenschists"] = numpy_support.vtk_to_numpy(field_vtk_array)
    
    # compute the equivalent shear stress
    #tau_eq=np.zeros(len(strain_rate))     
    #for i in range(len(strain_rate)):
    #    stress=shear_stress[i,:]
    #    sigma = np.array( [ [stress[0], stress[3], stress[5]],
    #                       [stress[3], stress[1], stress[4]],
    #                       [stress[5], stress[4], stress[2]] ])
    #    eigvals = np.linalg.eigvalsh(sigma)
    #    sig1,sig2,sig3 = eigvals
    #    J2=sig1*sig1+sig2*sig2+sig3*sig3
    #    tau_eq[i]=np.sqrt(3/2*J2)
    #    #tau_eq[i]=2*viscosity[i]*strain_rate[i]
    #    #print('J2, ', tau_eq)

    return x,y,z,npDataDict
    #return x,y,z,number_of_fields,strain_rate,viscosity

###################################################################################################


#ntot=len(glob.glob(f'solution-*.pvtu'))
#print('found ',ntot,' pvtu files')

pvtuFiles= glob.glob(sys.argv[1]+"/*.pvtu")

outdir= sys.argv[2]

for fich in pvtuFiles: #glob.glob(f'solution-*.pvtu'):

    #x,y,z,nb,sr,eta=readvtu(fich)
    
    x,y,z,npDataDict=readvtu(fich)
    
    ################################
    # export to png via scatter plot
    ################################

    print('processing ',fich,'which contains ',np.size(x),' data points')
        
    #print('-----> strain rate m/M:',min(sr),max(sr))
    #plt.scatter(x, y, c=np.log10(sr), s=3, cmap='viridis', vmin=-13, vmax=-9) 
    #ax= plt.plot( kind="scatter",  c=npDataDict["eclogites"], s=3, cmap='viridis', vmin=0, vmax=1, label="eclo")
    #plt.plot( kind="scatter", c=npDataDict["greenschists"], s=3, cmap='viridis', vmin=0, vmax=1, label="grg",ax=ax)
    
    plt.scatter(x, y, c=npDataDict["eclogites"], s=3, cmap='viridis', vmin=0, vmax=1, label="eclo")
    plt.figure().add_subplot(111)
    plt.scatter(x, y, c=npDataDict["greenschists"],s=3, cmap='viridis', vmin=0, vmax=1, label="grg") #ax=ax)
    #plt.xlim(0, 1)
    #plt.ylim(0, 1)
    plt.axis('scaled')
    plt.colorbar()
    
    plt.savefig(outdir+"/materials_"+ os.path.basename(fich).split(".")[0] ) #str(fich[11:-1]))
    
    #plt.savefig('strainrate_'+str(fich[10:14]))
    #plt.show()
    plt.clf()
    sys.exit(0)

    #print('-----> viscosity m/M:',min(eta),max(eta))
    #plt.scatter(x, y, c=np.log10(eta), s=4, cmap='plasma', vmin=17, vmax=22)
    #plt.axis('scaled')
    #plt.colorbar()
    #plt.savefig('viscosity_'+str(fich[10:14]))
    ##plt.show()
    #plt.clf()

    ################################
    # export to ascii
    ################################

    #np.savetxt('solution_'+str(fich[10:14])+'.ascii',np.array([x,y,z,sr]).T,header='# x,y,z,sr')

#---
