#!/usr/bin/env bash

# For ... reasons, pandas needs the DISPLAY variable to be set
# Running as a cronjob it will not, so set it. Do not clobber already set values
if [[ -z ${DISPLAY} ]]
then
    export DISPLAY=localhost:10.0
fi

SCRIPTDIR=$(readlink -f "${BASH_SOURCE%/*}")

"${SCRIPTDIR}"/isp_checker.py -o "${SCRIPTDIR}"/speedData.csv
