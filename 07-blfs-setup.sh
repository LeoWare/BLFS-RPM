#!/bin/bash
#################################################
#	Title:	07-blfs-setup.sh		#
#        Date:	2018-02-09			#
#     Version:	1.1				#
#      Author:	baho-utot@columbus.rr.com	#
#     Options:					#
#################################################
#
set -o errexit					# exit if error...insurance ;)
set -o nounset					# exit if variable not initalized
set +h						# disable hashall
PRGNAME=${0##*/}				# script name minus the path
TOPDIR=${PWD}
PARENT=/usr/src/Octothorpe
LOGFILE=$(date +%Y-%m-%d).log
#LOGFILE=/dev/null				# uncomment to disable log file
#
#	Common support functions
#
die() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	false
	exit 1
}
msg() {
	printf "%s\n" "${1}"
	return
}
msg_line() {
	printf "%s" "${1}"
	return
}
msg_failure() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	printf "${_red}%s${_normal}\n" "FAILURE"
	exit 2
}
msg_success() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "SUCCESS"
	return
}
msg_log() {
	printf "\n%s\n\n" "${1}" >> ${_logfile} 2>&1
	return
}
end-run() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "Run Complete"
	return
}
#
#	Functions
#
_wget_list() {
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/wget-blfs <<- EOF
			 http://anduin.linuxfromscratch.org/BLFS/blfs-bootscripts/blfs-bootscripts-20170731.tar.xz
			 https://www.kernel.org/pub/software/utils/pciutils/pciutils-3.5.5.tar.xz
		EOF
	msg_success
	return
}
_md5sum_list(){
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/md5sum-blfs <<- EOF
			238d9969cc0de8b9105d972007d9d546	SOURCES/pciutils-3.5.5.tar.xz
			feeffb543c42d3a9790d4e77437b57db	SOURCES/blfs-bootscripts-20170731.tar.xz
		EOF
	msg_success

	return
}
_copy_source() {
	#	Copy build system to $LFS
	#	Directories to copy
	msg_line "	Installing build system: "
		cp -ar *  ${PARENT}
		chmod 777 ${PARENT}/*.sh
	msg_success
	return
}
#
#	Main line
#
[ -z ${PARENT} ]		&& { echo "${PRGNAME}: PARENT: not set";exit 1; }
[ -z ${LOGFILE} ]		&& { echo "${PRGNAME}: LOGFILE: not set";exit 1; }
_copy_source			#	Copy build system to $LFS
_wget_list			#	Create wget list
_md5sum_list			#	Create md5sum list
end-run