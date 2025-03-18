<!--- TODO: auto-generate this header -->
# historical

<!--- TODO: pull this from some common machine-readable file -->
Short description: Simulation of the recent past from 1 Jan 1850 to 31 Dec 2021.

<!--- TODO: pull this from some common machine-readable file -->
Long description: Simulation of the recent past from 1 Jan 1850 to 31 Dec 2021.
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

The experiment should branch from the piControl experiment.

#### Biomass burning emissions

These come from DRES 
(i.e. use data with DRES in the source ID).
A number of species are provided.
If these do not suit your model,
please raise an issue ([TODO issue raising link]).

The data are provided in two flavours:

1. raw
1. smoothed

We recommend using the [TODO recommendation] flavour.
Whichever flavour you use, please document this clearly
in [TODO recommendation about how to document].

#### Greenhouse gas concentrations

These come from CR
(i.e. use data with CR in the source ID).

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
Please use the grid and frequency that best suits your model.

If you have a choice,
we recommend using the monthly data on the 15-degree latitudinal grid.
Whichever grid and frequency you use, please document this clearly
in [TODO recommendation about how to document].

#### Volcanic forcing

This is provided by the University of Exeter 
(i.e. use data with UOEXETER in the source ID).
Both stratospheric aerosol properties as well as volcanic emissions are provided.
Please use the inputs which suit your model.
Please document which inputs you used
in [TODO recommendation about how to document].

#### Solar forcing

This is provided by the SOLARIS-HEPPA consortium
(i.e. use data with SOLARIS-HEPPA in the source ID).
A number of inputs are provided related to solar activity.
Please use the inputs which suit your model.
Please document which inputs you used
in [TODO recommendation about how to document].

##### Frequencies

The data is provided at both a monthly and a daily frequency.
Please use the frequency that best suits your model.

If you have a choice,
we recommend using the [TODO recommendation].
Whichever frequency you use, please document this clearly
in [TODO recommendation about how to document].

## Getting the data

<!--- TODO: auto-generate a script showing how to download the data using esgpull -->
