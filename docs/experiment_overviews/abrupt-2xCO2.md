<!--- This file contains a number of sections -->
<!--- They are bounded by comments like this -->
<!--- Do not edit these sections by hand -->
<!--- Start title -->
# abrupt-2xCO2
<!--- End title -->

## One-line description

<!--- Start one-line-description -->
Abrupt doubling of CO2
<!--- End one-line-description -->

## Longer description

<!--- Start longer-description -->
Identical to the `piControl` DECK experiment but with a step change to 2xCO2 concentration from its pre-industrial value, held constant for the duration of the run.  Reference: [Webb et al., 2017](https://doi.org/10.5194/gmd-10-359-2017)
<!--- End longer-description -->

## Other experiment info

<!--- Start other-experiment-info -->
Parent experiment: piControl
Parent experiment activity: CMIP
<!--- End other-experiment-info -->

## Forcings

The forcings required for this experiment are listed below.
For each forcing, we provide a short-hand/common name,
followed by the source ID from which this forcing should be retrieved.
Where relevant, we also provide further information.

<!--- Start forcings -->
- co2: [CR-CMIP-1-0-0](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22CR-CMIP-1-0-0%22%5D%7D)
    - Further information: CO2 data has the variable_id `co2`, this is a change from CMIP6 where the variable_id was `mole_fraction_of_carbon_dioxide` (see https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/greenhouse-gas-concentrations/#variable-name-mapping)
<!--- End forcings -->

## Getting the data

If you install [esgpull](https://esgf.github.io/esgf-download/),
you can download all the data associated with the source IDs above
with the script shown below.
Note that this will download all the data
associated with these source IDs,
which is likely to be much more data
than you actually need to run your model.

```sh
#!/bin/bash

EXPERIMENT_NAME="abrupt-2xCO2"

esgpull add --track --tag ${EXPERIMENT_NAME} source_id:CR-CMIP-1-0-0
esgpull update --tag ${EXPERIMENT_NAME} --yes
esgpull download --tag ${EXPERIMENT_NAME}
```
