- 2D only.
- free surface.
- incompressible or compressible ?
- prescribed velocity boundary conditions on bottom and vertical sides (or tangential or open or a mix of both) ?
- prescribed adiabatic temperature boundary conditions on bottom and top.
  
- Write an ASPECT plugin prm file that is based the following official ASPECT cookbooks prm files: 

   https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-reaction.prm

   https://github.com/geodynamics/aspect/blob/master/cookbooks/composition-passive-particles-properties.prm

   https://github.com/geodynamics/aspect/blob/master/contrib/perplex/perplex_lookup_composition.prm
   (somewhat outdated, it seems that it was created before this interface file:

    https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h

    and its implementation

    https://github.com/geodynamics/aspect/blob/master/source/utilities.cc

    were created)

-  particles: initial composition + initial_position + pT_path + 
metamorphic facies(no metamorphism, greenschist, amphibolites, granulites, ?eclogites?)
I will have to write code that sets the metamorphic facies for each particle
using the (dynamic?) total pressure and pressure conditions prevailing at the
particles positions.

-     material model reaction_terms: Reacts to (dynamic?)total pressure-temperature conditions OR use 
the data structures that are defined in
https://github.com/geodynamics/aspect/blob/master/include/aspect/material_model/utilities.h
instead of the material model reaction_terms attribute ?  
 
- ?? Also use the visco_plastic material model as in :
https://github.com/anne-glerum/paper-aspect-plasticity-subduction-data/blob/master/2D_subduction/2D_subduction_2.prm ??
 

------------------------------------------------------------------
- Things To remember:
 
The composition is an attribute of the template <int dim>struct MaterialModel::MaterialProperties::MaterialModelInputs
and not an attribute of the template <int dim>struct MaterialModel::MaterialProperties::MaterialModelOutputs.

BUT the template <int dim>struct MaterialModel::MaterialProperties::MaterialModelOutputs does have
an attribute called reaction_terms which I think can be used to store metamorphic mineral phases changes
(as weight proportions ?) ex. if reaction_terms[i][c] is 0.0 then there is no mineral phase c at position i.
if the attribute reaction_terms[i][c] is 0.69 then we have 0.69 of mineral c in weight proportion compared
to the other mineral phases(which must sum up to 0.31 in weight proportion) present at position i.

Question: Does that reaction_terms attribute is used to update the material model properties(viscosity,
density and so on) ?
