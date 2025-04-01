<!--- This file contains a number of sections -->
<!--- They are bounded by comments like this -->
<!--- Do not edit these sections by hand -->
<!--- Start title -->
# piControl
<!--- End title -->

## One-line description

<!--- Start one-line-description -->
Coupled atmosphere-ocea preindustrial control run (concentration driven)
<!--- End one-line-description -->

## Longer description

<!--- Start longer-description -->
DECK: pre-industrial control
 Pre-industrial control simulation
<!--- End longer-description -->

## Other experiment info

<!--- Start other-experiment-info -->
<!--- End other-experiment-info -->

## Forcings

The forcings required for this experiment are listed below.
For each forcing, we provide a short-hand/common name,
followed by the source ID from which this forcing should be retrieved.
Where relevant, we also provide further information.

<!--- Start forcings -->
- anthropogenic-emissions: [CEDS-CMIP-2025-03-18, CEDS-CMIP-2025-03-18-supplemental](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22CEDS-CMIP-2025-03-18%22%2C%22CEDS-CMIP-2025-03-18-supplemental%22%5D%7D)
    - Further information: https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/anthropogenic-slcf-co2-emissions/
- biomass-burning-emissions: [DRES-CMIP-BB4CMIP7-2-0](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22DRES-CMIP-BB4CMIP7-2-0%22%5D%7D)
    - Further information: https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/open-biomass-burning-emissions/
- land-use: [UofMD-landState-3-1-1](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22UofMD-landState-3-1-1%22%5D%7D)
    - Further information: https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/land-use/
- greenhouse-gas-concentrations: [CR-CMIP-1-0-0](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22CR-CMIP-1-0-0%22%5D%7D)
    - Further information: There are multiple options for how to get the radiative effect of all greenhouse gases, for details see https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/greenhouse-gas-concentrations/#species-provided
- volcanic: [UOEXETER-CMIP-2-0-0](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22UOEXETER-CMIP-2-0-0%22%5D%7D)
    - Further information: https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/stratospheric-volcanic-so2-emissions-aod/
- ozone: Not available yet
- nitrogen-deposition: Not available yet
- solar: [SOLARIS-HEPPA-CMIP-4-6](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&activeFacets=%7B%22source_id%22%3A%5B%22SOLARIS-HEPPA-CMIP-4-6%22%5D%7D)
    - Further information: https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/solar/
- aerosol-optical-properties: Available outside ESGF
    - Further information: https://input4mips-cvs.readthedocs.io/en/latest/dataset-overviews/aerosol-optical-properties-macv2-sp/
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

EXPERIMENT_NAME="piControl"

esgpull add --track --tag ${EXPERIMENT_NAME} source_id:CEDS-CMIP-2025-03-18,CEDS-CMIP-2025-03-18-supplemental,DRES-CMIP-BB4CMIP7-2-0,UofMD-landState-3-1-1,CR-CMIP-1-0-0,UOEXETER-CMIP-2-0-0,SOLARIS-HEPPA-CMIP-4-6
esgpull update --tag ${EXPERIMENT_NAME} --yes
esgpull download --tag ${EXPERIMENT_NAME}
```
