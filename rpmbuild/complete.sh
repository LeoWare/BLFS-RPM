#!/bin/bash
set -o errexit	# exit if error
set -o nounset	# exit if variable not initalized
set +h		# disable hashall
#	Customizable environment variables
export FAILURE="$(pwd)/FAILURE"
#	Commence with the bombardment
[ -f ${FAILURE} ] && (printf "FAILURE detected exiting script \n";exit 1)
printf "Building packages\n"
SPECS/builder.sh
