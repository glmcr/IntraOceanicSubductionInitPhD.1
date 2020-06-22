Parameters for the 1st part of the PhD study:
----------------------------------------------

- 2D only.

- free surface on top. 

- velocity boundary conditions:

   bottom: tangential or no slip ? 

   vertical sides: open boundary conditions as defined in this [paper](https://www.researchgate.net/publication/258723103_Using_open_sidewalls_for_modelling_self-consistent_lithosphere_subduction_dynamics/fulltext/57aaf64408ae0932c970c1cd/Using-open-sidewalls-for-modelling-self-consistent-lithosphere-subduction-dynamics.pdf))

- incompressible or compressible ?

- prescribed adiabatic temperature boundary conditions on bottom and top ? also on vertical sides(or open) ? 

- Does the properties(mainly the densities) of the rocks material types compositions have to be used in the
  material model itself ?
  
- Write an ASPECT plugin prm file that is based the following official ASPECT cookbooks prm files: 

  [composition-reaction.prm](https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-reaction.prm)
  
  [composition-active-particles.prm](https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-active-particles.prm)
  
  [composition-passive-particles-properties.prm](https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-passive-particles-properties.prm)
  
  and [perplex_lookup_composition.prm](https://github.com/geodynamics/aspect/blob/master/contrib/perplex/perplex_lookup_composition.prm)
 
- Use __particles__  properties : initial composition + initial_position + pT_path + a new  __particles__
  property called metamorphic_facies(no metamorphism, greenschist, amphibolites, ?granulites?, ?eclogites?) to track
  the metamorphic evolution of the rocks materials on both sides of the subduction interface between the
  two interacting plates.

- Use an already defined metamorphic facies lookup table(i.e. a file) for the relation between the P-T
  conditions and the rocks materials for the specific context of an intra-oceanic subduction initiation.
  
- Just one rock material type for one __particle__ at any time(possible metastable cases ??). 

- We could also use the __reaction_terms__ object to hold the a representation of the volume fractions
  of the different rock material types in the FE cells.

-----------------------------------------------------------------
- Questions:

-  ?? Use the already mentioned data structures that are defined in [this include file](https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h)
instead of the material model __reaction_terms__ attribute ?? The answer to that question is probably no.
 
- ?? Also use some of the __visco_plastic__ material model implementation as in this [paper](https://www.researchgate.net/publication/323856800_Nonlinear_viscoplasticity_in_ASPECT_Benchmarking_and_applications_to_subduction/fulltext/5aaff120aca2721710fde151/Nonlinear-viscoplasticity-in-ASPECT-Benchmarking-and-applications-to-subduction.pdf) ??
 
------------------------------------------------------------------
- Things to always remember:
 
The __vector\<vector\<double\>\>__ __composition__ is an attribute of the __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelInputs__
and not an attribute of the __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelOutputs__.

BUT the __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelOutputs__ does contain
an attribute of the same type as __vector\<vector\<double\>\>__ __composition__ which is named __vector\<vector\<double\>\>__ __reaction_terms__ which I think could likely be used to store metamorphic mineral phases changes(as weight proportions ?) ex. if __reaction_terms[i][c]__ is 0.0 then there is no mineral phase c at position i. If the attribute __reaction_terms[i][c]__ is 0.69 then we have 0.69 of mineral c in weight proportion compared to the other mineral phases(which must sum up to 0.31 in weight proportion) present at position i.
