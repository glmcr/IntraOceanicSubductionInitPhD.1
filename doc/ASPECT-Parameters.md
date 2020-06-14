- 2D only.
- free surface.
- incompressible or compressible ?
- prescribed velocity boundary conditions on bottom and vertical sides (or tangential or open or a mix of both) ?
- prescribed adiabatic temperature boundary conditions on bottom and top ?
  
- Write an ASPECT plugin prm file that is based the following official ASPECT cookbooks prm files: 

   https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-reaction.prm

   https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-passive-particles-properties.prm

   https://github.com/geodynamics/aspect/blob/master/contrib/perplex/perplex_lookup_composition.prm
   (somewhat outdated, it seems that it was created before this interface file:

    https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h

    and its implementation

    https://github.com/geodynamics/aspect/blob/master/source/utilities.cc

    were created)

    But the prm file could use a brand new material model that has to be based on one of the already
    exiting material models implementations:

    (incompressible)
    https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/multicomponent.h

    (compressible)
    https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/multicomponent_compressible.h

    The metamorphic phases changes(by volume or mass fractions) could be tracked using the __reaction_terms__
    attribute of the  __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelOutputs__ 
    object. The __reaction_terms__ compositions would be all at 0.0 everywhere in the domain at the beginning 
    of the simulations and would be set to the respective prograde(retrograde eventually ?) metamorphic facies
    of the initial compositions types(i.e. initial rocks types, ex. basalt -> greenschist metabasalt -> 
    amphibolite metabasalt -> granulite metabasalt, sediments -> greenschist metasediments -> amphibolite
    metasediments -> granulite metasediments).

-  __particles__: initial composition + initial_position + pT_path + 
metamorphic facies(no metamorphism, greenschist, amphibolites, granulites, ?eclogites?)
I will have to write code that sets the metamorphic facies for each particle
using the (dynamic?) total pressure and pressure conditions prevailing at the
particles positions.

-  material model __reaction_terms__: Reacts to (dynamic?)total pressure-temperature conditions OR use 
the data structures that are defined in
https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h
instead of the material model reaction_terms attribute ? The answer to that question is probably no.
 
- ?? Also use some of the __visco_plastic__ material model implementation as in :
https://github.com/anne-glerum/paper-aspect-plasticity-subduction-data/blob/master/2D_subduction/2D_subduction_2.prm ??
 

------------------------------------------------------------------
- Things to always remember:
 
The __vector\<vector\<double\>\>__ __composition__ is an attribute of the __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelInputs__
and not an attribute of the __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelOutputs__.

BUT the __template\<int dim\>__ __struct__ __MaterialModel::MaterialProperties::MaterialModelOutputs__ does contain
an attribute of the same type as __vector\<vector\<double\>\>__ __composition__ which is named __vector\<vector\<double\>\>__ __reaction_terms__ which I think could likely be used to store metamorphic mineral phases changes(as weight proportions ?) ex. if __reaction_terms[i][c]__ is 0.0 then there is no mineral phase c at position i. If the attribute __reaction_terms[i][c]__ is 0.69 then we have 0.69 of mineral c in weight proportion compared to the other mineral phases(which must sum up to 0.31 in weight proportion) present at position i.
