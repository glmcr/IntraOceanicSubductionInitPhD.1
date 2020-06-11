- 2D only
- free surface
- incompressible or compressible ?
- prescribed velocity boundary conditions on bottom and vertical sides (or tangential or open) ?
- prescribed temperature boundary conditions on bottom and top.
  
- Write an ASPECT plugin prm file that is based the following official ASPECT cookbooks prm files: 

   aspect/cookbooks/composition-reaction.prm
   aspect/cookbooks/composition-passive-particles-properties.prm
   aspect/contrib/perplex/perplex_lookup_composition.prm(a bit outdated, was created before utilities.h)

   notes: particles: initial composition + initial_position + pT_path + 
                     ? metamorphic facies(no metamorphism, greenschist, granulites, eclogites)

          composition: It reacts to (dynamic?)pressure-temperature conditions.
                       Use the data structures that are defined in aspect/include/aspect/material_model/utilities.h ?   
 
- ? Also use the visco_plastic material model as in :

  paper-aspect-plasticity-subduction-data/paper-aspect-plasticity-subduction-data-master/2D_subduction/2D_subduction_2.prm

------------------------------------------------------------------
Questions: 

  1). Not sure where to put metamorphic facies flags: particles or composition or create new data structure or class ?
  2). Still not clear to me: The relations of the material models vs composition, does the feebacks between those two
      entities are one way or two way ?.
