- 2D only
- free surface
- incompressible or compressible ?
- prescribed velocity boundary conditions on bottom and vertical sides (or tangential or open) ?
- prescribed adiabatic temperature boundary conditions on bottom and top.
  
- Write an ASPECT plugin prm file that is based the following official ASPECT cookbooks prm files: 

   https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-reaction.prm

   https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-passive-particles-properties.prm

   https://github.com/geodynamics/aspect/blob/master/contrib/perplex/perplex_lookup_composition.prm
   (Somewhat outdated, seems that it was created before
    https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h
    and its implementation
    https://github.com/geodynamics/aspect/blob/master/source/utilities.cc
    were created)

   notes: 

     particles: initial composition + initial_position + pT_path + 
                ? metamorphic facies(no metamorphism, greenschist, granulites, eclogites)

    composition: It reacts to (dynamic?)pressure-temperature conditions.
                 ? Use the data structures that are defined in 
                 https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h ?   
 
- ?? Also use the visco_plastic material model as in :
  https://github.com/anne-glerum/paper-aspect-plasticity-subduction-data/blob/master/2D_subduction/2D_subduction_2.prm
 

------------------------------------------------------------------
Questions: 

  1). Not sure where to put metamorphic facies flags: particles or composition or create new data structure or class ?
  2). Still not clear to me: The relations between the material model attributes vs composition attributes, does the
      feebacks between the attributes of those two entities are one way or two way ?.
