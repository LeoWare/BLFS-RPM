#!/bin/bash
#################################################
#	Title:	rpm-lint.sh			#
#        Date:	2018-02-19			#
#     Version:	1.0				#
#      Author:	baho-utot@columbus.rr.com	#
#     Options:					#
#################################################
set -o errexit	# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
TOPDIR=${PWD}
	#	Build variables
LC_ALL=POSIX
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin
export LC_ALL PATH
#
PARENT=/usr/src/Octothorpe
LOGPATH=${TOPDIR}/LOGS/BLFS
INFOPATH=${TOPDIR}/INFO/BLFS
SPECPATH=${TOPDIR}/SPECS/BLFS
PROVIDESPATH=${TOPDIR}/PROVIDES/BLFS
REQUIRESPATH=${TOPDIR}/REQUIRES/BLFS
RPMPATH=${TOPDIR}/RPMS
#
#	Build functions
#
die() {	
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	exit 1
}
msg() {
	printf "%s\n" "${1}"
}
msg_line() {
	printf "%s" "${1}"
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
	return 0
}
end-run() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "Run Complete"
	return
}

maker(){	#	$1:	name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	local _filespec=${SPECPATH}/${1}.spec
	#
	#	Build
	#
	msg_line "	Building: ${1}: "
	if [ -z ${_pkg} ]; then
		rm ${_log}.installed > ${_log} 2>&1	|| true
		rm ${INFOPATH}/${1} > ${_log} 2>&1	|| true
		rpmbuild -ba \
			${_filespec} >> ${_log} 2>&1 && msg_success || msg_failure
		_pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print)
	else
		msg "Skipped"
		#	return
	fi
}
info(){		#	$1:	Name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	#
	#	Info
	#
	msg_line "	Info: ${1}: "
	[ -z ${_pkg} ] && die "ERROR: rpm package not found"
	if [ ! -e ${INFOPATH}/${1} ]; then
		rpm -qilp \
			${_pkg} > ${INFOPATH}/${1} 2>&1 || true
		rpm -qp --provides \
			${_pkg} > ${PROVIDESPATH}/${1} 2>&1 || true
		rpm -qp --requires \
			${_pkg} > ${REQUIRESPATH}/${1} 2>&1 || true
		msg_success
	else
		 msg "Skipped"
	fi
}
installer(){	#	$1:	name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	#
	#	Install
	#
	msg_line "	Installing: ${1}: "
	[ -z ${_pkg} ] && die "ERROR: rpm package not found"
	if [ ! -e ${_log}.installed ]; then
		su -c "rpm -Uvh --nodeps ${_pkg}" >> "${_log}" 2>&1  && msg_success || msg_failure
		mv ${_log} ${_log}.installed
	else
		msg "Skipped"
	fi
}
_prepare() {
	return
	local _log="${LOGPATH}/${1}"
	msg "	Prepare processing:"
	if [ ! -e ${LOGPATH}/${1} ]; then
		true
	fi		
	touch ${_log}
	return
}
_post() {
	return
	local _log="${LOGPATH}/${1}"
	msg "	Post processing:"
	if [ ! -e ${LOGPATH}/${1} ]; then
		msg_line "	BLFS: Post: " 
		msg_success
	fi		
	touch ${_log}
	return
}
#
#	Main line
#
[ -z ${PARENT} ]	&& die "${PRGNAME}: Variable: PARENT not set: FAILURE"
#
#	Mainline
#
msg "Building Lint"
#	Dependences
LIST+="cpio pcre glib gobject-introspection "
#	Lint
LIST+="rpmlint rpm"
for i in ${LIST};do
	rm -rf BUILD BUILDROOT
	case ${i} in
		prepare)	_prepare ${i}	;;
		post)		_post ${i}	;;
		*)		maker ${i}	
				info  ${i}
				installer ${i}	;;
	esac
done
end-run