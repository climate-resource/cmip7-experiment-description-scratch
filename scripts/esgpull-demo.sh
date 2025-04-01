#!/bin/bash

EXPERIMENT_NAME="historical"

esgpull add --track --tag ${EXPERIMENT_NAME} source_id:CEDS-CMIP-2025-03-18,CEDS-CMIP-2025-03-18-supplemental,DRES-CMIP-BB4CMIP7-2-0,UofMD-landState-3-1-1,CR-CMIP-1-0-0,UOEXETER-CMIP-2-0-0,SOLARIS-HEPPA-CMIP-4-6
esgpull update --tag ${EXPERIMENT_NAME} --yes
esgpull download --tag ${EXPERIMENT_NAME}
