<!--- TODO: auto-generate this header -->
# piControl

<!--- TODO: pull this from some common machine-readable file -->
Short description: Simulation of the climate before large-scale industrialisation.

<!--- TODO: pull this from some common machine-readable file -->
Long description: Simulation of the climate before large-scale industrialisation.
More text would go here.
If pulling from machine-readable then this can only be text.
More fancy stuff would have to be in here directly.

## Forcings

<!--- TODO: auto-generate this from some common machine-readable file -->
### Source IDs

In this experiment, forcings with the following source IDs should be used:

<!--- TODO: auto-generated ESGF links -->

- DRES-CMIP-BB4CMIP7-2-0
- CR-CMIP-1-0-0
- UOEXETER-CMIP-2-0-0
- SOLARIS-HEPPA-CMIP-4-6

### Implementation details

<!--- TODO?: auto-generate this from some common machine-readable file? -->

The experiment should branch from the piControl-spinup experiment.

#### Biomass burning emissions

These come from DRES 
(i.e. use data with DRES in the source ID).
A number of species are provided.
If these do not suit your model,
please raise an issue ([TODO issue raising link]).

Repeat the 1850 values on repeat for piControl.

[TODO figure out whether raw vs. smoothed matters]

#### Greenhouse gas concentrations

These come from CR
(i.e. use data with CR in the source ID).

Repeat the 1850 values on repeat for piControl.

##### Species choices

There are three combinations of inputs that can be used
to capture the full radiative effect of all greenhouse gases.

###### Option 1

Use all 43 greenhouse gas species as inputs.
The list you should use is [TODO list].

###### Option 2

Use CO2, CH4, N2O and CFC12, then CFC11-eq for everything else.

###### Option 3

Use CO2, CH4, N2O and CFC12-eq and HFC134a-eq.

##### Grids and frequencies

The data is provided on multiple grids and frequencies.
For the piControl experiment,
only the yearly frequency data should be used
(the monthly frequency data includes a trend
so cannot be used as the basis for repeating inputs
as there will be a discontinuity from Dec 31 to Jan 1
in each year).
Please use the grid that best suits your model.

If you have a choice,
we recommend using the grid that matches the grid you will use during the historical
(unless that is the 15-degree grid, 
in which case you will have to do piControl with one of the grids 
that is provided at yearly frequency 
then switch to the monthly frequency data for the historical simulation).
Whichever grid you use, please document this clearly
in [TODO recommendation about how to document].

#### Volcanic forcing

This is provided by the University of Exeter 
(i.e. use data with UOEXETER in the source ID).
Both stratospheric aerosol properties as well as volcanic emissions are provided.
Please use the inputs which suit your model.
Please document which inputs you used
in [TODO recommendation about how to document].

For the piControl, there are dedicated climatology files.
These can be identified by the fact that they have "clim" in their filename.

#### Solar forcing

This is provided by the SOLARIS-HEPPA consortium
(i.e. use data with SOLARIS-HEPPA in the source ID).
A number of inputs are provided related to solar activity.
Please use the inputs which suit your model.
Please document which inputs you used
in [TODO recommendation about how to document].

For the piControl, there are dedicated piControl files.
These are identified as being fixed fields
(they're actually climatologies, but to avoid breaking things
we have not worried about this minor inconsistency,
for more details, see https://github.com/PCMDI/input4MIPs_CVs/issues/184).
These piControl files can be identified by the fact 
that they have "fx" in their filename.
